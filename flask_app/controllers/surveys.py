from flask import session, flash, render_template, redirect, request
from flask_app import app
from flask_app.models.survey import Survey

@app.route('/')
def send_home():
    return redirect("/survey")

@app.route('/survey')
def survey_page():
    dojos = Survey.get_dojos()
    languages = Survey.get_languages()
    return render_template("index.html", dojos = dojos, languages = languages)

@app.route('/survey/submit', methods=['POST'])
def submit_survey():
    if Survey.validate_form_data(request.form):
        data = {
            'user_name' : request.form['user_name'],
            'dojo_name' : request.form['dojo_name'],
            'fav_language' : request.form['fav_language'],
            'comments' : request.form['comments']
        }
        Survey.save(data)
        return redirect('/show')
    else:
        return redirect('/survey')

@app.route('/show')
def show_all():
    survey_data = Survey.show_all()
    return render_template("showAll.html", surveys = survey_data)