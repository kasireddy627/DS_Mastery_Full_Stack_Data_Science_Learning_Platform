from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta
from sqlalchemy.sql import func


# ---------------------------------------------------------
# USER MODEL
# ---------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    # Relations
    subscription = db.relationship("Subscription", uselist=False, back_populates="user")
    payments = db.relationship("Payment", back_populates="user")
    progress = db.relationship("Progress", back_populates="user", cascade="all, delete-orphan")

    # Check subscription status
    def has_active_subscription(self):
        s = self.subscription
        if not s:
            return False
        return s.is_active()

    # Admin check (secure)
    def check_admin(self):
        from config import ADMIN_EMAILS
        return self.email in ADMIN_EMAILS or self.is_admin


# ---------------------------------------------------------
# MODULE MODEL (Main course modules)
# ---------------------------------------------------------
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_free = db.Column(db.Boolean, default=False)
    content_html = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    lessons = db.relationship("Lesson", back_populates="module", cascade="all, delete-orphan")


# ---------------------------------------------------------
# LESSON MODEL (Inside module)
# ---------------------------------------------------------
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    content_html = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)

    module = db.relationship("Module", back_populates="lessons")


# ---------------------------------------------------------
# PAYMENT MODEL
# ---------------------------------------------------------
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    amount = db.Column(db.Integer)  # paise
    currency = db.Column(db.String(10), default="INR")
    provider = db.Column(db.String(100), default="razorpay")
    provider_payment_id = db.Column(db.String(200))
    provider_order_id = db.Column(db.String(200))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship("User", back_populates="payments")


# ---------------------------------------------------------
# SUBSCRIPTION MODEL
# ---------------------------------------------------------
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    provider_sub_id = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)

    user = db.relationship("User", back_populates="subscription")

    def is_active(self):
        if not self.active:
            return False
        if self.end_date and datetime.utcnow() > self.end_date:
            return False
        return True


# ---------------------------------------------------------
# PROGRESS MODEL (Tracks completion)
# ---------------------------------------------------------
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    
    completed = db.Column(db.Boolean, default=False)
    last_viewed = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship("User", back_populates="progress")
    module = db.relationship("Module")


# ---------------------------------------------------------
# OPTIONAL (Future Feature):
# QUIZ SYSTEM (Placeholder)
# ---------------------------------------------------------
"""
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
    text = db.Column(db.Text)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    text = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean, default=False)
"""
