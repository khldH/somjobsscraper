import uuid

import requests


def get_jobs():
    # date = datetime.now().astimezone().replace(hour=0,minute=0, second=0, microsecond=0).isoformat().replace('+',
    # '%2B')
    url = f"https://api.reliefweb.int/v1/jobs?appname=apidoc&filter[field]=country.name&filter[value]=Somalia&limit=1000"
    url += f"&preset=latest&profile=full&fields[include][]"
    try:
        resp = requests.get(url)
        data = resp.json()
        return data
    except Exception as e:
        print(e)


def get_refined_job_list():
    jobs = get_jobs()
    som_jobs = []
    for item in jobs["data"]:
        city = ""
        if "city" in item["fields"].keys():
            city = item["fields"]["city"][0]["name"]
        job = dict(
            id=str(uuid.uuid4()),
            title=item["fields"]["title"],
            category=item["fields"]["career_categories"][0]["name"],
            type=item["fields"]["type"][0]["name"],
            posted_date=item["fields"]["date"]["created"],
            url=item["fields"]["url"],
            location=city + " " + "Somalia",
            organization=item["fields"]["source"][0]["name"],
            source="reliefweb",
        )
        som_jobs.append(job)
    return som_jobs
