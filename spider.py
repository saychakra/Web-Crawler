from urllib.request import urlopen
from link_finder import LinkFinder
import general as gen

class Spider:

    # Class variables (shared among all the instances)
    project_name = ''   # will be entered by the user at run time
    base_url = ''       # base url needed to get the full url from relative ones
    domain_name = ''    # for checking whether the domain names are valid or not
    queue_file = ''     # file for storing queue items from the list
    crawled_file = ''   # file for storing crawled items from the list
    queue = set()       # set of all urls in the waiting list
    crawled = set()     # set of all urls in th crawled list


    # method for creating the initial project directory and the data files within
    @staticmethod # because we are only assigning values to class variables a method was not really necessary
    def boot():
        # create the project directory with the name as specified by the user
        gen.create_project_dir(Spider.project_name)

        # create the files within the project directory 
        gen.create_data_files(Spider.project_name, Spider.base_url)
    
        # create the queue set and the crawled set
        Spider.queue = gen.file_to_set(Spider.queue_file)
        Spider.crawled = gen.file_to_set(Spider.crawled_file)


    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            # checking if the urls are not in either of the queue list or the crawler list
            if url in Spider.queue or url in Spider.crawled:
                continue
            # explained in readme
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)


    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            # just check if the page contains html and is not something else eg. a pdf or something
            if response.getheader('Content-Type') == 'text/html': 
                html_bytes = response.read() # reading the raw bytes from response to html_bytes
                html_string = html_bytes.decode('utf-8') # decoding the bytes to utf-8 string format
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print("Error: Cannot Crawl Page")
            return set() # our function needs to return a set from where it is called. 
            # Hence even if anything is not found at least an empty set should be returned
        # finally returning the set of urls from the LinkFinder.page_links()
        return finder.page_links()


    @staticmethod
    def update_files():
        pass


    @staticmethod
    def crawl_page(thread_name, page_url):
        # making sure we haven't already crawled this page already
        if page_url not in Spider.crawled:
            print(thread_name, 'is crawling', page_url)
            print('Queue ' + str(len(Spider.queue)) + '     |       crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            # remove page_url from the queue and add it to the crawled list
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            # update the files in the directory
            Spider.update_files()


    def __init__(self, project_name, base_url, domain_name):
        # assigning the same project_name, base_url and domain_name for all spider instances created 
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name

        # assigning the file paths for queue and crawled files
        Spider.queue_file = project_name + '/queue.txt'
        Spider.crawled_file = project_name + '/crawled.txt'

        self.boot() 
        self.crawl_page('First Spider', Spider.base_url)