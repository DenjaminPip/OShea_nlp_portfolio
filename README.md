| <strong>Portfolio Information</strong> | <strong>Details</strong> |
| -------------------------------------- | ------- |
| Language | Python |
| Libraries Used | NLTK, spaCy, re(Regex), matplotlib, seaborn, pandas, scipy, numpy, scikit-learn, Google API|
| Projects Count | 5 |
| Author | Denny O'Shea |

## Instructions for Running Python Notebooks Locally

Many of these projects exist in Jupyter Notebooks that provide step-by-step explainations of my process. To download and read these files, the following steps are required:

  1. Install dependencies using requirements.txt
  2. Run notebooks as usual by using a Jupyter Notebook server, VSCode, etc.

# Welcome to My GitHub Portfolio

Hello and welcome to my GitHub portfolio! Here, you'll find a collection of my data analyst projects, showcasing my skills and experience in the field. While my focus is currently on data analysis, I'm actively working towards expanding into the realm of data science in the near future. I am passionate about the insights data provide and constantly strive to expand my skills.

## Content

### Helpful Modules

This folder contains simple modules and scripts I have written that are meant to help automate the tasks I complete regularly. Namely, there is a work-in-progress module which I update regularly for helping me download and upload data to my Google Drive API. Most often, I use this to access data in a Google Sheet, but I am also working on adding Google Forms functionality as I often create repetitive surveys for my research projects and it would save time and money having an automated system I have written compared to converting a Google Sheet to a Form through software.

<strong>Note</strong>: I regularly use these modules, so in order for some code to run efficiently on your machine, it may be necessary to download this folder as well.

### DataCamp Projects
  - [Gender Prediction with Sound](https://github.com/DennyOShea/OShea_nlp_portfolio/tree/main/datacamp_projects/gender_prediction_with_sound/notebook.ipynb) | In this guided project, the overall goal is to analyze the gender distribution of authors of best-selling children's picture books from 2008 to 2017 using NLP techniques. The project involves tasks such as fuzzy name matching to check if two strings sound the same, extracting phonetic equivalents of first names, determining the likely gender of names based on a dataset of baby names, and analyzing the gender distribution of authors over time. The project aims to uncover any changes in the gender representation of authors in the given time period.

  <strong>Tools</strong>: fuzzy, pandas, Regex, numpy, matplotlib

  - [Predicting Credit Care Approval](https://github.com/DennyOShea/OShea_nlp_portfolio/tree/main/datacamp_projects/predicting_credit_card_approval/notebook.ipynb) | The overall goal of this guided project is to build an automatic credit card approval predictor using machine learning techniques. The project involves analyzing credit card applications, preprocessing the dataset, performing exploratory data analysis, and building a machine learning model to predict credit card approval. The dataset used is the Credit Card Approval dataset from the UCI Machine Learning Repository, and the project includes tasks such as loading and viewing the dataset, inspecting the applications, splitting the dataset into train and test sets, and handling missing values.

  <strong>Tools</strong>: pandas, numpy, scikit-learn, logistic regression, grid search

  - [Word Frequency in Classic Novels](https://github.com/DennyOShea/OShea_nlp_portfolio/tree/main/datacamp_projects/word_frequency_in_classic_novels/notebook.ipynb) | This is an unguided project where I was tasked with identifying the 10 most frequent meaningful words within the text _Peter and Wendy_ by J.M. Barrie. Specifically, the project required simple Named Entity Recognition (NER) to find which of these 10 words were character names. The data was scraped from <a href="https://www.gutenberg.org/files/16/16-h/16-h.htm">Project Gutenberg</a>, cleaned and tokenized with both NLTK and spaCy.

  <strong>Tools</strong>: NLTK, BeautifulSoup, spaCy, Regex

### NLP Projects
  - [Toxicity Report](https://github.com/DennyOShea/OShea_nlp_portfolio/tree/main/nlp_projects/flagging_toxic_comments/notebook.ipynb) | The goal of this project was to build a program that can identify toxic or negative comments in a dataset of Wikipedia comments and flag them for review. The proposed method involved training a naïve Bayes classifier on a .csv file of comments, but due to computational constraints, the final approach utilized the scikit-learn library for multilabel classification. The steps included parsing and normalizing the data, vectorizing the text, training the classifier, testing its accuracy, and saving the predicted scores to a .csv file.

  <strong>Tools</strong>: scikit-learn, logistic regression, pandas, numpy, tfidf vectorization, Regex, json

### Linguistics Projects
  - [Predicting Prenominal Adjective Word Order based on Degrees of Gradability](https://github.com/DennyOShea/OShea_nlp_portfolio/tree/main/linguistic_projects/gradability_syntax) | In this project, I conducted two small-scale surveys designed to elicit degrees of subjectivity for both semantic and gradability categories. The ultimate goal of this research was to identify the degree to which subjectivity influences prenominal adjective order. Previous research suggests that prenominal adjective order preferences are determined by subjectivity with semantic categories falling within a spectrum. However, it has long been assumed that these semantic categories are highly structured and incapable of unmarked movement. This paper hypothesizes that if this is the case, perhaps a finer degree of subjectivity, that of gradability categories, may be influencing the syntactic structure.

  <strong>Tools</strong>: pandas, GoogleAPI, matplotlib, seaborn, scipy, statistics

## Connect with Me

I hope you find my GitHub portfolio engaging and insightful. Feel free to explore the projects and reach out to me if you have any questions, suggestions, or collaboration opportunities. I am always eager to connect with like-minded individuals and discuss exciting data-related projects.

Thank you for visiting my portfolio, and I look forward to sharing more projects with you in the future!
