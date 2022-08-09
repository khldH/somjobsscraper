import uuid
from datetime import datetime, timedelta
from scrapy.exceptions import DropItem


class SomJobsPipeline(object):
    def process_item(self, item, spider):
        item["url"] = "https://somalijobs.com" + item["url"]
        item["category"] = item["category"].split("\n")[2].strip()
        item["type"] = item["type"].split("\n")[2].strip()
        item["location"] = item["location"].split("\n")[2].strip()
        # if item['category'] is None:
        #     item['category'] = ''
        # if item['title'] is None:
        #     item['title'] = ''
        # if item['posted_date'] is None:
        #     item['posted_date'] = ''
        # if item['organization'] is None:
        #     item['organization'] = ''
        # item['title'] = item['url'].split("jobs/")[1].strip('/').replace('-', ' ').title()
        item["id"] = str(uuid.uuid4())

        item["source"] = "Somalijobs"

        return item


class UNJobsPipeline(object):
    def process_item(self, item, spider):
        if item["title"] is None:
            raise DropItem("Invalid job")

        else:

            if "about" in item["posted_date"]:
                item["posted_date"] = datetime.utcnow().isoformat()
            elif item["posted_date"] == "a day ago":
                item["posted_date"] = (
                    datetime.utcnow() - timedelta(days=1)
                ).isoformat()
            elif item["posted_date"] is not None:
                item["posted_date"] = (
                    datetime.utcnow()
                    - timedelta(int(item["posted_date"].split(" ")[0]))
                ).isoformat()
            else:
                item["posted_date"] = item["posted_date"]
            item["location"] = item["title"].split(",")[1].strip()
            item["id"] = str(uuid.uuid4())
            item["source"] = "UNjobs"
            return item


class ImpactpoolJobsPipeline(object):
    def process_item(self, item, spider):
        item["url"] = "https://impactpool.org" + item["url"]
        item["organization"] = (
            item["organization"].split("</h3>")[1].split("\n")[1].strip()
        )
        item["location"] = (
            item["location"]
            .split('<i class="icon fa fa-map-marker"></i>')[1]
            .split("\n")[1]
            .strip()
        )
        if item["posted_date"] == "New":
            item["posted_date"] = (datetime.utcnow() - timedelta(days=1)).isoformat()
        else:
            item["posted_date"] = (datetime.utcnow() - timedelta(days=10)).isoformat()
        item["id"] = str(uuid.uuid4())
        item["source"] = "Impactpool"
        return item
