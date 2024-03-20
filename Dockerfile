FROM python:3.12

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
