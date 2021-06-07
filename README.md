# web-scraping-challenge
This repository is for DU Data Analytics Bootcamp web-scraping-challenge homework.  There are 2 sections to this project.

## Section 1
During Section 1, I was able to use the splinter and beautiful soup libraries in Jupyter Notebook to scrape data on Mars from 3 different websites.  I was able to scrape several different types of data including text, headlines, and image urls. The image urls were a bit tricky because they had to be put into a for loop that would click through the page based off a html tag that I had pulled.  Once on the new page the image url could be added to a dictionary.  All data that was scraped was added to a dictionary for use in the next section.

## Section 2
In Section 2, I was able to use the scrape script from Section 1 and create a function in a .py file.  Then I created a flask app that would call the scrape function from the .py file and store it in a mongodb database.  Lastly, I created an .html file that rendered the scraped data from the mongodo database into a functioning website. It was created with a button that will call the scrape function anytime I want to see the most recent info on Mars. 
