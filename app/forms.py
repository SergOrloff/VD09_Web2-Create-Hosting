from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Length(max=35)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такой email уже существует')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message="Пожалуйста, введите имя пользователя.")])
    email = StringField('Email', validators=[DataRequired(message="Пожалуйста, введите email пользователя.")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Пожалуйста, введите пароль.")])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')