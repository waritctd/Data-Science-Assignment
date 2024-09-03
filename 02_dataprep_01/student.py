import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

"""
    ASSIGNMENT 2 (STUDENT VERSION):
    Using pandas to explore Titanic data from Kaggle (titanic.csv) and answer the questions.
"""



def Q1():
    """
        Problem 1:
            How many rows are there in the “titanic.csv?
            Hint: In this function, you must load your data into memory before executing any operations. To access titanic.csv, use the path /data/titanic.csv.
    """
    df = pd.read_csv('data/titanic_to_student.csv', index_col=0)
    rows = df.shape[0]
    print(rows)
    return rows


def Q2(df):
    '''
        Problem 2:
            Drop unqualified variables
            Drop variables with missing > 50%
            Drop categorical variables with flat values > 70% (variables with the same value in the same column)
            How many columns do we have left?
    '''
    half_count = len(df) /2
    df_filtered = df.dropna(thresh = half_count, axis =1)
    columns = df_filtered.shape[1]
    print(columns)
    return columns


def Q3(df):
    '''
       Problem 3:
            Remove all rows with missing targets (the variable "Survived")
            How many rows do we have left?
    '''
    df_filtered = df[df["Survived"].notna()]
    rows = df_filtered.shape[0]
    print(rows)
    return rows


def Q4(df):
    '''
       Problem 4:
            Handle outliers
            For the variable “Fare”, replace outlier values with the boundary values
            If value < (Q1 - 1.5IQR), replace with (Q1 - 1.5IQR)
            If value > (Q3 + 1.5IQR), replace with (Q3 + 1.5IQR)
            What is the mean of “Fare” after replacing the outliers (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
        # Replace Fare == 0 with NaN
    df.loc[df.Fare == 0, 'Fare'] = np.nan

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Calculate logarithm of Fare
    df['Log_Fare'] = np.log(df['Fare'])

    # Calculate quartiles and IQR
    q3, q1 = np.percentile(df['Fare'].dropna(), [75, 25])
    iqr = q3 - q1
    min_boundary = q1 - (1.5 * iqr)
    max_boundary = q3 + (1.5 * iqr)

    # Replace outliers with boundary values
    df['Fare'] = np.where(df['Fare'] < min_boundary, min_boundary, df['Fare'])
    df['Fare'] = np.where(df['Fare'] > max_boundary, max_boundary, df['Fare'])

    # Calculate the mean of Fare after replacing outliers
    mean_fare = df['Fare'].mean()

    # Round the mean to 2 decimal places
    mean_fare_rounded = round(mean_fare, 2)
    print(mean_fare_rounded)
    return mean_fare_rounded


def Q5(df):
    '''
       Problem 5:
            Impute missing value
            For number type column, impute missing values with mean
            What is the average (mean) of “Age” after imputing the missing values (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    df.fillna(df.mean(numeric_only=True), inplace = True)
    mean_age = df['Age'].mean()
    mean_age_rounded = round(mean_age, 2)
    print(mean_age_rounded)
    return mean_age_rounded


def Q6(df):
    '''
        Problem 6:
            Convert categorical to numeric values
            For the variable “Embarked”, perform the dummy coding.
            What is the average (mean) of “Embarked_Q” after performing dummy coding (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    dummy_df_filtered = pd.get_dummies(df[['Embarked']], drop_first=False)

# Concatenate the dummy variables with the original DataFrame
    filtered_with_dummy = pd.concat([df, dummy_df_filtered], axis=1)

    # Drop the original 'Embarked' column
    filtered_with_dummy = filtered_with_dummy.drop(['Embarked'], axis=1)

    # Display the DataFrame to confirm the changes
    mean_embarked_q = filtered_with_dummy['Embarked_Q'].mean()

    # Round the mean to 2 decimal places
    mean_embarked_q_rounded = round(mean_embarked_q, 2)
    print(mean_embarked_q_rounded)
    return mean_embarked_q_rounded


def Q7(df):
    '''
        Problem 7:
            Split train/test split with stratification using 70%:30% and random seed with 123
            Show a proportion between survived (1) and died (0) in all data sets (total data, train, test)
            What is the proportion of survivors (survived = 1) in the training data (round 2 decimal points)?
            Hint: Use function round(_, 2), and train_test_split() from sklearn.model_selection
    '''
    from sklearn.model_selection import train_test_split

    X = df.drop('Survived', axis=1)
    y = df['Survived']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.3, 
        random_state=123, 
        stratify=y
    )
    total_survived_proportion = df['Survived'].mean()

    # Calculate proportions in the training set
    train_survived_proportion = y_train.mean()
    print(train_survived_proportion)

    # Calculate proportions in the test set
    test_survived_proportion = y_test.mean()


    return (round(train_survived_proportion, 2))


