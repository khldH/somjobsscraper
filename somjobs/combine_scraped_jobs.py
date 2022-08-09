import json
from pathlib import Path
import time

from somjobs.api_jobs.get_jobs_from_api import get_refined_job_list


def append_all_scraped_jobs(files_dir):
    try:
        print("getting reliefweb jobs")
        jobs = get_refined_job_list()
        print("reading all scraped files")
        all_files = [path for path in Path(files_dir).rglob("*.json")]
        for file in all_files:
            # print(file)
            with open(file) as f:
                data = json.load(f)
                jobs.extend(data)
        return jobs
    except Exception as e:
        print(e)


def insert_jobs_to_db(table, scraped_jobs):
    try:
        print("total scraped jobs :", len(scraped_jobs))
        print("writing all jobs to db")
        time.sleep(10)
        with table.batch_writer() as batch:
            for job in scraped_jobs:
                batch.put_item(Item=job)
    except Exception as e:
        print(e)
