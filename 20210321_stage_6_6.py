import argparse
import os
import requests
import colorama

from bs4 import BeautifulSoup

colorama.init()

class Browser():

    directory = ''

    stack = []

    def parsing(self):
        parser = argparse.ArgumentParser(description='Managing CLI interface')
        parser.add_argument('argument')
        args = parser.parse_args()
        self.directory = args.argument

    def makedir(self):
        if not os.access(self.directory, os.F_OK):
            os.mkdir(self.directory)

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
        inp = inp.lstrip('https://')
        inde = inp[::-1].index('.')
        inp = inp[:len(inp) - inde]

        return inp

    def action(self):
        if self.directory == '':
            self.parsing()
            self.makedir()
        else:
            inp = input()
            if inp == 'exit':
                exit()
            elif inp == 'back':
                if len(self.stack) > 1:
                    self.stack.pop()
                    file = open(os.path.join(self.directory, self.stack.pop()), 'r', encoding='utf-8')
                    print(file.read())
                    file.close()
                else:
                    pass
            elif os.access(os.path.join(self.directory, inp), os.F_OK):
                file = open(os.path.join(self.directory, inp), 'r', encoding='utf-8')
                print(file.read())
                file.close()
                self.stack.append(inp)
            elif self.url_confirm(inp) == 'ok':
                inp = self.url_modifyer(inp)
                name = self.file_name(inp)
                r = requests.get(inp)
                soup = BeautifulSoup(r.content, 'html.parser')
                param = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
                content = soup.find_all(param)
                file = open(os.path.join(self.directory, name), 'w', encoding='utf-8')
                text_to_add = ''
                for x in content:
                    if x.name == 'a':
                        text_to_add += colorama.Fore.BLUE + x.get_text() + '\n'
                    else:
                        text_to_add += colorama.Style.RESET_ALL + x.text + '\n'
                print(text_to_add)
                file.write(text_to_add)
                file.close()
                self.stack.append(name)
            else:
                print('Error: Incorrect URL')


start = Browser()

while True:
    start.action()
