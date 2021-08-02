'''import data files and create database

Arguments:
messages -- pathname of a .csv file containing the messages that are to be loaded.
categories -- pathname of a .csv file containing the labels assigned to the messages
output -- a name that will be used to create the SQLite database, <name>.db

This script takes two .csv files, the first containing messages and the second 
containing categories for that message.  It cleans the data by removing duplicates,
generating category titles and expanding the category field into numeric columns
for each category.  Finaly it creates an SQLite database with the cleaned data.
'''
import os
from os import path
import sys
from textwrap import indent

import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''read in the two data files and merge them into a single dataframe, returning the dataframe'''
    
    # read in the two files into dataframes
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories)

    return df

def clean_data(df):
    '''clean the dataframe.
    
    - remove duplicates
    - convert the string feature in categories to numeric features
    - return the cleaned dataframe
    '''

    df.drop_duplicates('message', inplace=True)
    
    '''create a categories dataframe by spliting the category column on ";"
    The category columns are now key value pairs where the key is the category name
    and the value is either 0 or 1 and they are separated by a -.'''
    categories = df['categories'].str.split(';', expand=True)

    '''rename the columns by stripping off the last two characters from the value'''
    categories.columns = categories.iloc[0,:].apply(lambda x: x[:-2])

    '''Convert the vaules in the categories dataframe into int32's by stripping off all but the last
    character of the string and casting to int32'''
    for column in categories:
        categories[column] = categories[column].apply(lambda x: x[-1:]).astype('int32')

    '''There are more than two values in the "related" column.  We are going to impute the value "2"
    to "0" since the rows with value "0" in the related column have all zero in the remaining varriables.'''
    categories['related'] = categories['related'].apply(lambda x: x%2)
    
    '''' replace the old category column with the new categories dataframe'''
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    
    return df

def save_data(df, database_filename):
    '''Create a new db'''

    # remove the old db if there is one
    if path.exists(database_filename):
        os.remove(database_filename)
    
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('messages', engine, index=False)



def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories \n'\
              'datasets as the first and second argument respectively, as \n'\
              'well as the filepath of the database to save the cleaned data \n'\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':

    main()