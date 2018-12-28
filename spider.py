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


    def crawl_page(self):
        pass

    def __init__(self, project_name, base_url, domain_name):
        # assigning the same project_name, base_url and domain_name for all spider instances created 
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name

        # assigning the file paths for queue and crawled files
        Spider.queue_file = project_name + '/queue.txt'
        Spider.crawled_file = project_name + '/crawled.txt'

        self.boot() 
        # self.crawl_page('First Spider', Spider.base_url)