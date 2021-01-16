FROM python:3.9.0-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 
COPY . /usr/src/app
COPY ./libreria/jwa.py /usr/local/lib/python3.9/site-packages/jwt
ENV FLASK_APP=start.py
ENV FLASK_DEBUG=1

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
#RUN pytest
RUN flake8 /usr/src/app --count --select=E9,F63,F7,F821 --show-source --statistics