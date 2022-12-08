import boto3


class connectDB:
    def __init__(self, access_key, secret_key, nameTable):
        self.access_key = access_key
        self.secret_key = secret_key
        self.nameTable = nameTable

    def myTable(self):
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key)

        myTable = dynamodb.Table(self.nameTable)
        return myTable
