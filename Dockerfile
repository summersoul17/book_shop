FROM python:3.10-slim

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]