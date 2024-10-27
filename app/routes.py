from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        # Проверяем, существует ли уже пользователь с таким email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Этот адрес электронной почты уже используется. Пожалуйста, выберите другой.', 'danger')
            return render_template("register.html", form=form)
        
        # Хешируем пароль и создаем нового пользователя
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Добавляем пользователя в сессию и коммитим изменения
        db.session.add(user)
        db.session.commit()
        
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user and email and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверно введены данные аккаунта', 'danger')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/readme')
def readme():
    return render_template('readme.html')

@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/collect_star', methods=['POST'])
@login_required
def collect_star():
    current_user.stars += 1  # Увеличиваем количество звезд на 1
    db.session.commit()
    return jsonify({'success': True, 'stars': current_user.stars})