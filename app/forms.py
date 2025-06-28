from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError
from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email", validators=[DataRequired(), Length(min=2, max=40)])
    phone = StringField("Телефон", validators=[DataRequired(), Length(min=11, max=12)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Подтвердите пароль", validators=[DataRequired(), EqualTo('password')])
    avatar = FileField("Загрузите своё фото", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Зарегистрироваться")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Пользователь с данной почтой уже существует")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Пароль слишком короткий")
        if not any(char.isupper() for char in password.data):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(char.islower() for char in password.data):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву")
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(min=2, max=40)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
