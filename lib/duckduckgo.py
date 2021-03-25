import requests
from lxml import html
import time
class Duckduckgo():   
    def search(self, query, pages=10, proxy=None, max_results=None):
        url = 'https://duckduckgo.com/html/'
        params = {
            'q': query,
            's': '0',
        }

        yielded = 0
        while True:
            res = requests.post(url, data=params)
            doc = html.fromstring(res.text)

            results = [a.get('href') for a in doc.cssselect('#links .links_main a')]
            print(results)
            for result in results:
                yield result
                time.sleep(0.1)
                yielded += 1
                if max_results and yielded >= max_results:
                    return
            try:
                form = doc.cssselect('.results_links_more form')[-1]
            except IndexError:
                return
            params = dict(form.fields)
            print(params)