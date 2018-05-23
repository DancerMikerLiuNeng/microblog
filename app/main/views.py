from datetime import datetime
from flask import render_template, session, redirect, url_for,flash,current_app, abort

from . import  main
from .forms import NameForm
from ..email import send_email
from .. import db
from ..models import  User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
        # session['name'] = form.name.data
        # return redirect(url_for('index'))
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash('Looks like you have changed your name!')
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'],'New User',
                           'mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known',False))

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


