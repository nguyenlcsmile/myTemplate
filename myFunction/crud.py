import hashlib
import json
import re
from boto3.dynamodb.conditions import Key


class myActions:
    def __init__(self):
        pass

    def check(self, data):
        # Check key
        checkElemetKeys = ['userId', 'email', 'username',
                           'password', 'address', 'phone', 'avatar']
        for element in checkElemetKeys:
            if (element not in data.keys()):
                return {
                    'statusCode': 400,
                    'message': f'{element} is not exists!!!'
                }

        # Check empty
        elementsCheckEmpty = ['userId', 'email', 'phone', 'password']
        for element in elementsCheckEmpty:
            if (data.get(element) == ""):
                return {
                    'statusCode': 400,
                    'message': f'{element} is empty!!!'
                }

        # Check valid email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        checkEmailValid = re.fullmatch(regex, data.get("email"))
        if (not checkEmailValid):
            return {
                'statusCode': 400,
                'message': 'Email is not valid!!!'
            }

    def getAllUsers(self, table):
        res = table.scan()
        return {
            'statusCode': 200,
            'message': 'Get all users success!!!',
            'data': res.get("Items", "Not exists users in table!!!")
        }

    def getUser(self, table, userId):
        res = table.query(
            ExpressionAttributeNames={
                '#id': 'id'
            },
            ExpressionAttributeValues={
                ':id': str(userId)
            },
            KeyConditionExpression='#id = :id'
        )
        if (res.get("Count") != 0):
            return {
                'statusCode': 200,
                'message': 'Get user success',
                'data': res.get("Items", "Something wrong from server!!!")
            }
        else:
            return {
                'statusCode': 400,
                'message': 'UserId is not exists!!!'
            }

    def putUser(self, data, table, actions):
        # list information users
        if (self.check(data)):
            return self.check(data)

        # Check exists
        checkExits = table.query(
            KeyConditionExpression=Key('id').eq(data.get("userId")))
        if (checkExits.get("Count") != 0):
            return {
                'statusCode': 400,
                'message': 'UserId is exists!!!'
            }

        try:
            # TODO: write code...
            urlImage = actions.putImage(
                data.get("avatar", None), data.get("userId") + '.png')

            hashPass = hashlib.sha256(
                data.get("password").encode('utf-8')).hexdigest()

            res = table.put_item(
                Item={
                    'id': data.get("userId"),
                    'username': data.get("username", ""),
                    'email': data.get("email"),
                    'password': hashPass,
                    'address': data.get("address", ""),
                    'phone': data.get("phone", ""),
                    'urlImage': urlImage,
                    'imagebase64': data.get("avatar", "")
                }
            )

            return {
                'statusCode': 200,
                'message': 'Insert user success!!!'
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': 'Something wrong from server!!!'
            }

    def updateUser(self, data, table, actions):
        if (self.check(data)):
            return self.check(data)

        # Check exists
        checkExits = table.query(
            KeyConditionExpression=Key('id').eq(data.get("userId")))
        if (checkExits.get("Count") != 0):
            try:
                # TODO: write code...
                hashPass = hashlib.sha256(
                    data.get("password").encode('utf-8')).hexdigest()

                urlImage = actions.putImage(
                    data.get("avatar", None), data.get("userId") + '.png')

                res = table.update_item(
                    Key={
                        'id': data.get("userId")
                    },
                    ExpressionAttributeNames={
                        '#username': 'username',
                        '#email': 'email',
                        '#password': 'password',
                        '#address': 'address',
                        '#phone': 'phone',
                        '#urlImage': 'urlImage',
                        '#imagebase64': 'imagebase64'
                    },
                    ExpressionAttributeValues={
                        ':username': data.get("username", ""),
                        ':email': data.get("email"),
                        ':password': hashPass,
                        ':address': data.get("address", ""),
                        ':phone': data.get("phone", ""),
                        ':urlImage': urlImage,
                        ':imagebase64': data.get("avatar", "")
                    },
                    UpdateExpression='SET #username = :username, #email = :email,' +
                    '#password = :password, #address = :address,' +
                    '#phone = :phone, #urlImage = :urlImage, #imagebase64 = :imagebase64',
                    ReturnValues='ALL_NEW',
                )

                return {
                    'statusCode': 200,
                    'body': 'Update user success!!!'
                }

            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': 'Somthing wrong from server!!!'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'User is not exists!!!'
            }

    def deleteUser(self, data, table, actions):
        checkUser = table.query(
            KeyConditionExpression=Key('id').eq(data.get("userId")))

        if (checkUser.get("Count") != 0):
            res = table.delete_item(
                Key={
                    'id': data.get("userId")
                }
            )

            actions.deleteImage(data.get("userId") + '.png')

            return {
                'statusCode': 200,
                'message': 'Delete user success!!!'
            }
        else:
            return {
                'statusCode': 400,
                'message': 'Not exits user!!!'
            }

    def error(self):
        return {
            'statusCode': 400,
            'message': 'Somthing wrong from client!!!'
        }

    # def deleteAllUser(self, data, table, actions):
    #     listUsers = data['users']

    #     for user in listUsers:
    #         checkUserExist = table.get_item(
    #             Key = {
    #                 'id': str(user['id']),
    #             }
    #         )

    #         if ('Item' in checkUserExist.keys()):
    #             resS3 = actions.deleteImage(user['id'] + '.png')

    #             res = table.delete_item(
    #                 Key = {
    #                     'id': str(user['id'])
    #                 }
    #             )

    #             return {
    #                 'statusCode': 200,
    #                 'body': json.dumps('Delete user success!!!')
    #             }
    #         else:
    #             return {
    #                 'statusCode': 200,
    #                 'body': json.dumps('Not exists user!!!')
    #             }
