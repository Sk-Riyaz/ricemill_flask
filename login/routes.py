from flask import render_template, request, redirect, url_for, flash

from login import login
from login.forms import LoginForm


@login.route('/login', methods=['GET', 'POST'])
def login():
    genericData = {
        "title": "Sign In",
        "heading": "Login"
    }
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))

    return render_template("login.html", data=genericData, form=form)

