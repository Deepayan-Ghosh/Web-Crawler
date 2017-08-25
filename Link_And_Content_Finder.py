"""

    It is a custom HTMLParser, made by inheriting python's HTMLParser.
    It defines what should be done on encountering text-nodes, starting of tags and comments.
    It accepts the scraped HTML from a spider and returns the data to be written to file, and also gathers the links on a page
    The scraped data obtained may contain un-necessary \n's and \r's so it uses regex to remove them, on condition that
    remove flag is set to True by user

"""

import urlparse
import re
from HTMLParser import HTMLParser
from utilities import *

'''
    @:class
    LinkDataUpdater:    subclass of HTMLParser
                        gathers links if the starting tag is anchor-tag and stores them in a set()
                        records the text nodes' contents encountered while parsing

'''


class LinkDataFinder(HTMLParser):
    """
        @:param
            base_url:   the url whose data is to be scraped and whose links are to be gathered
            remove:     flag to indicate whether \n,\r should be removed or not
        @attr:
            links:      set() which stores the gathered links on the base_url
            data:       records the data found on the page
            exceptions: a set which stores the tags whose content is not to be included in the data we want
            start_tag"  keep track of the tag encountered just before encountering text

    """

    def __init__(self, base_url, remove=False):
        HTMLParser.__init__(self)
        self.start_tag = ''
        self.links = set()
        self.base_url = base_url
        self.data = ''
        self.remove = remove
        self.exceptions = set(['img', 'a', 'link', 'meta', 'script', 'style'])

    #   overriden method:   defines what should be done when starting tags are encountered
    #                       here, if start tag is anchor, it gathers the urls in 'href' attribute
    #                       these links are the links yet to crawled

    def handle_starttag(self, tag, attrs):
        self.start_tag = tag
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    url = urlparse.urljoin(self.base_url, value)
                    idx = url.find('#')
                    if idx != -1:
                        url = url[:idx]
                    self.links.add(url)

    # defines what is to be done when text_nodes are encountered in the HTML content

    def handle_data(self, data):
        if self.start_tag not in self.exceptions:
            self.data += data

    # defines what is to be done when comments are encountered in the HTML content

    def handle_comment(self, data):
        self.data += ''

    #   if remove is set to True then removes the unnecessary \n,\r
    def process_data(self):
        if self.remove:
            self.data = re.sub(r'\t+', r'\t', self.data)
            self.data = re.sub(r'(\t\n)+', r'\n', self.data)
            self.data = re.sub(r'(\t\r)+', r'\n', self.data)
            self.data = re.sub(r'\n{2,}', r'\n', self.data)
            self.data = re.sub(r'\s{2,}', r'\n', self.data)
        return self.data

    #   getter functions

    def get_data(self):
        self.data = self.process_data()
        return self.data

    def get_links(self):
        return self.links

    def error(self, message):
        pass
