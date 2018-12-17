from nltk.corpus import stopwords
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from summa import summarizer


def remove_stop_words(text):
    word_list = word_tokenize(text)
    word_list = [word for word in word_list
                 if word not in stopwords.words('english')]
    return word_list


def find_topics(text):
    # https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
    tf_vectorizer = CountVectorizer(stop_words='english')
    tf = tf_vectorizer.fit_transform(text)
    lda = LatentDirichletAllocation(
        n_components=1,
        learning_method='online',
        learning_offset=50.,
    )
    lda.fit(tf)
    return extract_top_words(lda, tf_vectorizer.get_feature_names(), 8)


def extract_top_words(model, feature_names, n_top_words):
    return [feature_names[i] for topic in model.components_
            for i in topic.argsort()[:-n_top_words - 1:-1]]


def process_text_to_get_topics(text):
    parsed_text = remove_stop_words(text)
    return find_topics(parsed_text)


def summarize_video_text(video_text):
    return summarizer.summarize(video_text, words=100)
