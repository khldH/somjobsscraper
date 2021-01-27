class SomJobsPipeline(object):
    def process_item(self, item, spider):
        item['posted_date'] = item['posted_date'].split(":")[1]
        item['expires'] = item['expires'].split(":")[1]
        return item
