import os
import boto3
import uuid
from .api_jobs.get_jobs_from_api import get_refined_job_list


class SomJobsPipeline(object):
    _rw_jobs = get_refined_job_list()

    def __init__(self,
                 aws_access_key_id,
                 aws_secret_access_key,
                 region_name,
                 # local_db,
                 table_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.table_name = table_name
        # self.local_db = local_db
        self.table = None

    @classmethod
    def from_crawler(cls, crawler):
        aws_access_key_id = crawler.settings['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = crawler.settings['AWS_SECRET_ACCESS_KEY']
        region_name = crawler.settings['DYNAMODB_PIPELINE_REGION_NAME']
        table_name = crawler.settings['DYNAMODB_PIPELINE_TABLE_NAME']
        # local_db = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        return cls(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            table_name=table_name,
            # local_db=local_db
        )

    def open_spider(self, spider):
        db = boto3.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name, )
        # db = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

        if self.table_name in [table.name for table in db.tables.all()]:
            table = db.Table(self.table_name)
            table.delete()
            table.wait_until_not_exists()
        self.table = db.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

    def close_spider(self, spider):
        for item in self._rw_jobs:
            self.table.put_item(Item=item)
        self.table = None

    def process_item(self, item, spider):
        if item['category'] is None:
            item['category'] = ''
        if item['title'] is None:
            item['title'] = ''
        if item['posted_date'] is None:
            item['posted_date'] = ''
        if item['organization'] is None:
            item['organization'] = ''
        item['title'] = item['url'].split("jobs/")[1].strip('/').replace('-', ' ').title()
        item['id'] = str(uuid.uuid4())
        item['location'] = " ".join(item['title'].split()[-2:])
        item['category'] = item['category'].strip()
        item['type'] = item['type'].strip()
        item['source'] = 'Somali jobs'
        self.table.put_item(Item=item)
        return item
