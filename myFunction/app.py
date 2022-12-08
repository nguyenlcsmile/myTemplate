import json
from db import connectDB


def index(event, context):
    db = connectDB('AKIAQKOY52DIAY5KA76N',
                   '+W9hRTcItgu9ACqKsRFshwR9tgnxRQWdqf+JDJep', 'myTable')
    myTable = db.myTable()
    print(myTable)

    return {
        'statuscode': 200,
        'body': json.dumps('Hello HiHi!!!')
    }
