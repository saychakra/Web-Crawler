# Web-Crawler
### Introduction
This is a basic web crawler. In the subsequent phases I am gonna try and report each and every thing I
learnt, read and implemented in making this project. Let's Begin!!!

<br>

IMPORTANT: Please use python 3.x if you want to test. Queues are not available in 2.x. Refer to the 'requirements.txt' file for more details.

<br>
Well in the first phase, the basic functions for creating a project and a subsequent project directory is 
done (pretty intuitive). In the next phase, a few house-keeping directory manipulation functions are written.

<br>

#### Main Sketch of the Method:
Well, what I'll be trying to do here, is:
   1. Parse the required HTML page and find all the texts/strings which match a typicaly "URL" pattern.
   2. The first set of URLs are put in a file called "queue.txt".
   3. Thereby, the contents of the queue are pulled out
      - They are put in a set and the whole process is repeated till there are no more URLs to be found.
      - Each of the crawled URLs which belong to the same domain name are put in a final file, "crawled.txt" (which is the final output)
   4. Finally, the process is sped up using multithreading.

<br>

#### Speeding up the process
In general, as far as computational time is concerned, writing into a file takes a considerably good amount of time. In general, when we are trying to crawl over a huge page, this can come into as a difficulty and then my friend, you can observe the noticable time lag! 
So to solve this problem, one approach is to use variables. But again, those are temporary solutions. Thus, as a final solutions we can use the best feature of both by using a set.
<br>
So, essentially what we are doing here is that, say we have about 30 urls in our waiting list (queue), which are needed to be crawled. Instead of reading and writing contents from the file (queue.txt) every time, we use a set. We convert the elements of the file (each line in this case) into set items and access them through the set (which should be a lot more faster)

<br>

#### Getting Links
Here comes the reason why I say, Python is the greatest language in the world right now!
We need to parse the html and find the links in each page. Python comes with a built-in HTMLParser class which has all the features necessary to implement the same.
<br>
Understanding the class:
<br>
Say we have some url like this:
```HTML
<a href="https://en.wikipedia.org/wiki/Alan_Turing" class="something"> Link </a>
   /|\                    /|\
    |                      |
    |                      |
    |                      |
"attributes"            "value"
```

<br>

What we need to do is that parse through such a tag where it begins with 'a' and extract only the 'href' attribute's value. 

<br>

NOTE: The thing to remember here is that whenever we have a relative url, that is not gonna work in case of a crawler. Explicitly speaking, say we have a base url as "https://wikipedia.org" and a page under the base domain as "https://en.wikipedia.org/wiki/Alan_Turing", in this case, even "/sayan" should work when we are on the design (HTML) page. But such a relative url is actually useless in case of a crawler as it would make no sense whatsoever!

<br>

Luckily we have the base url already extracted and stored. We just need to join the subsequent url with the base and make it the final url. The code snippet below essentially does the said:

```python
def handle_starttag(self, tag, attr):
        if tag == 'a':
            for (attribute, value) in attr:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
```

### Implementing the Spider/Bot (I'm calling it a 'Spider' here)
#### What will it do?
Well, the main spider is considered as the main heart of the web crawler. The spider is responsible for connecting to the consequent pages and crawl through them in order. 

<br>

- The way this will work is that, we have a waiting list containing a bunch of urls.
- The spider grabs the first urls from the waiting list and connects to it and grab all of its HTML.
- It then calls in the link_finder program.
- The link finder will do its thing parse through the HTML and return the set of urls
- Once the spider spider has all the urls or links, it is going to add them to the waiting list.
- Another thing which it is going to do, is move the crawled pages from the waitng list to the crawled list. That way, we make sure we do not crawl the same page twice.


<br>

### Final Design Approach

#### A slight problem!

Another this to note here is that, say we have a spider and its corresponding crawler and queue. A single spider would be an exceptionally slow and useless process (Image Google running a single spider!). All in all, its useless. So what we can do is replicate the spiders. But in doing so, we will also end up replicating their queues and crawlers. Having multiple disconnected queues and crawlers for every other spider is again ambiguous and useless. One or more spider will end up crawling the same page. Thus, the main design approach we will aim for is implementing a single crawler and queue, with multiple spiders access to them. 

<br>

### How multithreading is going to work

In this case, the main idea is to make multiple spiders crawl over all the pages from the waiting list and iterate in the same manner. The thing to note is that in case of the first instance of the spider, it is irrelevant to create multiple instances since it only needs to crawl over the base url and gather the initial set of urls for the next crawl - wherein we will introduce multiple spider instances. Another thing is that the first spider also needs to create the project directory and then create the two data files - 'queue.txt' (with the base_url of the page to be crawled) and 'crawler.txt' (which at this point of time would essentially be an empty text file). After all this is done, thereby, the other spiders need not worry about anything else. They just need to crawl normally and continue their work.

<br>

As a basic notion of making the user understand that something is going on, we will be printing the instance number / thread number / spider number and the page which it is crawling at every point of time.

<br>

### Another Problem!

Now, when everything seems to be going great, a small issue that I learnt of, is that the urlopen method does not actually returns a human readable string after the parse the HTML. Instead it returns bytes. But the functions written in 'link_finder' actually needs a string format to parse correctly.  

#### The gather_links() method

What this does is actually the solving the above problem. Essentially, it converts all the byte values from the html response into a human readable string format ie utf-8. (God help if the page is not written with a HTML-utf-8 format!!). It then returns a set of all the urls found on the corresponding html page. 

<br>

The feed() function essentially executes everything within the LinkFinder class which takes in the base url of the home page (base_url) and the page which is it is crawling (page_url), parses over the html (which should be in a string format) and return the urls accordingly. The LinkFinder.page_links() method return the set of urls found within that page.

<br>

#### The add_links_to_queue() method

Everything is rather intuitive here. We just check whether the url is not already present in the crawled list or the waiting list and accordingly add it to the queue ie the waiting list. Now another thing to see here is the domain name checking. 

```python
if Spider.domain_name not in url:
                continue
```

Say we have a url as 'github.com/saychakra/', where I have some links along with some links to YouTube.com, Instagram.com, LinkedIn.com etc. Now, what the crawler would do is that, it will go through the initial page- 'github.com/saychakra/' and find the YouTube, IG, LinkedIn links and go there, and from there basically start crawling over any link it finds- which basically means that it'd end up searching almost the whole web! We don't want that (At least not now :P). So we check whether the url is within the current base domain ie anything starting with 'github.com/saychakra'. We'd want the crawler to crawl only over those links. 

What the above code snippet does is check whether the base domain is present within the specified url given or not. If not then we just skip it- ie. not add it to the queue. Otherwise, we add it to the queue.

<br>

#### The update_files() method

Its pretty intuitive man. Just give it a look!

### Domain name extraction

The general url structure is as follows:

```
https://wikipedia.org/Alan_Turing
 /|\          /|\       /|\
  |            |         |
  |            |         |
  |            |         |
Protocol     Domain    Directories
```
Now, the main reason we have this is because all domain names are not designed in the same way. 
Some are like 'mail.google.com/' some are like 'www.something.gov.politics_sucks.lol', you get the idea...

So what we wanna do is, fetch out the proper domain name such that everytime out crawler is set out. It finds the proper one and doesn't end up crawling over the whole internet as I mentioned before!

#### Working of the code:

How domain.py works is that say we have the following url:
'https://mail.google.com/mail/u/0/#inbox'

<br>

What the get_subdomain_name(url) does is that it just extracts the whole subdomain: 
'mail.google.com'

<br>

Then what the get_domain_name(url) does is split it into a list (separated by the '.'). So, we end up with something like this:

```python
results = ['mail', 'google', 'com']
```

<br>
After that we just return the last two strings separated by a '.' ie:
'google.com'

### Initializing Multithreading

The main reason why multithreading is brought up in the first place is already specified above. Plus, it looks and sounds cool :P !! 

<br>
Well to see the number of threads that could be run on your machine run the following code snippet:

```python
import os
print(os.cpu_count())
```

In my case it returns 4. The thing is I have a dual core CPU. Thus there is 2 physical CPUs at 2 cores (dual core) for each CPU. Hence,
<br>
2 CPUs X 2 cores per CPU = 4 total cores

Generally I think it is good to specify the number of threads as the total number of cores which can be supported by your machine. Thus, I specify Number_of_threads as 4

<br>

The function of each of the methods in main.py is already mentioned in the comments. Still I am mentioning them one by one in the order I wrote:

```python
def crawl():
    queued_links = gen.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()
```

What this does is basically access the queue file ie queue.txt which is initally created by the first spider. It then extracts the items into a set using file_to_set(). After that it just prints the number of items left in the queue, for reference and create the appropriate jobs.

<br>

```python
def create_jobs():
    for link in gen.file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join() # to avoid collision among multiple threads
    crawl()
```

What this does, is extract each link from the set and put it into the threading queue.
NOTE: queue = Queue() is the threading queue. 
We are basically putting every link from queue.txt to a queue set and from that set into the queue thread. That's all.
<br>
The join() functions helps avoid collition among multiple threads. Then, the crawl function crawls through each of the specified urls

<br>

```python
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
```

This method just creates the number of threads as specified. In my case 4 threads would be created.
'target' is a built-in parameter of the Thread() class which specifies what work the thread should be doing (it is specified below). The daemon is just suggesting that the threads are left as soon as the main program terminates. Thereby, the threads are started with start()

<br>

```python
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()
```
Here, every item is extracted from the threading queue and the work is specified within the crawl_page() method of the Spider class. Refer to that section for more details. We iterate over the threading queue till it is empty and thereby the task is done.

<br>

### Problems

As of now, there is only one problem. 
<br>
- The other problem which arose was because of a slight error in appending files.
<br>

```python
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data)
```
This was the method for appending links to the queue.txt. Well as you may have notices it does not contain any newline character. This ended up appending all links without the newline and the whole program failed as soon as we needed to remove a link from the queue and push it to the crawled file. This was solved later on.
<br>
Final Snippet looks something like this:
```python
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')
```

- One of the major problems is that most of the websites implement some kind of robot.txt file within them, to help counter attacks and visits from someone other than a human being. The setting mainly helps them to disallow anyone except a human being to parse any link within the page. Hence parsing almost all websites is getting somewhat a bit difficult. If anyone has any solution then please let me know. I'll also try and put some effort on getting something done.

### Observations and Conclusion

As a conclusion the crawler is successfully able to crawl any unrestriced and open websites 
(websites which have no or poor robot.txt configuration). 
<br>
EG. https://linrunner.de/en/tlp/docs/tlp-linux-advanced-power-management.html (Page for linux TLP)
In this case. Most of the links were crawled. We ended up with a total of 318 links. The files after running are removed from the repository. You may
download the repository and test it on your local machine.
<br>
Another thing was that during the running of the program, a quick htop (if you're using UNIX)) shows how all the cores in your machine will be performing
at the same time. This suggests that our multithreading approach is also working. Finally, I can also say, this is quite a fast crawler. It crawled 318
links in merely 20 seconds or so. I can later run a time module to find the time taken for the entire crawl to complete.
<br>
PS. There are and always will be some HTTP Errors. But that's because those pages are dead now or there are some kind of a server error. eg. HTTP Error 403, 404 etc. 
