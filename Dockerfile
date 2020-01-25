FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENTRYPOINT FLASK_APP=./app.py flask run --host=0.0.0.0 --port=8080
