import webbrowser
import sys
import os
import re

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def openBrowser(url):
    webbrowser.open_new(url)

def getMemoAndOpenBrowser(text, is_open, current_period):
    if 'url:' in text:
        regex = re.compile(r'url:\[\[(.+?)\]\]')
        urls = regex.findall(text)
        if is_open and current_period == 'yes':
            for url in urls:
                webbrowser.open_new(url)
        text = re.sub(r'url:\[\[(.+?)\]\]', r'<a href="\1">\1</a>', text)
    return text.replace('\n', '<br>')