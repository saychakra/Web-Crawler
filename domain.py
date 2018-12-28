from urllib.parse import urlparse

# Get domain name (example.com) 
## We just want the last two out of the subdomain
def get_domain_name(url):
    try:
        results = get_subdomain_name(url).split(".")
        return results[-2] + '.' + results[-1] #only the last 2 items of the results list
    except:
        return ''



# Get the subdomain name (name.example.com)
def get_subdomain_name(url):
    try:
        return urlparse(url).netloc # parse through the given url and return the network location (netloc)
    except:
        return '' # since we need to return something!


                                ## Testing the code ##
# print(get_domain_name('https://mail.google.com/mail/u/0/#inbox'))

                                    ## output ##
# google.com #