import csv
import requests
from bs4 import BeautifulSoup
import re


def gather_results(csv_file):
	"""
	Scrapes every web page in the given CSV file for two variables:
		* Sponsor name
		* Number of studies found

	Writes these results to a new CVS file
	"""
	print "Gathering results..."
	results = []
	with open(csv_file) as file:
		reader = csv.reader(file, delimiter=',')
		for row in reader:
			for url in row:
				results.append(parse_web_page(re.sub('[^!-~]+',' ',url).strip()))

	with open('output.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['Sponsor', 'Number of Studies Found'])
		writer.writerows(results)

	print ".\n.\n.\nDone! Find your results in the output.csv file :)"


def get_file():
	"""
	Helper function
	"""
	return raw_input("Enter the path to your file ('example.csv'): ")


def parse_web_page(url):
	"""
	Web scraper helper function
	"""
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	search = soup.find_all('div', class_='w3-center')
	results = search[2].get_text()
	number_of_studies = results.split()[0]
	if number_of_studies == 'No':
		number_of_studies = '0'
	spons = results.split(':')[1].split('|')[0].strip()
	return [spons, number_of_studies]



def main():
	# Run the program
	file = get_file()
	gather_results(file)


if __name__ == "__main__":
	main()
