from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
class Car:
    def __init__( self , data ):
        self.id = data['id']
        self.price = data['price']
        self.make = data['make']
        self.year = data['year']
        self.model= data['model']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.desc= data['description']
        self.user = {}

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id=cars.user_id;"
        results = connectToMySQL('belt_exam').query_db(query)
        cars = []
        for row in results:
            car = cls(row)

            user_data ={ 
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "password" : row['password']
            }
            car.user=user.User(user_data)


            cars.append( car )
        return cars

    @classmethod
    def create(cls, data):
        query = "INSERT INTO cars (price, make, model, description, year, created_at, updated_at, user_id) VALUES (%(price)s,%(make)s,%(model)s,%(desc)s,%(year)s,NOW(),NOW(), %(user_id)s)"
        results = connectToMySQL('belt_exam').query_db(query,data)
        return
            
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id=cars.user_id WHERE cars.id = %(car_id)s;"
        result = connectToMySQL('belt_exam').query_db(query,data)
        car = cls(result[0])
        user_data ={
            "id" : result[0]['users.id'],
            "first_name" : result[0]['first_name'],
            "last_name" : result[0]['last_name'],
            "email" : result[0]['email'],
            "created_at" : result[0]['users.created_at'],
            "updated_at" : result[0]['users.updated_at'],
            "password" : result[0]['password']
            }
        car.user=user.User(user_data)
        return car


    @classmethod
    def update_one(cls, data):
            query = "UPDATE cars SET  price= %(price)s, make= %(make)s, model= %(model)s, description=  %(desc)s, year= %(year)s, updated_at=NOW() WHERE user_id =  %(user_id)s;"
            results= connectToMySQL('belt_exam').query_db( query, data )
            return
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id= %(car_id)s;"
        results= connectToMySQL('belt_exam').query_db( query, data )
        return

    @staticmethod
    def validate(info):
        is_valid= True
        if len(info["price"]) <1:
            flash("Please enter price")
            is_valid= False
        if len(info["make"]) <1:
            flash("Please enter make")
            is_valid= False
        if len(info["model"]) <1:
            flash("Please enter model")
            is_valid= False
        if len(info["year"]) <1:
            flash("Please enter year")
            is_valid= False
        if len(info["desc"]) <1:
            flash("Please enter description")
            is_valid= False
        if len(info["year"]) <1:
            flash("year must be greater than 0")
            is_valid= False
        if len(info["price"]) <1:
            flash("price must be greater than 0")
            is_valid= False
        return is_valid