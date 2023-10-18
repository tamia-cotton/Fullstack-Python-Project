from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.password = data['password']
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at,updated_at, password) VALUES (%(firstname)s,%(lastname)s,%(email)s,NOW(),NOW(),%(password)s)"
        results = connectToMySQL('belt_exam').query_db(query,data)
        return 
            
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('belt_exam').query_db(query,data)
        if len(results) < 1: 
            return False
        return cls(results[0])
    
    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('belt_exam').query_db(query,data)
        if len(results) < 1: 
            return True
        flash("Email has been used already")
        return False
            
    @staticmethod
    def validate(info):
        email_reg=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid= True
        if len(info["fname"]) <3:
            flash("First name has to be least 3 characters")
            is_valid= False
        if len(info["lname"]) <3:
            flash("Last name has to be least 3 characters")
            is_valid= False
        if len(info["fname"]) <1:
            flash("Please enter First Name")
            is_valid= False
        if len(info["lname"]) <1:
            flash("Please enter Last Name")
            is_valid= False
        if len(info["email"]) <1:
            flash("Please enter Email")
            is_valid= False
        if len(info["password"]) <1:
            flash("Please enter Password")
            is_valid= False
        if len(info["password"]) <8:
            flash("Please make Password 8 characters long")
            is_valid= False
        if not info["password"] == info["cpassword"]:
            flash("Passwords dont match")
        if not email_reg.match(info['email']):
            flash("Not a valid email")
        if not info["fname"].isalpha():
            flash("can only be letters")
        if not info["fname"].isalpha():
            flash("can only be letters")
            
        return is_valid