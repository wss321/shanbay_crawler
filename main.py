# -*-coding:utf-8-*-

import requests
import lxml.html
from pandas import DataFrame
import argparse
#
# book = 'https://www.shanbay.com/wordbook/205946/' 核心词汇
# """https://www.shanbay.com/wordbook/3/"""


def parse_args():
    parser = argparse.ArgumentParser(description="crawl shanbay")
    parser.add_argument("--u", help="vocabulary book url", type=str)
    parser.add_argument("--o", help="output directory", default="", type=str)
    parser.add_argument("--m", help="add meanings", default=True, type=bool)
    args = parser.parse_args()
    return args


def get_book_unit(book):
    html = requests.get(book).text
    selector = lxml.html.fromstring(html)
    wordlist = selector.xpath('//td[@class="wordbook-wordlist-name"]/a/@href')
    wordlist_name = selector.xpath('//td[@class="wordbook-wordlist-name"]/a/text()')
    book_name = selector.xpath('//div[@class="wordbook-title"]/a/text()')[0]
    for ids, wl in enumerate(wordlist):
        wordlist[ids] = 'https://www.shanbay.com' + wl
    return book_name, wordlist, wordlist_name


if __name__ == '__main__':
    args = parse_args()
    book_name, urls, wordlist_name = get_book_unit(args.u)

    save_file = args.o + '/{}.csv'.format(book_name)
    for idx, each in enumerate(urls):
        with open(save_file, 'a', encoding='utf_8_sig') as f:
            f.write('# ' + wordlist_name[idx] + '\n')
        for i in range(10):
            url = each + '/?page={}'.format(i + 1)
            html = requests.get(url).text
            selector = lxml.html.fromstring(html)

            wordDict = {}
            meanings = selector.xpath('//tbody/tr[@class="row"]/td[@class="span10"]/text()')
            # meanings = [m.replace('\n', ' ') for m in meanings]
            words = selector.xpath('//tbody/tr[@class="row"]/td[@class="span2"]/strong/text()')
            if len(words) > 0:
                wordDict['words'] = words
                if args.m:
                    wordDict['meanings'] = meanings
                df = DataFrame(wordDict, index=None, columns=None)
                df.to_csv(save_file, mode='a', index=False, header=False, encoding='utf_8_sig')
        # with open(save_file, 'a', encoding='utf_8_sig') as f:
        #     f.write('\n\n')

    print('Done. Saved to {}'.format(save_file))
