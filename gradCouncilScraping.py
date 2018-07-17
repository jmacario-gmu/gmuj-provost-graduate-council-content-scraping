# Summary: Program to scrape the Provost website grad council pages and output the main content HTML to an HTML file and all contained PDF links to a CSV file, as well as saving all linked documents to local subfolders
# Details: This program requires a text file in the working directory containing a list of URLs to fetch. Each URL should be on its own line.
# Dependencies: This script requires additional libraries: requests and bs4. You can install these from the command lin using pip. Example: "pip install bs4".
# Last Modified: 20171004
# Modified by: JM

### import libraries
import os, urllib.request, requests, bs4, datetime, re, webbrowser, getpass, time

### define functions

def fnIsYes(inputString):
	##
	# Summary: checks to see if the input is a 'yes' ("y" or "Y" character)
	# Details: 
	# Last Modified: 20170929
	# Modified by: JM
	##

	# check to see if input string represents a yes
	if inputString=='y' or inputString=="Y": 
		varReturn=True
	else: 
		varReturn=False
	# return value
	return varReturn

def fnCleanHTMLContent(inputString):
	##
	# Summary: cleans-up HTML
	# Details: uses regex to find and replace parts of the content
	# Last Modified: 20171004
	# Modified by: JM
	##

	# create output string
	outputString=inputString
	# replace newline chars after line break tags
	# outputString=re.sub('<br/>\n','<br/>',outputString)
	# replace table class
	# outputString=re.sub('class="tablepress tablepress-id-\d+"','class="datatable"',outputString)
	# add table style
	# outputString=re.sub('<table class="datatable"','<table class="datatable" style="width:98%;"',outputString)
	# remove table id
	# outputString=re.sub(' id="tablepress-\d+"','',outputString)
	# remove tr classes
	# outputString=re.sub(' class="row-\d+ (odd|even)"','',outputString)
	# remove th and td classes
	# outputString=re.sub(' class="column-\d+"','',outputString)
	# add th styles
	#outputString=re.sub('<th>','<th style="width:20%">',outputString)
	# remove tbody class
	# outputString=re.sub(' class="row-hover"','',outputString)
	# return value
	return outputString

def fnTimestamp():
	##
	# Summary: returns a timestamp
	# Details: format: YYYYMMDDHHMMSS
	# Last Modified: 20160926
	# Modified by: JM
	##

	# return timestamp
	return '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())

def fnOutputStringToFile(inputString,outputFileName):
	##
	# Summary: outputs a string to a file
	# Details: string to output and the name of the file to output to are specified as parameters
	# Last Modified: 20161004
	# Modified by: JM
	##

	# open/create text file for output ("w" indicates opening file for writing text data)
	text_file = open(outputFileName, "w")
	# write output string to file
	text_file.write(inputString)
	# close text file
	text_file.close()

def main():
	##
	# Summary: 
	# Details: 
	# Last Modified: 20171004
	# Modified by: JM
	##

	# clear screen (cross platform - cls for windows, clear for linux)
	os.system('cls' if os.name == 'nt' else 'clear')

	# get option inputs
	bolWriteURLContentHTML = fnIsYes(input('Write HTML content to file? (Y/N): '))
	bolWriteURLContentCSV = fnIsYes(input('Write document links to CSV file? (Y/N): '))
	bolSaveFiles = fnIsYes(input('Save documents files locally? (Y/N): '))

	# Print text file URL list info
	print('\nProcessing URL list: '+urlListFile+'\n')

	# Open URL list text file for reading
	input_file = open(urlListFile, 'r')
	# Set initial value for URLs processed (lines read)
	count_lines = 0
	# Loop through lines in input file
	for line in input_file:
		# check to see if line begins with a number sign (which indicates a comment)
		if line[0]!="#":
			# Increment number of lines read
			count_lines += 1
			# Get URL to fetch data from, from current line of text file
			strFetchURL=line.strip()
			# parse month and year from URL
			workingMonth=strFetchURL.split('-')[0].split('=')[1] # based on file name convention, split on hyphens, take the first part, then split on equal sign and take the second part, which represents the month
			workingYear=strFetchURL.split('-')[1] # based on file name convention, split on hyphens, take the second part, which represents the year
			# set output filename prefix (folder path)
			outputFilenamePrefix=os.path.join(workingYear,workingMonth)
			# set output HTML file filename
			outputFileNameHTML=os.path.join(outputFilenamePrefix,'gradCouncil-'+strFetchURL[32:]+'_content.html')
			# set output CSV file filename
			outputFileNameCSV=os.path.join(outputFilenamePrefix,'gradCouncil-'+strFetchURL[32:]+'_file_list.csv')
			# if we are going to be making any output files, make sure we have or create the folders we will need as necessary
			if bolWriteURLContentHTML or bolWriteURLContentCSV or bolSaveFiles:
				# get directory name(s)
				directory = os.path.dirname(outputFileNameHTML)
				# if directories don't exist
				if not os.path.exists(directory):
					# make them
					os.makedirs(directory)
			# Get HTML document from specified URL
			print('Fetching URL: '+strFetchURL+'\n')
			res=requests.get(strFetchURL)
			# check status
			res.raise_for_status
			# print('Status: ' + str(res.status_code))
			# if status is not 200, print message and exit
			if res.status_code!=200:
				print ("Error: the response status code was: "+str(res.status_code))
				time.sleep(5)
				exit()
			else:
				# output progress message
				print("URL fetched successfully.")
				# parse HTML document to variable using BeautifulSoup
				parsedPageContent=bs4.BeautifulSoup(res.text,"html.parser")
				# get list of elements matching specified CSS selector
				print('Selecting HTML using selector: '+cssSelector)
				selectedTags=parsedPageContent.select(cssSelector)
				# check length of list
				if len(selectedTags)==0:
					print('Error: no HTML content was selected')
					exit()
				print('Number of HTML selections found: ' + str(len(selectedTags)))	
				if len(selectedTags)>1:
					print('Warning: multiple HTML selections found')
				# store HTML tag content to string variable
				inputString=str(selectedTags[0])
				#print('HTML Content Snippet: '+inputString[:50]+"...")
				# Clean-up content
				outputString=fnCleanHTMLContent(inputString)
				print('HTML content processed.')
				# check to see if we should output HTML file
				if bolWriteURLContentHTML:
					# output string to file
					fnOutputStringToFile(outputString,outputFileNameHTML)
					print('Data written to file: '+outputFileNameHTML+'\n')
				# Find document links
				print('\nParsing content for document links.\n')
				# parse output content (to find all A tags)
				parsedSectionContent=bs4.BeautifulSoup(outputString,"html.parser")
				# prepare link output text variable
				outputLinksText=''
				# find all A tags and loop through them
				for a in parsedSectionContent.find_all('a', href=True):
					urlMatch = re.search(fileRegex,a['href'].lower())
					if urlMatch:
						outputLinksText+=a['href']+'\n'
						if bolSaveFiles:
							# get filename
							remoteFilename=a['href'].rsplit('/', 1)[-1]
							# set local filename
							localFilename=os.path.join(outputFilenamePrefix,'gradCouncil-'+strFetchURL[32:]+'-'+remoteFilename)
							# download and save file
							workingDocumentURL = urllib.request.urlopen(a['href'])
							workingFile = open(localFilename, 'wb')
							workingFile.write(workingDocumentURL.read())
							workingFile.close()
							print("Document file saved: "+localFilename)
				# check to see if we should output CSV file of document links
				if bolWriteURLContentCSV:
					# remove trailing comma
					outputLinksText=outputLinksText[:-1]
					# output string to file
					fnOutputStringToFile(outputLinksText,outputFileNameCSV)
					print('Document links written to file: '+outputFileNameCSV+'\n')
				# print completed message
				print('URL Processing complete.\n')
	# print completed message
	print('\n\nProcess complete.\n')
	print('Number of URLs processed: '+str(count_lines))

### define global variables

# Set timestamp variable
timestamp = fnTimestamp()
# Text file list of URLs to fetch
urlListFile='urlList.txt'
# CSS selector to define which tags to capture
cssSelector='div#content'
# regex to determine which file links to match
fileRegex = "(pdf|docx?|xlsx?|pptx?)$"

### run main function if this file is running as main
if __name__ == "__main__":
	main()
