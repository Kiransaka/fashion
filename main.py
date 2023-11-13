from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from flask_login import login_user, LoginManager, logout_user
from wtforms import SubmitField, StringField,PasswordField
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import pandas as  pd

# all_products = pd.read_csv("product_catalog.csv", delimiter=",", encoding="")
# print(all_products)
with open("product_catalog.csv", "r") as f:
    all_products = [i.split(',') for i in f.readlines()]
class loginform(FlaskForm):
    email = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class registerform(FlaskForm):
    email = StringField(label="Username", validators=[DataRequired()])
    customer_name = StringField(label="Coustmor Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"
db = SQLAlchemy()
db.init_app(app)

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user():
    return home


@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/login", methods=['GET' , 'POST'])
def login():
    Loginform = loginform()
    if Loginform.validate_on_submit():
        result = db.session.execute(db.select(Users).where(Users.email == Loginform.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not user.password== Loginform.password.data:
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=Loginform)

@app.route("/register", methods=["GET", "POST"])
def register():
    Register_form = registerform()
    if Register_form.validate_on_submit():
        new_user = Users(
            username=Register_form.email.data,
            name=Register_form.customer_name.data,
            password=Register_form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html", form=Register_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)

