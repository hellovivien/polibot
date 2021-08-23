# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
# EXPOSE 8000
# COPY ./app app
# RUN pip install -r app/requirements.txt
# CMD ["python3", "fastapi/app/main.py"]

FROM python:3.8
EXPOSE 8080
WORKDIR /app
COPY ./app app
RUN pip install -r app/requirements.txt
CMD ["python3", "app/start.py"]