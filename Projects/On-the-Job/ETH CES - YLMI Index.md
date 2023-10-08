# ETH Chair of Education Systems - YLMI Index

> Keywords: R, Shiny, Docker, CI/CD, APIs

During my civil service at the [ETH Chair of Education Systems](https://ces.ethz.ch/) I got the chance to work on the [Youth Labour Market Index](https://ces.ethz.ch/research/benchmark-instruments/YLMI.html).

> "The CES Youth Labour Market Index (CES YLMI) is a multidimensional composite index that enables comparison of young people’s labour market situation across countries and over time. The index consists of twelve indicators grouped into four dimensions. In contrast a single-​indicator approach using something like the unemployment rate, the CES YLMI accounts for multiple aspects of employment."

## Goal and Starting Position
The goal of this projects was to automate the updating process of the index as much as possible. In the past there was the need for a lot of manual work to update the index with the newly provided data. The Index consists of many different values in which are provided by statistical offices like Eurostat or the ILO. These indicators can be accessed automatically through their APIs. In a frist step the data is gathered an combined into a dataset which can then be used by the [YLMI online tool](https://apps.ces.ethz.ch/ylmi/) a public R shiny application. The second part of this automation process is the implementation of a CI/CD pipeline using Docker and GitLab CI/CD.

## 1. Updating the Data Gathering Script
There is a script which gets the data from the API and performs the calculation. I updated this script to almost fully automate this process.

## 2. Changes in the R shiny app

## 3. CI/CD Pipeline
