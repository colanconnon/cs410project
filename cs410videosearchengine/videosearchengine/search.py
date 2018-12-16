from difflib import SequenceMatcher
from elasticsearch import Elasticsearch
import string

INDEX = 'video-search'
DOC_TYPE = 'video'

es = Elasticsearch(['elasticsearch:9200'])


def index_video(body):
    es.index(index=INDEX, doc_type=DOC_TYPE, body=body)
    es.indices.refresh(index=INDEX)


def delete_index():
    es.indices.delete(index=INDEX, ignore=[400, 404])


def search_videos(query):
    es_query = {
        'query': {
             'multi_match': {
                 'query': query,
                 'fields': ['transcript']
             },
        },
        'highlight': {
            'fields': {
                'text': {'type': 'plain',
                         'number_of_fragments': 3,
                         'fragment_size': 30
                         }
            }
        }
    }
    search_res = es.search(index=INDEX, body=es_query)
    print(search_res)
    return search_res['hits']['hits']


def find_matches_in_string(haystack, needle):
    needle = needle.lower()
    haystack = haystack.lower()
    from spacy.matcher import PhraseMatcher
    from spacy.lang.en import English
    nlp = English()
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('query', None, nlp(needle))
    doc = nlp(haystack)
    matches = matcher(doc)
    return matches