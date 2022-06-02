from flask import flash
from trees_app.config.mysqlconnections import connectToMySQL
import re  # the regex module
# created regular expression object to use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "arbortrary_trees_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters", "first_name")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "last_name")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address", "email")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters", "password")
            is_valid = False
        if form_data['password'] != form_data['confirm']:
            flash("Passwords don't match", "config")
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        return user
