import json


def index(event, context):
    print("asdakjsdakjsdad")
    return {
        'statuscode': 200,
        'body': json.dumps('Hello HiHi!!!')
    }
