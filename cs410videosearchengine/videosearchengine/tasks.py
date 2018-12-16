from .video_transcode import transcode_aws
from .search import index_video
from celery.decorators import task
from .models import Video
from .text_processing import process_text_to_get_topics, summarize_video_text


@task()
def parse_video_upload(s3_file_name, video_id):
    video_result = transcode_aws(s3_file_name)
    topics = process_text_to_get_topics(video_result['transcript'])
    document_data = dict(
        topics=topics,
        video_id=video_id,
        summary=summarize_video_text(video_result['transcript']),
        transcript=video_result.get('transcript', ''),
        words=video_result.get('words', [])
    )
    index_video(document_data)
