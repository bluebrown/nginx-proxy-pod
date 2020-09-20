FROM python

COPY ./requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app

CMD ["uvicorn", "main:app", "--reload", "--root-path", "/api"]
