from trees_app.models.user import User
from trees_app.config.mysqlconnections import connectToMySQL
from flask import flash


class Tree:
    db = "arbortrary_trees_schema"

    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Below was for JOIN appointments on users
        self.user = None

    @staticmethod
    def validate_tree(data):
        is_valid = True
        if len(data['species']) < 5:
            flash("Species must be at least 5 characters", "species")
            is_valid = False
        if len(data['location']) < 2:
            flash("Location must be at least 2 characters", "location")
            is_valid = False
        if len(data['reason']) >= 50:
            flash("Reasons must be 50 characters or less", "reason")
            is_valid = False
        if data['date'] == "":
            flash("Date required", "date")
            is_valid = False
        return is_valid
    # (2^) Validations

    @classmethod
    def save(cls, data):
        query = "INSERT INTO trees (species, location, reason, date, user_id) VALUES (%(species)s, %(location)s, %(reason)s, %(date)s, %(user_id)s);"
        new_tree_id = connectToMySQL(cls.db).query_db(query, data)
        return new_tree_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trees JOIN users ON user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        trees = []
        for row in results:
            info = cls(row)
            data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            info.user = User(data)
            trees.append(info)
        return trees

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trees WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        tree = cls(results[0])
        return tree

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return "delete!"

    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET species = %(species)s, location = %(location)s, reason = %(reason)s, date = %(date)s WHERE id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return "update!"
