# cs410 final project Video Search Engine

This project is a video search engine, that allows you to upload videos
and the audio from the video gets transcribed into text. Once you upload
the video, topics, and a summary will extracted and then uploaded into elasticsearch.

# This project uses docker

docker-compose up -d --build will run the projects. You need to make sre that aws
config makes it into ~/.aws/config

docker-compose logs will give you logs for what is wrong.

# testing it on the web

The easiest way to test to this project is to visit: 
http://34.224.88.106/


# Implementation

This project uses django, celery, aws transcribe, sklearn, spacy, summa, elasticsearch and nltk.

Django is to serve web requests

Celery for background processing

aws transcribe takes videos and extracts the audio into text data

nltk is used for preprocessing and removing stop words.

elastic search for searching

sklearn and nltk for topic modeling

summa for generating summarizations

The front end is using react.js to make the front end interactive.

## Functions

Topic modeling

https://github.com/colanconnon/cs410project/blob/master/cs410videosearchengine/videosearchengine/text_processing.py#L15

This function preprocessing the data using a count vectorizer and then uses LDA for topic modeling


https://github.com/colanconnon/cs410project/blob/master/cs410videosearchengine/videosearchengine/text_processing.py#L38

Uses the summa library for summarization:

https://pypi.org/project/summa/



For searching three different parts are used.
* Elastic search for finding documents that match the query
https://github.com/colanconnon/cs410project/blob/master/cs410videosearchengine/videosearchengine/search.py#L20

*  spacy for finding where the phrase is in the video
https://github.com/colanconnon/cs410project/blob/master/cs410videosearchengine/videosearchengine/search.py#L41

* This is the http handler for tying everything together.
https://github.com/colanconnon/cs410project/blob/master/cs410videosearchengine/videosearchengine/views.py#L40



# Usage


Uploading Videos
![Alt Text](https://github.com/colanconnon/cs410project/blob/master/uploading_videos.gif)

Searching Videos

![Alt Text](https://github.com/colanconnon/cs410project/blob/master/searching.gif)

