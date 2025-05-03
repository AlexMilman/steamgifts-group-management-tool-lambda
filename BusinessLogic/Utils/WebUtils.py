import gzip
import traceback
from io import StringIO, BytesIO
import http.client as httplib
import time
import urllib.request
import ssl

# from lxml import html
from bs4 import BeautifulSoup
from BusinessLogic.Utils import LogUtils

# WebUtils module responsible for web page downloads, and xpath traversal
# Copyright (C) 2017  Alex Milman


def get_items_by_xpath(data, xpath_param, default=None):
    xpath_value = data.xpath(xpath_param)
    if xpath_value is not None:
        return xpath_value
    return default


def get_item_by_xpath(data, xpath_param, default=None):
    xpath_value = data.xpath(xpath_param)
    if isinstance(xpath_value, list):
        if len(xpath_value) > 0:
            return xpath_value[0]
        else:
            return default
    else:
        return xpath_value.extract()


def get_html_page(page_url, cookies=None, retries=3, https=False, delay=0):
    while retries > 0:
        try:
            if https:
                return BeautifulSoup(get_https_page_content(page_url), "html.parser")
                # return html.fromstring(get_https_page_content(page_url))
            else:
                return BeautifulSoup(get_page_content(page_url, cookies, delay), "html.parser")
                # return html.fromstring(get_page_content(page_url, cookies, delay))
        except Exception as e:
            if retries > 0:
                LogUtils.log_error('Error downloading page ' + page_url + '. ' + str(retries) + ' retries left. retyring...')
            else:
                LogUtils.log_error('Error downloading page ' + page_url + '. now more retries left. stopping... Reason: ' + str(e))
                traceback.print_exc()
            time.sleep(0.1)
            retries -= 1

    return None


def get_page_content(page_url, cookies=None, delay=0):
    time.sleep(delay)
    if isinstance(page_url, str):
        page_url = page_url.encode('utf-8').decode('utf-8')  # ensure it's a str, not bytes
    content = b''

    request = urllib.request.Request(page_url)
    if cookies:
        request.add_header('Cookie', cookies)
    request.add_header('Accept-encoding', 'gzip')

    opener = urllib.request.build_opener()
    response = opener.open(request)

    try:
        data = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            buffer = BytesIO(data)
            with gzip.GzipFile(fileobj=buffer) as zipped_file:
                data = zipped_file.read()
        content += data
    except httplib.IncompleteRead as e:
        content += e.partial

    return content.decode('utf-8', errors='replace')  # decode bytes to str safely


def get_https_page_content(page_url, unverified=False):
    if unverified and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

    if isinstance(page_url, str):
        page_url = page_url.encode('utf-8').decode('utf-8')

    content = b''
    request = urllib.request.Request(page_url, headers={'User-Agent': "Magic Browser"})

    try:
        response = urllib.request.urlopen(request)
        content = response.read()
    except httplib.IncompleteRead as e:
        content = e.partial

    return content.decode('utf-8', errors='replace')

