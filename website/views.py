from flask import Blueprint, render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/feedback', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')

    return render_template("feedback.html", user=current_user)


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

@views.route('/user/<username>',methods=['GET', 'POST'])
def userpage(username):
    possibilities = ['Change appearance', 'See reached level and points', 'Make a point purchase and see status of order']
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template('userpage.html', user=user, possibilities=possibilities)
