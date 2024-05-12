FROM python:3.11-slim


RUN apt-get update
RUN apt-get install -y git

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt


COPY . /app

RUN pip install git+https://github.com/Myortv/fastapi-plugins.git@dev

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "app/core/log.config"]
