FROM python:3
EXPOSE 8080
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
ENV MONGO_URI="mongodb://mongo-0.mongo.birthday-mongodb:27017/birthdays"
ENTRYPOINT FLASK_APP=./app.py flask run --host=0.0.0.0 --port=8080
