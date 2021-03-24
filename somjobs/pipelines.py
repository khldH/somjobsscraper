import urllib
import requests
from datetime import datetime
from transformers import pipeline


class SomJobsPipeline(object):
    key = '58f9f7655ba7c89e1f0c4ded45d3511802dc8'
    nlp = pipeline('ner', grouped_entities=True)

    def process_item(self, item, spider):
        url = urllib.parse.quote(item['link'])
        req = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(self.key, url))
        req = req.json()
        location = []
        entities = self.nlp(item['title'].title())
        for entity in entities:
            if 'LOC' in entity.values():
                location.append(entity['word'])
            item['job_location'] = location

        item['posted_date'] = datetime.strptime(item['posted_date'].split(":")[1].strip(), '%d %b %Y').date()
        item['expires'] = item['expires'].split(":")[1]
        item['short_url'] = req['url']['shortLink']
        return item
