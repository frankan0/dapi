import os
import requests
import execjs  # 这个库是PyExecJS
import re
import json

from flask import Flask
from flask import request

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @application.route('/query')
    def query():
        headers={"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "en-us",
    "Connection" : "keep-alive",
    "Accept-Charset" : "GB2312,utf-8;q=0.7,*;q=0.7"}

        title=request.args.get('key', '');

        url = 'https://search.douban.com/book/subject_search?search_text='+title+'&cat=1001';
        response = requests.get(url,headers=headers);
        r = re.search('window.__DATA__ = "([^"]+)"',response.text).group(1)
        jspath=os.path.join(APP_ROOT, 'main.js')
        with open(jspath, 'r', encoding='gbk') as f:
            decrypt_js = f.read()
        ctx = execjs.compile(decrypt_js)
        data = ctx.call('decrypt', r)
        result = json.dumps(data['payload']['items'])
        return result;

    return application