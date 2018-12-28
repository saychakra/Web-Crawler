import threading
from queue import Queue
from spider import Spider
import domain as dm
import general as gen

project_name = input("Enter the project name: ")
home_page = input("Enter the homepage URL: ")

DOMAIN_NAME = dm.get_domain_name(home_page)
QUEUE_FILE = project_name + '/queue.txt'
CRAWLED_FILE = project_name + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()

# The first spider instance does not need a multithreaded approach. 
# We just need to find generate the first queue of urls from the base_url or the home page.
Spider(project_name, home_page, DOMAIN_NAME)


# Creating Threads (The threads will die after main terminates)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # which suggests that the threads are left as main terminates
        t.start()

# Do the next job in the queue
# Essentially iterate through the queue and take each url and crawl it
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Basically each queued_link is a new job
def create_jobs():
    for link in gen.file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join() # to avoid collision among multiple threads
    crawl()


# iterating through the queue and checking if any urls are left
# if so then crawl them until the whole queue is empty
def crawl():
    queued_links = gen.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()