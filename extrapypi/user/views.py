"""Views for self-user management

If you set ``DASHBOARD = False`` in settings, this blueprint will also be disabled
"""
import logging
from passlib.apps import custom_app_context
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed, RoleNeed
from flask import Blueprint, request, flash, render_template, url_for, redirect

from extrapypi.extensions import db
from extrapypi.forms.user import UserForm, PasswordForm
from extrapypi.models import User

log = logging.getLogger("extrapypi")


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def update_user():
    """Update current logged user
    """
    user = current_user
    form = UserForm(request.form, obj=user)
    del form.role
    del form.is_active

    perm = Permission(
        UserNeed(user.id),
        RoleNeed('admin')
    )
    perm.test()

    if form.validate_on_submit():
        if form.username.data != user.username and User.username_is_in_use(form.username.data):
            flash("This username is already been used. Please choose another one!", "alert-danger")
            form.username.errors.append('Please correct this field')
        elif form.email.data != user.email and User.email_is_in_use(form.email.data):
            flash("This email is already been used. Please choose another one!", "alert-danger")
            form.email.errors.append('Please correct this field')
        else:
            form.populate_obj(user)
            db.session.commit()
            flash("Informations updated", "alert-info")
            return redirect(url_for('dashboard.index'))

    return render_template("user/update.html", form=form, user=current_user)


@blueprint.route('/password', methods=['GET', 'POST'])
@login_required
def update_password():
    """Update current logged user password
    """
    user = current_user
    form = PasswordForm(request.form)

    perm = Permission(
        UserNeed(user.id),
        RoleNeed('admin')
    )
    perm.test()

    if form.validate_on_submit():
        to_check = user.password_hash
        if not custom_app_context.verify(form.current.data, to_check):
            flash("Bad password provided", "alert-danger")
            return render_template("user/pwd_update.html", form=form)

        new_hash = custom_app_context.hash(form.password.data)
        user.password_hash = new_hash
        db.session.commit()

        flash("Password updated", "alert-info")
        return redirect(url_for('dashboard.index'))

    return render_template("user/pwd_update.html", form=form)
