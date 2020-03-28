FROM python:3.8-slim-buster

WORKDIR .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

CMD ["./wait-for-it.sh", "database:3306", "-s", "-t", "30", "--", "python", "./main.py"]