# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    # postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/fmeiraf/LLM-budget-assistant.git .

RUN pip3 install -r requirements.txt

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health
