from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Todo, User
from flask_login import login_user, current_user, logout_user, login_required

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def index():
    return render_template("index.html")

@my_view.route("/yourtodolist", methods=["GET", "POST"])
def yourtodolist():
    todo_list = Todo.query.all()
    return render_template("yourtodolist.html", todo_list = todo_list)

@my_view.route("/add", methods =["POST"])
def add():
    task = request.form.get("task")
    new_todo = Todo(task=task, userid=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("my_view.yourtodolist"))

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.yourtodolist"))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.yourtodolist"))

@my_view.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == 'POST':
        todo.task = request.form['newtext']
        db.session.commit()
        return redirect(url_for('my_view.yourtodolist'))
    return render_template("edittask.html", todo_id = todo_id)

@my_view.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my_view.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('my_view.login'))
    return render_template('register.html')

@my_view.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_view.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('my_view.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@my_view.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('my_view.index'))

