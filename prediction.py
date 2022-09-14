import pickle
import pandas as pd


def make_prediction(data_path: str = './flight_prices/flight_prices_predict.csv', model_path: str = 'model.pkl') -> pd.DataFrame:
    # Load Model
    model = pickle.load(open(model_path, 'rb'))

    # Read in new data
    test = pd.read_csv(data_path)

    # Drop column not used in making predictions
    test = test.drop(columns=['flight'])

    # Identify categorical columns and transform to numerical for model
    cat_cols = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    test = pd.get_dummies(test, prefix=cat_cols, columns=cat_cols)

    # Drop empty price column and recreate using model predictions
    test = test.drop(['price'], axis=1)
    test['price'] = model.predict(test)

    # Save dataframe to csv in the same directory
    test.to_csv('flight_prices_predictions.csv')

    # Return results dataframe
    return test


if __name__ == '__main__':
    make_prediction()
