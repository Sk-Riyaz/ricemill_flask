from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
# from flask_user import roles_required
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ChangePasswordForm
from app.models import User
from app.utilities import write_to_db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("User already loggedin")
        return redirect(url_for('core.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(
        #    form.username.data, form.remember_me.data))

        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid user or password")
            return redirect(url_for('auth.login'))

        if not user.active:
            flash("You are not authorized to access this page. Please contact Administrator")
            return redirect(url_for('auth.login'))

        #flash("User loggedin")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(current_user.is_admin())
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('core.home')
        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    message = request.args.get("message")
    if message is not None:
        flash(message)
    return redirect(url_for('auth.login'))


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    generic_data = {
        "title": "Change Password",
        "heading": "Change Password"
    }
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.new_password.data)
        status, e = write_to_db(user)
        db.session.commit()
        if status != 200:
            # logger.error(f"status: {status}, {e}")
            abort(status)
        return redirect(url_for('auth.logout',
                                message=("You password changes succesfully."
                                         " Please Login"))
                        )
    return render_template(f"auth/change_password.html", form=form,
                           data=generic_data)
