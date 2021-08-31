FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY ./app app
RUN pip install -r app/requirements.txt
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "[general]\nemail = \"your-email@domain.com\"\n" > /root/.streamlit/credentials.toml'
ENTRYPOINT ["streamlit", "run"]
CMD ["app/main.py"]