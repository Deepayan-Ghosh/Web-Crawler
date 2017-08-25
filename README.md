# Multi Threaded Web Crawler
This is a multi threaded crawler which takes an url as input through commad line, and crawls all the links belonging to that domain, and creates a folder hierarchy on the local computer. The contents of each web page is written to a file and placed in the correct folder in the created hierarchy. For example, in the screenshot folder, I have a screenshot of the folder hierarchy created on my own system.

## Getting stated
The instructions below will allow you to run the crawler on your machine.

### Prerequisites
You must have Python 2.7 installed. To check, on Linux, type the following on your terminal:
```
python --version 
```
You will be shown the current version of python installed.

### Running the crawler
Download the repository on your local system.
Navigate to the directory where you have placed the downloaded files.
From terminal, run:
```
  python crawler.py https://www.example_url.com
```
and the crawler should be up and running.
There is an optional command line argument which is a kind of flag which tells the parser whether or not to remove extra newlines, carriage returns from the scraped data. The value is stored in 'remove' variable which defaults to False. You can explicitly tell the parser to remove the spaces by adding a command line argument ``` True ``` in the end, like:
```
  python crawler.py https://www.example_url.com True
 ```
 ## Contributing
 
 Anyone is open to contributing but please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.
 
 ## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
