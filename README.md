# Mission-to-Mars

## Overview
### Purpose
After creating a web app from scraped data on Mars, I was asked to adjust the current web app to include images of Mars's four hemispheres. To do this, you’ll use BeautifulSoup and Splinter to scrape full-resolution images of Mars’s hemispheres and the titles of those images, store the scraped data on a Mongo database, use a web application to display the data, and alter the design of the web app to accommodate these images

Deliverable 1: Scrape Full-Resolution Mars Hemisphere Images and Titles
Deliverable 2: Update the Web App with Mars Hemisphere Images and Titles
Deliverable 3: Add Bootstrap 3 Components


Find the HTML tag that holds all the links to the full-resolution images, or find a common CSS element for the full-resolution image.

Using a for loop, iterate through the tags or CSS element.

Create an empty dictionary, hemispheres = {}, inside the for loop.

Use the for loop to complete the following actions: a) click on each hemisphere link, b) navigate to the full-resolution image page, c) retrieve the full-resolution image URL string and title for the hemisphere image, and d) use browser.back() to navigate back to the beginning to get the next hemisphere image.