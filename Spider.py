"""

    Main unit of a crawler which does the actual crawling.
    A spider takes a base_url and crawls it to find outgoing links on that page.
    It removes base_url from the queue, adds it to the crawled list, and adds all the gathered links to the queue.
    It scraps the url, takes out the HTML from the page, hands it over to the LinkDataFinder instance, which
    parses the HTML for links, and data.
    The spider updates the links to be crawled, and the links already crawled.
    The crawling process is fastened by using multiple spiders running simultaneously on different threads

"""

import requests
import threading
from utilities import *
from Link_And_Content_Finder import *
import sys


class Spider:

    """
        Since the queue containing links to be crawled, and links already crawled should be shared by all spiders,
        thus they are declared as class variables or static variables. A lock is also used to prevent multiple threads working
        on the same file in a random manner. The operations on the queue and crawled_links should be atomic.

        @attr:
            domain_name:            stores the domain, used to check whether the url to crawl belongs to that domain or not
            queued_links:           set() of all links yet to be crawled
            crawled_links:          set() of links already crawled
            prefix:                 the top level directory path inside which all files are to be written
            queued_links_filepath:  stores path to the file containing the links yet to be crawled
            crawled_links_filepath: stores path to the file containing the links already crawled
            tLock:                  used to lock the critical section to prevent simultaneous modification of shared resouces

        All methods are static methods

    """

    base_url = ''
    domain_name = ''
    queued_links = None
    crawled_links = None
    queued_links_filepath, crawled_links_filepath = '', ''
    project_name = ''
    prefix = ''
    remove = ''
    tLock = None

    def __init__(self, project_name, base_url, domain_name, remove):
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queued_links = set()
        Spider.crawled_links = set()
        Spider.project_name = project_name
        Spider.queued_links_filepath = project_name + '/config/queue.txt'
        Spider.crawled_links_filepath = project_name + '/config/crawled.txt'
        Spider.prefix = Spider.project_name + '/' + Spider.domain_name
        Spider.remove = remove
        Spider.tLock = threading.Lock()

        #   called for the first Spider which does housekeeping like creating the project dir, creating the config files
        #   and initialising them

        self.initialise_spider()
        self.crawl_page(Spider.base_url)

    @staticmethod
    def initialise_spider():
        create_main_directory(Spider.project_name)
        create_directory(Spider.crawled_links_filepath)
        create_directory(Spider.queued_links_filepath)
        create_file(Spider.queued_links_filepath, Spider.base_url)
        create_file(Spider.crawled_links_filepath)
        Spider.crawled_links = file_to_set(Spider.crawled_links_filepath)
        Spider.queued_links = file_to_set(Spider.queued_links_filepath)

    @staticmethod
    def crawl_page(url_to_crawl):

        """Crawl the site for links and data"""

        print 'crawling:', url_to_crawl

        #   @filename:  name of the file to which the contents of this url is to be written
        #               if the url does not specify resource name like the url ends in '/', it is given a name index.txt

        filename = urlparse.urlparse(url_to_crawl).path
        if filename == '':
            filename += '/index.txt'
        elif filename.endswith('/'):
            filename += 'index.txt'

        if filename.startswith('/'):
            path = Spider.prefix + filename
        else:
            path = Spider.prefix + '/' + filename

        links, data = set(), ''

        if url_to_crawl not in Spider.crawled_links:
            try:
                r = requests.get(url_to_crawl)
                if 'text/html' in r.headers['content-type']:
                    finder = LinkDataFinder(url_to_crawl, Spider.remove)
                    finder.feed(r.content.decode('utf-8'))
                    links = finder.get_links()
                    data = finder.get_data()
            except Exception as e:
                print e
                print "Error"

            """
                Add the new links to queue, add crawled site to crawled_links, remove it from queue
                The shared resources are to be modified so the lock is acquired

            """

            Spider.tLock.acquire()

            #   exception is handled to prevent termination of program due to any unexpected error

            try:
                Spider.queued_links.remove(url_to_crawl)
                Spider.crawled_links.add(url_to_crawl)

                for url in links:
                    if (Spider.base_url in url) and (url not in Spider.queued_links):
                        Spider.queued_links.add(url)

                '''write the data to file'''
                create_directory(path)
                add_content(path, data)

                '''update config files'''

                set_to_file(Spider.queued_links_filepath, Spider.queued_links)
                set_to_file(Spider.crawled_links_filepath, Spider.crawled_links)

            except Exception as e:
                print e

            finally:

                # the lock is released
                Spider.tLock.release()


if __name__ == "__main__":
    input_url = sys.argv[1]
    remove = False
    if len(sys.argv) > 2:
        remove = bool(sys.argv[2])
    print remove
    domain_name = get_domain_name(input_url)

    PROJECT_NAME = domain_name.replace('.', '_')
    Spider(PROJECT_NAME, input_url, domain_name, remove)
