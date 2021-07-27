# DisasterRespnse-Udacity
This is my work for the Udacity Data Science Nano-degree project for the Disaster Response ML Project.

The goal of this project is to train a Machine Learning Model that will take tweets and text messages that are sent during times of disaster and categorize them according to a specific set of labels.  One use of this sort of ML model could be to automate the distribution of messages to the most relevant organization in order for that organization to take action.  Figure Eight Inc.  (now part of appen  https://appen.com/ ) have provided a labeld training set consisting of two .csv files; a file with messages (disaster_messages.csv), and a file with labels (disaster_categories.csv).  As a part of the solution to this problem will be a web app that can be used by an emergency worker to imput new messages and get classification results.  The web app will also display viualizations of the data.  

The components of this project are:

## 1. The ETL Pipeline:
 
   A Python script called `process_data.py` which has the following effects:
    - Load the `messages.csv` and `categories.csv` datasets
    - Merge and clean the datasets
    - Store the cleaned data in an SQLite database
    
## 2. The ML Pipeline:
 
  A python script called `train_classifier.py` that has the following effects:
   - Load the data from the SQLite DB
   - Split the dataset into training and test sets
   - Build a text processing and machine learning pipeline
   - Train and tune the model
   - Output the results on the test set
   - Exports the final model as a `.pkl` file
 
 ## 3. A Flask Web App:
 
 TBD
