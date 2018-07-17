# Mason Provost Graduate Council Content Scraping

**A Python program used to scrape the Provost website graduate council web pages and output the main content to an HTML file and all included document links (PDF, DOC, XLX, PPT, etc.) to a CSV file, as well as saving all linked documents to local subfolders.**

## Details

This program requires a text file in the working directory containing a list of URLs to fetch. Each URL should be on its own line.

## Dependencies

This script requires a couple additional Python libraries: **requests** and **bs4**. You can install these from the command line using **pip**. 
Example: "pip install bs4"