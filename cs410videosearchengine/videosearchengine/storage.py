import datetime
import six
import boto3
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, ['mp4'])
    filename = _safe_filename(filename)

    session = boto3.Session()
    s3 = session.resource('s3')
    bucket_name = 'cconnon-410-videos'
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(
        Body=file_stream,
        Key=filename,
        ACL='public-read',
        StorageClass='REDUCED_REDUNDANCY',
        ContentType='video/mp4'
    )

    return filename, 'https://s3.amazonaws.com/{}/{}'.format(bucket_name, filename)
