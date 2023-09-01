from setuptools import setup

setup(
    name='swan',
    version='0.0.1',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "chardet"
        , "docx"
        , "beautifulsoup4"
        , "hygiene-dm"
        , "matplotlib"
    ],
    package_dir = {
        "config": "swan"
        , "copier": "swan"
        , "fax": "swan"
        , "janitor": "swan"
        , "receipts": "swan"
        , "supplies": "swan"
        , "teacher": "swan"
        , "utils": "swan"
    },
    url = 'https://github.com/DylanAlloy/swan_scrape'
)