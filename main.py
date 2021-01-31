from flask import Flask, render_template, redirect, url_for, request
from forms import CreateProjectForm, WorkExperience, Certificates, Skills, User
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from apiclient.discovery import build
import smtplib
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
load_dotenv()

apikey = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=apikey)

req = youtube.search().list(q='Incognito Relationships',
                            part='snippet', type='video')
res = req.execute()
incognito_relationships = res["items"][0]['id']['videoId']

request = youtube.search().list(q='Karma-A Short Film Aman Shrivastava',
                                part='snippet', type='video')
response = request.execute()
karma = response["items"][0]["id"]["videoId"]


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    icon = db.Column(db.String(1000))


class WorkExp(db.Model):
    __tablename__ = "work-experience"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    company = db.Column(db.String(1000))
    link = db.Column(db.String(1000))
    description = db.Column(db.String(1000))


class Certificate(db.Model):
    __tablename__ = "certificates"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    certificate_type = db.Column(db.String(1000))
    description = db.Column(db.String(1000))


class Skill(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    languages = db.Column(db.String(1000))
    databases = db.Column(db.String(1000))
    web = db.Column(db.String(1000))
    frameworks = db.Column(db.String(1000))


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    all_certificates = db.session.query(Certificate).all()
    all_skills = db.session.query(Skill).all()
    all_work_exp = db.session.query(WorkExp).all()
    all_projects = db.session.query(Project).all()
    return render_template("index.html", incognito_relationships=incognito_relationships, karma=karma, all_certificates=all_certificates, all_skills=all_skills, all_work_exp=all_work_exp, all_projects=all_projects)


@app.route("/aman/project", methods=["GET", "POST"])
def projects():

    form = CreateProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            title=form.title.data,
            description=form.description.data,
            url=form.url.data,
            icon=form.icon.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("portfolio.html", form=form, id=1)


@app.route("/aman/workexperience", methods=["GET", "POST"])
def work():

    form = WorkExperience()
    if form.validate_on_submit():
        new_work_experience = WorkExp(
            date=form.date.data,
            title=form.title.data,
            company=form.company.data,
            link=form.link.data,
            description=form.description.data
        )
        db.session.add(new_work_experience)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("portfolio.html", form=form, id=2)


@app.route("/aman/skills", methods=["GET", "POST"])
def skills():

    form = Skills()
    if form.validate_on_submit():
        new_skill = Skill(
            languages=form.languages.data,
            web=form.web.data,
            databases=form.databases.data,
            frameworks=form.frameworks.data
        )
        db.session.add(new_skill)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("portfolio.html", form=form, id=3)


@app.route("/aman/certificates", methods=["GET", "POST"])
def certificate():
    form = Certificates()
    if form.validate_on_submit():
        new_certificate = Certificate(
            date=form.date.data,
            title=form.title.data,
            certificate_type=form.certificate_type.data,
            description=form.description.data,
        )
        db.session.add(new_certificate)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("portfolio.html", form=form, id=4)


@app.route("/mail", methods=["GET", "POST"])
def mail():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        comment = request.form["comment"]
        message = f"Subject:Recieved a message from your portfolio website!\n\n name: {name}\nemail: {email}\ncomment: {comment}"

        my_email = os.getenv("MY_EMAIL")
        my_password = os.getenv("MY_PASSWORD")

        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=os.getenv("MY_EMAIL"), msg=message.encode("utf-8"))
        # connection.close()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
