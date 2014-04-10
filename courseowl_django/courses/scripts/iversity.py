from courses.models import *
import urllib2
from bs4 import BeautifulSoup
import re


def run():
    print("Adding courses from iVersity (this will take a minute)...")
    scrape()


def scrape():
    iversity_web = BeautifulSoup(urllib2.urlopen('https://iversity.org/courses').read())
