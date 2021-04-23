import argparse
import os
import requests
import colorama

from bs4 import BeautifulSoup

colorama.init()

class Browser:

    directory = ''

    stack = []

    @classmethod
    def parsing(cls):
        parser = argparse.ArgumentParser(description='Managing CLI interface')
        parser.add_argument('argument')
        args = parser.parse_args()
        cls.directory = args.argument

    @classmethod
    def makedir(cls):
        if not os.access(cls.directory, os.F_OK):
            os.mkdir(cls.directory)

    def url_modifyer(self, inp):
        if not inp.startswith('https://'):
            inp = 'https://' + inp
        return inp

    def url_confirm(self, url):
        url = self.url_modifyer(url)
        try:
            r = requests.get(url)
            if r:
                return 'ok'
            else:
                return 'error'
        except requests.exceptions.ConnectionError:
            return 'error'

    def file_name(self, inp):
        if inp.startswith('https://'):
            inp = inp[8:]
        if inp.startswith('www.'):
            inp = inp[4:]
        inde = inp[::-1].index('.')
        inp = inp[:len(inp) - inde - 1]
        return inp

    def action(self):
        if Browser.directory == '':
            Browser.parsing()
            Browser.makedir()
        else:
            inp = input()
            if inp == 'exit':
                exit()
            elif inp == 'back':
                if len(Browser.stack) > 1:
                    Browser.stack.pop()
                    file = open(os.path.join(Browser.directory, Browser.stack.pop()), 'r', encoding='utf-8')
                    print(file.read())
                    file.close()
                else:
                    pass
            elif os.access(os.path.join(Browser.directory, inp), os.F_OK):
                file = open(os.path.join(Browser.directory, inp), 'r', encoding='utf-8')
                print(file.read())
                file.close()
                Browser.stack.append(inp)
            elif self.url_confirm(inp) == 'ok':
                inp = self.url_modifyer(inp)
                name = self.file_name(inp)
                r = requests.get(inp)
                soup = BeautifulSoup(r.content, 'html.parser')
                content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
                file = open(os.path.join(Browser.directory, name), 'w', encoding='utf-8')
                text_to_add = ''
                for x in content:
                    if x.name == 'a':
                        text_to_add += colorama.Fore.BLUE + x.get_text().strip() + colorama.Style.RESET_ALL + '\n'
                    else:
                        text_to_add += colorama.Style.RESET_ALL + x.text.strip() + '\n'
                print(text_to_add)
                file.write(text_to_add)
                file.close()
                Browser.stack.append(name)
            else:
                print('Error: Incorrect URL')


start = Browser()

while True:
    start.action()