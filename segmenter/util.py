import json
import urllib3
import base64
import boto3
from botocore.exceptions import ClientError
import os
import logging


BUCKET_NAME = "sp4013-test"
s3 = boto3.client('s3')


def download_file(object_name):
    with open('temp.jpg', 'wb') as f:
        s3.download_fileobj(BUCKET_NAME, object_name, f)


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3.upload_file(file_name, BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


TOKEN = "ya29.c.b0AXv0zTOb-qIjXYFZGv-x3tEihPZeP1Rc-hmSjkli3wKuEKz3Vr3vW8Rf5O0FwNGu7fshEHCNYYMa-F1YTPqL-xe6npSOHwXG3qcZQPFEzAGhePUn9jaodyR2zQSFus1REwaRchh547Uj40DZoNqNTPArkXgdWOoB5uKF53Jlbl8wFQ4gYYOc0iyD3Mg9jLimzw7UfAVrdqlUelTNutZaUiC1fG0OAL8........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................"
HEADERS = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + TOKEN}


def convert_b64(img_path):
    with open("temp.jpg", "rb") as imfile:
        b64_str = base64.b64encode(imfile.read())
    return b64_str.decode("utf-8")


def query_vision(img_path):
    payload = {
        "requests": [
            {
                "image": {
                    "content": convert_b64(img_path)
                },
                "features": [
                    {
                        "maxResults": 10,
                        "type": "OBJECT_LOCALIZATION"
                    },
                ]
            }
        ]
    }

    http = urllib3.PoolManager()

    response = http.request('POST',
                            "https://vision.googleapis.com/v1/images:annotate",
                            body=json.dumps(payload),
                            headers=HEADERS,
                            retries=False)

    return response.data.decode('utf-8')
