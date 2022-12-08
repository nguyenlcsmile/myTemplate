import json


def index(event, context):

    return {
        'statuscode': 200,
        'body': json.dumps('Hello HiHi!!!')
    }
