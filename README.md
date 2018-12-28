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