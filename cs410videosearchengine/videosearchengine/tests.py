from django.test import TestCase
from videosearchengine.text_processing import (
    remove_stop_words, find_topics, summarize_video_text)
from .search import (index_video, search_videos)
from .video_transcode import _adapt_response


class TextProcessingTest(TestCase):

    def test_it_removes_stop_words(self):
        text = "this is a test hello"
        filtered_list = remove_stop_words(text)
        self.assertEqual(filtered_list, ["test", "hello"])

    def test_it_will_cluster_lda(self):
        text = """
         I will go to the store tonight and buy groceries and supplies
        """
        text = remove_stop_words(text)
        topics = find_topics(text)
        self.assertEqual(len(topics), 5)

    def test_it_will_summarize_text(self):
        text = """
        This is the greatest text in the world.
        Tribute.
        Couldn't remember the greatest text in the world.
        Tribute to the greatest text in the world.
        This is just a tribute.
        """
        result = summarize_video_text(text)
        assert result is not None


class TestElasticSearch(TestCase):

    def test_it_will_add_index_and_search(self):
        text = """Hello world this is some test text
          what the text test and some more test text
          lorem ipsum del more lorem"""
        video = {
            "transcript": text,
            "words": [],
            "topics": "hello world",
        }
        index_video(video)
        search_results = search_videos('Hello world')
        self.assertEqual(len(search_results) > 1, True)


class TextVideoTranscode(TestCase):

    def test_it_will_adapt_transcribe_response(self):
        results = {
            "transcripts": [
            {
                "transcript": "It was",
            }],
            "items": [
            {
                "start_time": "5.08",
                "end_time": "5.21",
                "alternatives": [{"confidence": "0.9986", "content": "It"}],
                "type": "pronunciation"
            },
            {
                "start_time": "5.21",
                "end_time": "5.35",
                "alternatives": [{"confidence": "1.0000", "content": "was"}],
                "type": "pronunciation"
            },
            ]
        }
        response = _adapt_response(results)
        self.assertEqual(response['transcript'], 'It was')
        self.assertEqual(len(response['words']), 2)
