FROM python:3.10
WORKDIR /code
# PROJECT_MODE - choose dev or prod (set in .envrc)
ARG PROJECT_MODE
COPY requirements/${PROJECT_MODE}.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code/
