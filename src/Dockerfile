FROM python

RUN mkdir -p usr/src
WORKDIR /usr/src

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["gunicorn", "--bind=0.0.0.0:8000", "app.app:app"]