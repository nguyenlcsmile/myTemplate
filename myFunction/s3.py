import boto3
import base64
import io
import json
import csv
from io import BytesIO, StringIO


class myBucket:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket = bucket

    def connectS3(self):
        s3 = boto3.client(
            service_name='s3',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        return s3

    def loadImage(self, imagebase64):
        imgdata = base64.b64decode(str(imagebase64))
        return io.BytesIO(imgdata)

    def putImage(self, imagebase64, key):
        if (imagebase64 is None):
            return ""

        res = self.connectS3().put_object(
            Body=self.loadImage(imagebase64),
            Bucket=self.bucket,
            ContentType='image/png',
            Key=key
        )

        url = '{}/{}/{}'.format(self.connectS3().meta.endpoint_url,
                                self.bucket, key)

        return url

    def deleteImage(self, key):
        res = self.connectS3().delete_object(
            Bucket=self.bucket,
            Key=key,
        )
        return res

    def getImage(self, key):
        res = self.connectS3().get_object(
            Bucket=self.bucket,
            Key=key
        )
        imgContent = res['Body'].read()
        imgBase64 = base64.b64encode(imgContent)

        return imgBase64.decode('utf-8')

    def getDataFile(self, key):
        res = self.connectS3().get_object(
            Bucket=self.bucket,
            Key=key
        )

        body = res.get('Body', '').read()
        content = body.decode("windows-1252")
        file = StringIO(content)
        csv_data = list(csv.reader(file))

        return csv_data[:10]

    def putObject(self, obj):
        return
