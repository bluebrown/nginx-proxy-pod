FROM python

COPY ./requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app

ENV FLASK_DEBUG=1
ENV FLASK_ENV development
ENV FLASK_APP=app.py


CMD ["flask", "run", "--host", "0.0.0.0"]
