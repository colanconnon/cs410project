import json
import logging
import time
import boto3
import uuid
import requests

logger = logging.getLogger(__name__)



def transcode_aws(s3_file_name):
    transcribe = boto3.client('transcribe')
    job_name = str(uuid.uuid4())
    job_uri = "https://s3-us-east-1.amazonaws.com/cconnon-410-videos/{}".format(
        s3_file_name
    )
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='en-US'
    )
    status = _wait_until_complete(transcribe, job_name)
    if 'TranscriptionJobStatus' not in status['TranscriptionJob']:
        raise Exception("Bad Response status from aws... {}".format(
            str(status)
        ))
    if status['TranscriptionJob']['TranscriptionJobStatus'] != 'COMPLETED':
        raise Exception("Status from transcription job was not completed: {}".format(
            str(status)
        ))
    results = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri']).json()['results']
    return _adapt_response(results)

def _adapt_response(results):
    transcription_response = dict(
        transcript='',
        words=[]
    )
    for transcript in results['transcripts']:
        transcription_response['transcript'] += transcript['transcript']
    transcription_response['words'] += [_adapt_word(word) 
                                        for word in results['items']
                                        if 'type' in word and word['type'] != 'punctuation']
    return transcription_response

def _wait_until_complete(transcribe, job_name):
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            return status
        time.sleep(5)

def _adapt_word(word):
    return dict(
        start_time=word.get('start_time', None),
        end_time=word.get('end_time', None),
        word=word['alternatives'][0].get('content', '') if len(word['alternatives']) > 0 else '',
    )