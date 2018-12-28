# Web-Crawler
### Introduction
This is a basic web crawler. In the subsequent phases I am gonna try and report each and every thing I
learnt, read and implemented in making this project. Let's Begin!!!

<br>
Well in the first phase, the basic functions for creating a project and a subsequent project directory is 
done (pretty intuitive). In the next phase, a few house-keeping directory manipulation functions are written.

<br>

#### Speeding up the process
In general, as far as computational time is concerned, writing into a file takes a considerably good amount of time. In general, when we are trying to crawl over a huge page, this can come into as a difficulty and then my friend, you can observe the noticable time lag! 
So to solve this problem, one approach is to use variables. But again, those are temporary solutions. Thus, as a final solutions we can use the best feature of both by using a set.
<br>
So, essentially what we are doing here is that, say we have about 30 urls in our waiting list (queue), which are needed to be crawled. Instead of reading and writing contents from the file (queue.txt) every time, we use a set. We convert the elements of the file (each line in this case) into set items and access them through the set (which should be a lot more faster)

<br>

#### Getting Links
Here comes the reason why I say, Python is the greatest language in the world right now!
We need to parse the html and find the links in each page. Python comes with a build in HTMLParser class which has all the features necessary to implement the same.
<br>
Understanding the class:
<br>
Say we have some url like this:
```
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

```
def handle_starttag(self, tag, attr):
        if tag == 'a':
            for (attribute, value) in attr:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
```

### Implementing the Spider
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

```
if Spider.domain_name not in url:
                continue
```

Say we have a url as 'github.com/saychakra/', where I have some links along with some links to YouTube.com, Instagram.com, LinkedIn.com etc. Now, what the crawler would do is that, it will go through the initial page- 'github.com/saychakra/' and find the YouTube, IG, LinkedIn links and go there, and from there basically start crawling over any link it finds- which basically means that it'd end up searching almost the whole web! We don't want that (At least not now :P). So we check whether the url is within the current base domain ie anything starting with 'github.com/saychakra'. We'd want the crawler to crawl only over those links. 

What the above code snippet does is check whether the base domain is present within the specified url given or not. If not then we just skip it- ie. not add it to the queue. Otherwise, we add it to the queue.

<br>

#### The update_files() method

Its pretty intuitive man. Just give it a look!