FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 5000

COPY . /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

