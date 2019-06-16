import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def link_preview():
    url = request.args.get('url')
    if url:
        if not url.startswith('http'):
            url = 'http://' + url

        resp = requests.get(url)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content)
            meta_des = soup.find('meta', attrs={'name': 'description'})
            data = {
                'title': soup.title.text if soup.title else '',
                'description': meta_des['content'] if meta_des.get('content') else ''
            }
            return SuccessResponse(data).send()
        else:
            return ErrorResponse(error='Error in getting resource.').send()
    else:
        return ErrorResponse(error='No url detected').send()


class SuccessResponse:
    def __init__(self, data=None, message='', status=200):
        if data is None:
            data = {}
        self.data = data
        self.message = message
        self.status = status

    def send(self):
        return jsonify(self.__dict__)


class ErrorResponse:
    def __init__(self, error='', message='', status=400):
        self.error = error
        self.message = message
        self.status = status

    def send(self):
        return jsonify(self.__dict__)


if __name__ == '__main__':
    app.run()
