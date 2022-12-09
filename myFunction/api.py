import urllib3
import json


class API:
    def __init__(self, username, passwrod, baseURL="https://stag-apimgmt.ubank.vn/api/v1/"):
        # self.baseURL = baseURL
        self.http = urllib3.PoolManager()
        self.baseURL = baseURL
        self.data = {'Username': username, 'Password': passwrod}
        self.encoded_data = json.dumps(self.data)
        self.req = self.http.request(
            'POST',
            baseURL + 'auth/token',
            body=self.encoded_data,
            headers={'Content-Type': 'application/json'}
        )
        self.token = json.loads(self.req.data.decode(
            'utf-8')).get('data', '').get('AccessToken', '')

    def customer_retail(self, url, data):
        # print(self.token)
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )
        data = json.loads(req.data.decode('utf-8'))

        return data

    def current_account(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )
        data = json.loads(req.data.decode('utf-8'))

        return data

    def savings_accounts(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def cards_status(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def cards_stop(self, url, data):
        req = self.http.request(
            'POST',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            body=json.dumps(data)
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def cards_activecards(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def deposits_customer(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def loans_CardDtlsInq(self, url, data):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=data
        )

        data = json.loads(req.data.decode('utf-8'))

        return data

    def income_statement(self, url, dataBody, dataParam):
        req = self.http.request(
            'GET',
            self.baseURL + url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            },
            fields=dataParam,
            body=json.dumps(dataBody)
        )

        data = json.loads(req.data.decode('utf-8'))

        return data
