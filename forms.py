from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


class CreateProjectForm(FlaskForm):
    title = StringField("Enter project name", validators=[DataRequired()])
    description = StringField(
        "Enter project description", validators=[DataRequired()])
    url = StringField("Github Url", validators=[DataRequired(), URL()])
    icon = StringField("Icon", validators=[DataRequired()])
    submit = SubmitField("Submit")


class WorkExperience(FlaskForm):
    date = StringField("Enter Date", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    company = StringField("Company Name", validators=[DataRequired()])
    link = StringField("Company's Website", validators=[DataRequired(), URL()])
    description = StringField("Job Description", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Certificates(FlaskForm):
    date = StringField("Enter Date", validators=[DataRequired()])
    title = StringField("Enter title of certificate",
                        validators=[DataRequired()])
    certificate_type = StringField(
        "Certificate Type", validators=[DataRequired()])
    description = StringField(
        "Certificate Description", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Skills(FlaskForm):
    languages = StringField("Enter Language")
    databases = StringField("Enter Database")
    web = StringField("Enter Web Technology")
    frameworks = StringField("Enter Framework")
    submit = SubmitField("Submit")


class Admin(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
