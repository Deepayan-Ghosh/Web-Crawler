"""

    Main starting point of the crawler
    Uses multithreading to fasten the crawling
    Each thread is a worker, and each url is a job it must complete
    There are two config files:
        1)  <project_dir_name>/config/queue.txt        ---->    stores the urls to be crawled
        2)  <project_dir_name>/config/crawled.txt      ---->    stores the urls that has been crawled

    The urls are taken from the queue.txt config file and put into a thread-safe queue imported from python Queue module
    Each thread upon creation takes an url from the queue and crawls it
    Once the queue is exhausted, it is re-filled again with all the newly found links

"""

import threading
from Queue import Queue
from Spider import Spider
import utilities
import sys


'''
    The input url and the remove flag is given as command line argument
    @:param
        NUMBER_OF_THREADS   --->    number of spiders
        domain_name         --->    domain of the main url to be crawled (e.g:  in docs.python.org, it would be python.org)
        PROJECT_NAME        --->    same as domain name, period(.) replaced with _  (e.g:   python_org)
        QUEUE               --->    the queue configuration file
        remove              --->    a modifier flag which tells the HTMLParser whether it should remove \n,\r,\s from the
                                    scraped data
                                    initialised to FALSE, else provided by user as command-line-arg
        queue               --->    thread safe queue for storing jobs(urls) for each thread
        input_url           --->    url of website to be crawled, provided as command-line-arg

    The config files saves the links to be crawled and the links already in permanent storage allowing the crawler to resume
    crawling from where it left last time. It is a permanent form of the queue set and crawled set.

'''

NUMBER_OF_THREADS = 8
queue = Queue()
input_url = sys.argv[1]
remove = False
if len(sys.argv) > 2:
    remove = bool(sys.argv[2])
domain_name = utilities.get_domain_name(input_url)

PROJECT_NAME = domain_name.replace('.', '_')
QUEUE = PROJECT_NAME + '/config/queue.txt'

'''
    First spider does a lot of house-keeping
    It makes the project directory, config directory and the config files
    It also crawls the base_url and updates the crawled list of urls, and the queued list of urls

'''
Spider(PROJECT_NAME,input_url,domain_name,remove)


def create_threads():
    for _ in xrange(NUMBER_OF_THREADS):
        t = threading.Thread(target=assign_url_to_thread)
        t.daemon = True
        t.start()

'''
    assign_url_to_thread():     assign url to each thread which it should crawl
'''


def assign_url_to_thread():
    while True:
        url = queue.get()
        Spider.crawl_page(url)
        queue.task_done()


'''
    start_crawling():   creates the queue of jobs(urls) from which the spiders(threads) pick up jobs and crawl
                        once empty, it is refilled with the newly discovered to-be-crawled links
'''


def start_crawling():
    q = utilities.file_to_set(QUEUE)
    if len(q) > 0:
        for link in q:
            queue.put(link)
        queue.join()
    start_crawling()


if __name__=="__main__":
    create_threads()
    start_crawling()