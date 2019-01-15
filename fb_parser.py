from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import io
import shutil
import json
import re
import argparse
import csv
import sys

PAGES_REACTION_URL = 'https://www.facebook.com/pages_reaction_units'
POSTS_URL_REGEX = re.compile('https://www.facebook.com/.+?/posts')


def read_content(record):
    output = io.BytesIO()
    shutil.copyfileobj(record.content_stream(), output)
    return output.getvalue().decode('utf-8')


def json_str_generator(json_obj):
    iter_obj = None
    if isinstance(json_obj, list):
        iter_obj = json_obj
    elif isinstance(json_obj, dict):
        iter_obj = json_obj.values()

    if iter_obj:
        for child_obj in iter_obj:
            for yield_obj in json_str_generator(child_obj):
                yield yield_obj
    else:
        yield str(json_obj)


def process_html(html_str):
    post_details = set()
    html = BeautifulSoup(html_str, features='html.parser')
    for userContentWrapperDiv in html.find_all('div', class_='userContentWrapper'):
        timestamp_content_div = userContentWrapperDiv.find('span', class_='timestampContent')
        timestamp = None
        if timestamp_content_div:
            timestamp = timestamp_content_div.get_text()
        user_content = userContentWrapperDiv.find('div', class_='userContent')
        if user_content:
            post = user_content.get_text()
            post_details.add((timestamp, post))
    return post_details


def is_html(html_str):
    return html_str.startswith('<div')


def process_pages_reaction_record(record):
    xhr = json.loads(read_content(record).replace('for (;;);', ''))
    for str_obj in json_str_generator(xhr):
        if is_html(str_obj):
            return process_html(str_obj)


def process_posts_record(record):
    pagelets = read_content(record).rstrip().split('/*<!-- fetch-stream -->*/')
    for pagelet in pagelets:
        if pagelet:
            parsed_pagelet = json.loads(pagelet)
            for str_obj in json_str_generator(parsed_pagelet):
                if is_html(str_obj):
                    return process_html(str_obj)


def process_warc(filepath):
    post_details = set()
    with open(filepath, 'rb') as stream:
        for record in ArchiveIterator(stream):
            url = record.rec_headers.get_header('WARC-Target-URI')
            if record.rec_type == 'response':
                if url.startswith(PAGES_REACTION_URL):
                    post_details.update(process_pages_reaction_record(record))
                elif re.match(POSTS_URL_REGEX, url):
                    post_details.update(process_posts_record(record))
    return post_details


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extract Facebook posts from WARCs.')
    parser.add_argument('filepath', help='Filepath of WARC file')

    args = parser.parse_args()
    m_post_details = process_warc(args.filepath)
    post_writer = csv.writer(sys.stdout)
    for post_detail in m_post_details:
        post_writer.writerow(post_detail)
