FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install -r requirements.txt
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords');"
CMD gunicorn -w 3 -b :8000 --timeout 300 cs410videosearchengine.wsgi:application
