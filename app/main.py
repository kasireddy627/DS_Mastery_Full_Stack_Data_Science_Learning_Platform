from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from .models import Module
from . import db

main_bp = Blueprint("main", __name__)

# -------------------------------------------------------------------
# HOME & MODULE LISTING (SORT BY ORDER → ID)
# -------------------------------------------------------------------

# @main_bp.route("/")
# def home():
#     featured = Module.query.order_by(Module.order).all()
#     # Optional: If you want to show a special Python Basics card
#     featured_course = Module.query.filter_by(slug="python-basics").first()
#     return render_template("home.html", featured=featured, featured_course=featured_course)

@main_bp.route("/")
def home():
    # Fetch everything (no limit)
    modules = Module.query.all()

    # Hard sort using Python (order → id)
    modules = sorted(modules, key=lambda m: (m.order, m.id))

    # You can still limit if needed:
    # featured = modules[:6]   # show first 6 in sorted order
    featured = modules   # show all

    # python-tutorial card if you want
    featured_course = Module.query.filter_by(slug="python-tutorial").first()

    return render_template("home.html", featured=featured, featured_course=featured_course)


@main_bp.route("/free")
def free_list():
    free_modules = Module.query.filter_by(is_free=True).order_by(Module.order.asc(), Module.id.asc()).all()
    return render_template("free_list.html", modules=free_modules)


@main_bp.route("/modules")
def modules_list():
    modules = Module.query.order_by(Module.order.asc(), Module.id.asc()).all()
    return render_template("free_list.html", modules=modules)



# -------------------------------------------------------------------
# MODULE PAGE (FREE / PAID / LOCKED)
# -------------------------------------------------------------------

@main_bp.route("/module/<slug>")
def module_page(slug):
    """
    Loads module content normally.
    No redirects. Free modules open directly.
    Paid modules require subscription.
    """

    module = Module.query.filter_by(slug=slug).first_or_404()

    # Free module
    if module.is_free:
        return render_template("module.html", module=module)

    # Paid module - require subscription
    if current_user.is_authenticated and current_user.has_active_subscription():
        return render_template("module.html", module=module)

    # Otherwise locked
    return render_template("locked_module.html", module=module)


# -------------------------------------------------------------------
# USER DASHBOARD (SORT BY ORDER → ID)
# -------------------------------------------------------------------

@main_bp.route("/dashboard")
@login_required
def dashboard():
    modules = Module.query.order_by(Module.order.asc(), Module.id.asc()).all()
    return render_template("dashboard.html", modules=modules)
