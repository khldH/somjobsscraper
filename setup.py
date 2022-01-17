# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = somjobs.settings']},
)

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
}
DELTAFETCH_ENABLED = True
