from flask_app.config.mysqlonnection import connectToMySQL
from flask import flash

class Survey:
    def __init__(self, data) -> None:
        self.user_name = data['user_name']
        self.dojo_name = data['dojo_name']
        self.language_name = data['language_name']
        self.comment = data['comment']

    def show_all() -> list:
        query = '''SELECT surveys.user_name, dojos.name, languages.name, surveys.comment FROM surveys
LEFT JOIN survey_dojos ON surveys.id = survey_dojos.survey_id
LEFT JOIN dojos ON survey_dojos.dojo_id = dojos.id
LEFT JOIN survey_languages ON surveys.id = survey_languages.survey_id
LEFT JOIN languages ON survey_languages.language_id = languages.id;
'''     
        results = connectToMySQL('dojo_surveys').query_db(query)
        print(results)
        return results

    def get_dojos() -> list:
        query = 'SELECT id, name FROM dojos;'
        results = connectToMySQL('dojo_surveys').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(dojo)
        return dojos
    @staticmethod
    def has_dojo(data) -> bool:
        query = 'SELECT id FROM dojos WHERE id = %(id)s;'
        results = connectToMySQL('dojo_surveys').query_db(query, data)
        if results:
            return True
        else:
            return False

    def get_languages() -> list:
        query = 'SELECT id, name FROM languages;'
        results = connectToMySQL('dojo_surveys').query_db(query)
        languages = []
        for language in results:
            languages.append(language)
        return languages
    @staticmethod
    def has_language(data) -> bool:
        query = 'SELECT id FROM languages WHERE id = %(id)s;'
        results = connectToMySQL('dojo_surveys').query_db(query, data)
        if results:
            return True
        else:
            return False

    @staticmethod
    def validate_form_data(data):
        print(data['user_name'])
        print(data['dojo_name'])
        print(data['fav_language'])
        is_valid = True
        if len(data['user_name']) <= 0 or data['user_name'].isspace() == True:
            flash('Invalid Name. Please fill properly.', 'name_error')
            is_valid = False
        if Survey.has_dojo({'id' : data['dojo_name']}) == False:
            flash('Invalid Dojo. Please select actual dojo', 'dojo_error')
            is_valid = False
        if Survey.has_language({'id' : data['fav_language']}) == False:
            flash('Invalid Language', 'lang_error')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data) -> None:
        query = '''INSERT INTO surveys (user_name, comment) VALUES(%(user_name)s, %(comments)s);'''
        data['id'] = connectToMySQL('dojo_surveys').query_db(query, data)
        query = '''INSERT INTO survey_languages (language_id, survey_id) VALUES(%(fav_language)s, %(id)s);'''
        connectToMySQL('dojo_surveys').query_db(query, data)        
        query = '''INSERT INTO survey_dojos (dojo_id, survey_id) VALUES(%(dojo_name)s, %(id)s);'''
        connectToMySQL('dojo_surveys').query_db(query, data)