import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def link_preview():
    url = request.args.get('url')
    if url:
        if '//' not in url:
            url = 'http://' + url
        try:
            resp = requests.get(url)
        except Exception as e:
            return ErrorResponse(error=str(e), message='Error in connecting to url', ).send()
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, features='html.parser')
            data = {
                'title': get_title(soup),
                'site_name': get_site_name(soup),
                'favicon': get_favicon(soup, url),
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


def get_site_name(soup):
    meta_site_name = soup.find('meta', attrs={'property': 'og:site_name'})
    if meta_site_name and meta_site_name.get('content'):
        meta_site_name = meta_site_name.get('content')
    else:
        meta_site_name = ''
    return meta_site_name


def get_favicon(soup, url):
    meta_favicon = soup.find('link', attrs={'rel': 'icon'})
    if meta_favicon and meta_favicon.get('href'):
        meta_favicon = meta_favicon.get('href')
        if meta_favicon.startswith('/'):
            meta_favicon = '/'.join(url.split('/')[:3]) + meta_favicon
    else:
        meta_favicon = ''
    return meta_favicon


if __name__ == '__main__':
    app.run()
