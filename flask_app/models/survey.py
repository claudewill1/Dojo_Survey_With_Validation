from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
class Survey:
    db_name = "dojo_survey_schema"
    def __init__(self,data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.location = data["location"]
        self.languages = data["languages"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validateSurvey(survey):
        isValid = True
        if not NAME_REGEX.match(survey["name"]):
            isValid = False
            flash("Name can only contain letters")
        if len(survey["name"]) < 2:
            isValid = False
            flash("Name must be at least 2 characers long")
        if not survey["location"]:
            isValid = False
            flash("Location required")
        if not survey["language"]:
            isValid = False
            flash("Language is required")
        if not survey["comment"]:
            isValid = False
            flash("A comment is Required")
        return isValid

    @classmethod
    def addNewSurvey(cls,data):
        query = "INSERT INTO dojos (name, location, languages, comment) VALUES (%(name)s,%(location)s,%(language)s,%(comment)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def getSurvey(cls,id):
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        data = {
            "id": id
        }
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def getMostRecentSurvey(cls):
        query = "SELECT * FROM dojos ORDER BY dojos.id DESC LIMIT 1;"
        result = connectToMySQL(cls.db_name).query_db(query)
        return cls(result[0])