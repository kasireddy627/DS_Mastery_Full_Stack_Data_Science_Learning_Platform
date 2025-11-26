
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Module


admin_bp = Blueprint("admin_ui", __name__, url_prefix="/admin")


# -------------------------------------------------------------------
# ADMIN RESTRICTION
# -------------------------------------------------------------------
@admin_bp.before_request
def restrict():
    if (not current_user.is_authenticated) or (not current_user.check_admin()):
        flash("Admin access required", "danger")
        return redirect(url_for("auth.login"))


# -------------------------------------------------------------------
# ADMIN DASHBOARD  (HARD SORT: ORDER -> ID)
# -------------------------------------------------------------------
@admin_bp.route("/")
def index():
    # Use Python-level sorting to avoid database caching issues
    modules = sorted(
        Module.query.all(),
        key=lambda m: (m.order, m.id)
    )
    return render_template("admin/index.html", modules=modules)


# -------------------------------------------------------------------
# CREATE MODULE
# -------------------------------------------------------------------
@admin_bp.route("/module/new", methods=["GET", "POST"])
def new_module():
    if request.method == "POST":
        slug = request.form.get("slug")
        title = request.form.get("title")
        desc = request.form.get("description")
        is_free = bool(request.form.get("is_free"))
        content_html = request.form.get("content_html") or ""
        order = int(request.form.get("order") or 0)

        module = Module(
            slug=slug,
            title=title,
            description=desc,
            is_free=is_free,
            content_html=content_html,
            order=order
        )

        db.session.add(module)
        db.session.commit()

        flash("Module created successfully!", "success")
        return redirect(url_for("admin_ui.index"))

    return render_template("admin/new_module.html")


# -------------------------------------------------------------------
# EDIT MODULE
# -------------------------------------------------------------------
@admin_bp.route("/module/<int:id>/edit", methods=["GET", "POST"])
def edit_module(id):
    module = Module.query.get_or_404(id)

    if request.method == "POST":
        module.slug = request.form.get("slug")
        module.title = request.form.get("title")
        module.description = request.form.get("description")
        module.is_free = bool(request.form.get("is_free"))
        module.content_html = request.form.get("content_html") or ""
        module.order = int(request.form.get("order") or 0)

        db.session.commit()

        flash("Module updated!", "success")
        return redirect(url_for("admin_ui.index"))

    return render_template("admin/edit_module.html", module=module)


# -------------------------------------------------------------------
# DELETE MODULE
# -------------------------------------------------------------------
@admin_bp.route("/module/<int:id>/delete", methods=["POST"])
def delete_module(id):
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()

    flash("Module deleted!", "info")
    return redirect(url_for("admin_ui.index"))
