# MySmartJournal

## Summary

MySmartJournal is a full-stack web app gratitude journal where users can make a 'morning' or a 'night' type journal entry, view the history of their journal entries, and sort/filter by time or type. Users are asked the same 3 questions for each entry type, so users can see how their answers change over time. The smart aspects of the journal include sentiment analysis using AWS Comprehend API, SMS reminders using Twilio API, and various data visualizations of streaks, moods, and common phrases using Charts JS and custom data analysis.

## About the Developer

MySmartJournal was authored by Masha Ikromova. Masha studied Neuroscience and Software Engineering at Columbia University and Hackbright Academy respectively. Learn more about the software engineer on Linkedin. 

## Technologies

### Tech Stack

- Python
- Flask
- SQL
- SQLAlchemy
- Jinja2
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Bootstrap
- Charts.js
- Python unittest module
- Twilio API
- AWS Comprehend API

MySmartJournal is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. On the front end it uses Jinja2, HTML/CSS, Bootstrap, Javascript (JQuery and AJAX) to interact with the backend. The graphs are rendered using Chart.js and wordcloud2.js. The sentiment analysis is performed using the AWS Comprehend API. User's receive an SMS reminder to write in app daily, which is done using a Twilio API. Server routes are tested using the Python unittest module.

## Features

Making a journal entry
Viewing all journal entries. Sorting journal entrues by type and time
Streaks to track habit of journaling
Happiness graph, directly charting user input
Word cloud
sentiment analysis
twilio sms reminder 

