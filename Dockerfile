FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY ./libreria/jwa.py /usr/local/lib/python3.9/site-packages/jwt
ENV FLASK_APP=start.py
ENV FLASK_DEBUG=1

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]