# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'bookscraper',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        'bookscraper': ['resources/*.txt']
    },
    entry_points = {'scrapy': ['settings = bookscraper.settings']},
    zip_safe=True,
)
