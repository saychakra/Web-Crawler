import os

############################### General House-Keeping Functions ###############################
#################################### for file manipulation ####################################

# writing contents into a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# appending contents at the end of the file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data)
    
# deleting the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass


################################################################################################


# creating the project directory
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project: ", directory)
        os.makedirs(directory)

# creating a new file
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawler = project_name + '/crawler.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url) # we pass the base_url as the initial variable
    if not os.path.isfile(crawler):
        write_file(crawler, '')
    