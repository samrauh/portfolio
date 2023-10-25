# Article Database

> Keywords: SQL, MySQL, Python, Relational Database, APIs, Data Scraping

This database is part of a larger End-to-end project. This part handles the gathering of data and its storage in a MySQL database.

The goal is to easily scratch data from newspaper API's and store them into a database with additional information.
This database focuses on newspaper articles about companies but it could be extended with any category, e.g. Personalities.

The database acts as a base for later projects (ML, shiny/dash apps, Data Analysis,...)

## Gathering the data

The first step in the process is the gathering of newspaper data. I created a python module for the Guardian API which makes it more efficient to scrape articles with a keyword and a year as input.
The module could be extended with other Newspaper API's such as the one of the New York times.

## Storing the data

A second module handles the storing of the gathered data in the database.
It provides the functionality of easily inserting a pandas dataframe into the SQL database.
