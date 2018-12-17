from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .storage import upload_file
from .models import Video
from .tasks import parse_video_upload
from .search import search_videos, find_matches_in_string
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_file_upload(request):
    if request.method == 'POST':
            file_obj = request.FILES.get('file')
            file_name, s3_url = upload_file(
                    file_obj,
                    file_obj.name,
                    file_obj.content_type
            )
            video = Video.objects.create(
                url=s3_url
            )
            parse_video_upload.delay(file_name, video.pk)
            return HttpResponseRedirect('/success-upload')
    return HttpResponse("Ok")

class SearchEngineViewSet(viewsets.ViewSet):

    def list(self, request):
        query = request.GET.get('q', None)
        if query is None:
            return Response(dict(errors=['q param is required']), status=400)

        def _format_query_result(result):
            document_data = result.get('_source', {})
            matches = find_matches_in_string(document_data['transcript'], query)
            video = Video.objects.filter(pk=document_data.get('video_id')).first()
            if 'words' in document_data and len(document_data['words']) > 0:
                if len(matches) > 0:
                    length, start, end = matches[0]
                    words = document_data.get('words')
                    if len(words) < end and len(words) > start:
                        document_data['start_match'] = words[start]['start_time']
                        document_data['end_match'] = words[end]['end_time']
                else:
                    document_data['start_match'] = None
                    document_data['end_match'] = None
            del document_data['words']
            return dict(
                score=result.get('_score', 0),
                url=video.url,
                **document_data
            )

        return Response(
            list(map(_format_query_result, search_videos(query))),
            status=200
        )
