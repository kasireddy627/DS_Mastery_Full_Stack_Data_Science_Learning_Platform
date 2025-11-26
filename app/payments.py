from flask import Blueprint, render_template, redirect, url_for, current_app, request, jsonify, flash
from flask_login import login_required, current_user
from . import db
from .models import Payment, Subscription
import razorpay
from datetime import datetime, timedelta
import hmac, hashlib, json

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

def razorpay_client():
    return razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))

@payments_bp.route("/checkout/<int:months>", methods=["GET"])
@login_required
def checkout(months=1):
    # Price logic: 1 month = Rs 499 (example)
    monthly_price_inr = 499
    total_inr = monthly_price_inr * months
    amount_paise = total_inr * 100

    client = razorpay_client()
    # create order on razorpay
    order_receipt = f"order_rcpt_{current_user.id}_{int(datetime.utcnow().timestamp())}"
    order_data = {
        "amount": amount_paise,
        "currency": "INR",
        "receipt": order_receipt,
        "payment_capture": 1
    }
    order = client.order.create(data=order_data)

    # Save minimal pending payment record (optional)
    p = Payment(user_id=current_user.id,
                amount=amount_paise,
                currency="INR",
                provider="razorpay",
                provider_order_id=order.get("id"),
                status="created")
    db.session.add(p)
    db.session.commit()

    return render_template("checkout.html",
                           order=order,
                           key_id=current_app.config['RAZORPAY_KEY_ID'],
                           amount=amount_paise,
                           months=months,
                           total=total_inr)

# Client will POST here after checkout success to mark UX quicker.
# IMPORTANT: webhook is canonical. This endpoint does server-side verification of signature.
@payments_bp.route("/verify", methods=["POST"])
@login_required
def verify_payment():
    data = request.form.to_dict()
    # fields: razorpay_payment_id, razorpay_order_id, razorpay_signature
    payment_id = data.get("razorpay_payment_id")
    order_id = data.get("razorpay_order_id")
    signature = data.get("razorpay_signature")
    client = razorpay_client()

    # Server-side signature verification
    try:
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        client.utility.verify_payment_signature(params_dict)
    except Exception as e:
        current_app.logger.error("Razorpay signature verification failed: %s", e)
        flash("Payment verification failed. We will confirm via webhook.", "danger")
        return redirect(url_for("main.dashboard"))

    # signature OK -> record Payment and create subscription
    payment = Payment.query.filter_by(provider_order_id=order_id).first()
    if payment:
        payment.provider_payment_id = payment_id
        payment.status = "paid"
        db.session.commit()

    # create subscription for 30*months days (for simplicity 30 days per month)
    months = int(request.form.get("months", 1))
    sub = Subscription(user_id=current_user.id,
                       start_date=datetime.utcnow(),
                       end_date=datetime.utcnow() + timedelta(days=30*months),
                       provider_sub_id=payment_id,
                       active=True)
    # replace existing
    existing = current_user.subscription
    if existing:
        db.session.delete(existing)
    db.session.add(sub)
    db.session.commit()

    flash("Payment verified and subscription activated!", "success")
    return redirect(url_for("main.dashboard"))

# Razorpay webhook endpoint (configure this URL in Razorpay Dashboard)
# This is the canonical endpoint to trust for unlocking content.
@payments_bp.route("/webhook", methods=["POST"])
def razorpay_webhook():
    payload = request.get_data(as_text=True)
    sig = request.headers.get('X-Razorpay-Signature')

    webhook_secret = current_app.config.get("RAZORPAY_WEBHOOK_SECRET")
    client = razorpay_client()

    # verify signature using razorpay util
    try:
        client.utility.verify_webhook_signature(payload, sig, webhook_secret)
    except Exception as e:
        current_app.logger.error("Webhook signature verification failed: %s", e)
        return jsonify({"status":"invalid signature"}), 400

    event = json.loads(payload)
    event_type = event.get("event")

    # handle checkout/payment captured events
    if event_type == "payment.captured" or event_type == "payment.authorized":
        # extract payment info
        payment_entity = event["payload"]["payment"]["entity"]
        razorpay_payment_id = payment_entity.get("id")
        razorpay_order_id = payment_entity.get("order_id")
        amount = payment_entity.get("amount")  # paise
        status = payment_entity.get("status")

        # find existing Payment or create
        payment = Payment.query.filter_by(provider_order_id=razorpay_order_id).first()
        if not payment:
            payment = Payment(user_id=None,
                              amount=amount,
                              currency=payment_entity.get("currency", "INR"),
                              provider="razorpay",
                              provider_payment_id=razorpay_payment_id,
                              provider_order_id=razorpay_order_id,
                              status=status)
            db.session.add(payment)
            db.session.commit()
        else:
            payment.provider_payment_id = razorpay_payment_id
            payment.status = status
            db.session.commit()

        # Get the user from metadata if you set it at order creation.
        # But in our code, we created a Payment row with user_id, so check that:
        if payment.user_id:
            user = payment.user
        else:
            # fallback: if order receipt included user id, extract
            # (If you encoded user id into receipt, parse it here)
            user = None

        # For demo: if we have user, create subscription (30 days)
        if user:
            # create or update subscription
            from datetime import datetime, timedelta
            sub = user.subscription
            if sub:
                # extend
                sub.end_date = max(sub.end_date or datetime.utcnow(), datetime.utcnow()) + timedelta(days=30)
                sub.active = True
            else:
                sub = Subscription(user_id=user.id,
                                   start_date=datetime.utcnow(),
                                   end_date=datetime.utcnow()+timedelta(days=30),
                                   provider_sub_id=razorpay_payment_id,
                                   active=True)
                db.session.add(sub)
            db.session.commit()

    # You can handle other events like subscription.charged etc.
    return jsonify({"status":"ok"}), 200
