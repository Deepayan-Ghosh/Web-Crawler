"""
    file contains various functions used as subroutines by the spiders and crawler

"""

import os
import urlparse


#   creates the project directory
def create_main_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)


# used as subroutine in create_directory
#   splits the path into directory_name and filename and returns them as tuple
def path_split(path):
    u = urlparse.urlparse(path)
    path = get_domain_name(path) + u.path
    return os.path.split(path)


#   creates the directory with the specified path, and also creates an empty file for the corresponding URL
def create_directory(path):
    org_dir = os.getcwd()
    path_tuple = path_split(path)
    dir_path = path_tuple[0]
    resource = path_tuple[1]
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    change_directory(dir_path)
    if resource == '':
        resource = dir_path.split('/')[-1]
    resource.replace('.', '_')
    create_file(resource)
    change_directory(org_dir)


def change_directory(path):
    os.chdir(path)


#   utility function to create file and write data
def create_file(path, data=''):
    f = open(path, 'w')
    f.write(data.encode('utf-8'))
    f.close()


#   overwrites already existing file
def add_content(path, data):
    create_file(path, data)


#   takes a set() as parameter, produces a string containing all the links in that set, and writes it to a file
def set_to_file(path, link_data):
    s = ''
    for link in link_data:
        s += link + '\n'
    add_content(path, s)


#   takes a file_path and converts the contents of that file into a set
def file_to_set(path):
    f = open(path, 'r')
    links = set()
    for line in f:
        links.add(line.strip('\n'))
    f.close()
    return links


#   given an url which may be of form A.B.C.D.tld(in general), the function parses it and returns the main domain
#   consisting of the hostname and tld
def get_domain_name(url):
    domain_name = ''
    try:
        parse_result = urlparse.urlparse(url)
        domain_name = parse_result.netloc.split('.')
        domain_name = '.'.join(domain_name[-2:])
        return domain_name
    except:
        return ''


if __name__ == "__main__":
    create_directory('https://docs.python.org/2/library/os.path.html')
    create_file('hi.c', '')
