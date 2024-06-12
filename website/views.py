from flask import Blueprint, render_template, request, flash, jsonify, abort, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Note, User, Form
from . import db
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/feedback', methods=['GET', 'POST'])
@login_required
def notes():
    form = Form()
    if form.validate_on_submit():
        note = form.feedback.data
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', category='success')
        return redirect(url_for('views.notes'))

    """
    note = form.feedback.data
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', category='success')
        return redirect(url_for('views.notes'))
    """
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', category="error")
        return redirect(url_for('auth.login', next=request.path))

    return render_template("feedback.html", user=current_user, form=form)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/user/<username>', methods=['GET', 'POST'])
def userpage(username):
    possibilities = ['Change appearance', 'See reached level and points',
                     'Make a point purchase and see status of order']
    user = User.query.filter_by(username=username).first()

    if not user:
        abort(404)

    if not current_user.is_authenticated:
        flash("Please log in to access this page.", category="error")
        return redirect(url_for('auth.login', next=request.path))

    if current_user.username == username:
        return render_template("userpage.html", username=username, user=user, possibilities=possibilities)

    else:
        abort(404)
