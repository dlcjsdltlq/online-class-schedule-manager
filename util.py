import webbrowser
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def openBrowser(url):
    webbrowser.open_new(url)

def getMemoAndOpenBrowser(text, is_open, current_period):
    if 'url:' in text:
        text = text.replace('url:[[', '|||||').replace(']]', '|||||').split('|||||')
        if is_open and current_period == 'yes':
            webbrowser.open_new(text[1])
        new_text = ''
        for txt in text:
            if txt.startswith('http'):
                txt = '<a href="{0}">{0}</a>'.format(txt)
            new_text += txt + '<br>'
        return ''.join(new_text)
    return text.replace('\n', '<br>')