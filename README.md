# 📝 MySmartJournal 📝
MySmartJournal is a full-stack web app gratitude journal

Deployment Link: Coming soon...

## Summary

- The journal allows users to make a 'morning' or a 'night' type journal entry, view the history of their journal entries, and sort/filter by time or type. 
- Users are asked the same 3 questions for each entry type, so users can see how their answers change over time. 
- The smart aspects of the journal include sentiment analysis using AWS Comprehend API, SMS reminders using Twilio API, and various data visualizations of streaks, moods, and common phrases using Charts JS and custom data analysis.

## About the Developer 🤖

MySmartJournal was authored by [Masha Ikromova](https://www.linkedin.com/in/mashikro/). Masha studied Neuroscience and Software Engineering at Columbia University and Hackbright Academy respectively. This is her first full-stack software project. Learn more about the developer on [Linkedin](https://www.linkedin.com/in/mashikro/). 

## Technologies 👾
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


MySmartJournal is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. On the front end it uses Jinja2, HTML/CSS, Bootstrap, Javascript (JQuery and AJAX) to interact with the backend. The graphs are rendered using Chart.js and wordcloud2.js. The sentiment analysis is powered using the AWS Comprehend API. User's receive an SMS reminder to write in app daily, which is done using a Twilio API. Server routes are tested using the Python unittest module.

## Features 🚀

- Users can make a journal entry.
- Users can view all journal entries. They can sort them by type and time.
- Users can view their streak, number of consecutive days of making an entry, which reinforces them to keep journaling.
- Users can view their happiness graph.
- Users can learn what makes them happy through the word cloud.
- Users can learn the sentiment of each entry through Sentiment Analysis 
- Users can receive text reminders to write in the journal.

