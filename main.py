import os
import boto3

from somjobs.combine_scraped_jobs import append_all_scraped_jobs, insert_jobs_to_db
from somjobs.db import create_table
from somjobs.run_spiders import run_all_spiders

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')  # crawler.settings['aws_access_key_id']
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

db_local = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
db = boto3.resource('dynamodb',
                    region_name="eu-west-2",
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)


def main():
    run_all_spiders()
    jobs_table = create_table(db=db)
    all_scraped_jobs = append_all_scraped_jobs("scraped_jobs")
    insert_jobs_to_db(table=jobs_table, scraped_jobs=all_scraped_jobs)


if __name__ == "__main__":
    main()
