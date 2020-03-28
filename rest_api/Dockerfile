FROM python:3.8-slim-buster

WORKDIR .
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run"]