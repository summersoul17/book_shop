FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . ./

CMD ["uvicorn", "src.main:app", "--reload"]