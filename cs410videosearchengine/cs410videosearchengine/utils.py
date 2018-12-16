import io
import os
from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio(file_name):
    client = speech.SpeechClient()
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    response = client.recognize(config, audio)
    return response.results
