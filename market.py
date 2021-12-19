from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/// users.db'
app.config['SECRET_KEY'] = "my super secret key that no one knows"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added: object = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash(" Form submitted Successfully")
    return render_template("contact.html",
                           name=name,
                           form=form)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/activities')
def activities_page():
    items = [
        {'id': 1, 'Jour': 'Lundi', 'Heure': '18h', 'Theme': 'Etude Biblique', 'Platform': "Whatsapp"},
        {'id': 2, 'Jour': 'Jeudi', 'Heure': '19h', 'Theme': 'Soiree intercession', 'Platform': "Telegram"},
        {'id': 3, 'Jour': 'Dimanche', 'Heure': '20h', 'Theme': 'Soiree adoration', 'Platform': "Whatsapp"}
    ]
    return render_template('activities.html', items=items)


@app.route('/contact')
def contact_page():
    return render_template('contact.html')


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)
    except:
        flash("whoops! There was a problem deleting user record ")

        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)
