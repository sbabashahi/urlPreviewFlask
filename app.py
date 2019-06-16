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
            data = {
                'title': get_title(soup),
                'description': get_description(soup),
                'image': get_image(soup),
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


def get_title(soup):
    return soup.title.text if soup.title else ''


def get_description(soup):
    meta_des = soup.find('meta', attrs={'name': 'description'})
    if meta_des:
        meta_des = meta_des['content'] if meta_des.get('content') else ''
    else:
        meta_des = ''
    return meta_des


def get_image(soup):
    meta_img = soup.find('meta', attrs={'property': 'og:image'})
    if meta_img:
        meta_img = meta_img['content'] if meta_img.get('content') else ''
    else:
        meta_img = ''
    return meta_img


if __name__ == '__main__':
    app.run()
