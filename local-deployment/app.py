import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from datetime import *
app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://host.docker.internal:27017/birthdays"
app.config["MONGO_URI"] =  os.environ.get('MONGO_URI')
mongo = PyMongo(app)
date_today = date.today()

@app.route("/")
def main():
    return "hello users"

@app.route('/hello/<username>', methods=['GET', 'PUT'])
def user(username):
    if request.method == 'GET':
        data = mongo.db.users.find_one_or_404({"_id": username})
        birth_year, birth_month, birth_day = list(map(int,data.get('dateOfBirth').split('-')))
        birth_date = date(birth_year, birth_month, birth_day)
        if date_today.month == birth_date.month and date_today.day == birth_date.day:
            return { "message": f"Hello, {username}! Happy birthday!" }, 200
        else:
            if (date(date_today.year, birth_date.month, birth_date.day) - date_today).days > 0:
                days = (date(date_today.year, birth_date.month, birth_date.day) - date_today).days
            else:
                days = (date(date_today.year+1, birth_date.month, birth_date.day) - date_today).days
            return { "message": f"Hello, {username}!Your birthday is in {days} day(s)"}, 200

    if request.method == 'PUT':
        if not username.isalpha():
            return jsonify({'ok': False, 'message': 'Bad request parameters!Please provide username with only alphabetical letters'}), 400
        data = request.get_json()
        if data.get('dateOfBirth') is  None:
            return jsonify({'ok': False, 'message': 'Bad request parameters!Please provide dateOfBirth key value'}), 400
        birth_year, birth_month, birth_day = list(map(int,data.get('dateOfBirth').split('-')))
        birth_date = date(birth_year, birth_month, birth_day)
        if birth_date >= date_today :
            return jsonify({'ok': False, 'message': 'Bad request parameters!Please provide dateOfBirth key value before the today date'}), 400
        user_data = mongo.db.users.find_one({"_id": username})
        dateOfBirth = data.get('dateOfBirth')
        merged_dict = data.copy()
        merged_dict.update({"_id": username})
        if user_data is None:
            mongo.db.users.insert_one(merged_dict)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 204
        else:
            mongo.db.users.update_one({"_id": username},{ '$set': { "dateOfBirth" : dateOfBirth }})
            return jsonify({'ok': True, 'message': 'User date of birth updated successfully !'}), 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
