import pandas as pd
from sklearn import linear_model
import random
import pickle


def load_data(path: str = './flight_prices/flight_prices_training.csv'):
    # Load data using provided path or default path
    train = pd.read_csv(path)
    # Drop column not needed for model training - identified by data scientist
    train = train.drop(columns=['flight'])
    # Identify categorical columns and transform to numerical for model
    cat_cols = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    train = pd.get_dummies(train, prefix=cat_cols, columns=cat_cols)
    # Split full dataset into x and y variables
    y_train = train['price']
    X_train = train.drop(['price'], axis=1)

    # Return preprocessed and split dataframes
    return X_train, y_train


def train_model(X_train: pd.DataFrame, y_train: pd.DataFrame):
    # Set random seed for reproducibility
    random.seed(10)

    # Train model using preprocessed data
    lasso = linear_model.Lasso(alpha=.1, max_iter=5000)
    lasso = lasso.fit(X_train, y_train)

    pickle.dump(lasso, open('model.pkl', 'wb'))

    return lasso


if __name__ == '__main__':
    X_train, y_train = load_data()
    train_model(X_train, y_train)
