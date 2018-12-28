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
