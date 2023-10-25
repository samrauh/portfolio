# ETH Chair of Education Systems - YLMI Index

> Keywords: R, Shiny, Docker, CI/CD, APIs

During my civil service at the [ETH Chair of Education Systems](https://ces.ethz.ch/) I got the chance to work on the [Youth Labour Market Index](https://ces.ethz.ch/research/benchmark-instruments/YLMI.html).

> "The CES Youth Labour Market Index (CES YLMI) is a multidimensional composite index that enables comparison of young people’s labour market situation across countries and over time. The index consists of twelve indicators grouped into four dimensions. In contrast a single-​indicator approach using something like the unemployment rate, the CES YLMI accounts for multiple aspects of employment."

## Goal and Starting Position
The goal of this projects was to automate the updating process of the index as much as possible. In the past there was the need for a lot of manual work to update the index with the newly provided data. The Index consists of many different values in which are provided by statistical offices like Eurostat or the ILO. These indicators can be accessed automatically through their APIs. In a frist step the data is gathered an combined into a dataset which can then be used by the [YLMI online tool](https://apps.ces.ethz.ch/ylmi/) a public R shiny application. The second part of this automation process is the implementation of a CI/CD pipeline using Docker and GitLab CI/CD. Those three steps make this a very interesting E2E project.

## 1. Updating the Data Gathering Script
To gather the data from the different sources and compute the index there is an R script.
In the first step it scarpes the data from the different API's (Eurostat, ILO) and already performs different data manipulations and calculations of the indicators.
Further there are qulity controll mechanisms to compare the gathered data with historical data, to check if there are any inconsistencies.

The data is then further processed to build the base dataset for the R shiny webapp.

## 2. Changes in the R shiny app

The base of the R shiny app was already instanciated but some additional changes were made by me. 

The changes include getting rid of hardcoded year values, a change in the map, adjustment of tables and others. 

## 3. CI/CD Pipeline

The third part of the projects is considers the deployment. Befor the update the shiny app was deployd using the Roxygen2 library and everytime there was a change made to the data or the app itself the whole projects needed to be pushed manually to the server.

To solve this problem we decided on using docker and Gitlab CI/CD to automatically deploy the changes.
