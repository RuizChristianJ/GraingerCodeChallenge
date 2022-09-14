FROM python:3.8-slim

RUN mkdir flight_prices

COPY ./requirements_test.txt ./requirements_test.txt
RUN python -m pip install --no-cache-dir --upgrade -r ./requirements_test.txt

COPY ./flight_prices/flight_prices_training.csv ./flight_prices/flight_prices_training.csv
COPY ./flight_prices/flight_prices_predict.csv ./flight_prices/flight_prices_predict.csv

COPY training.py ./train.py
COPY prediction.py ./prediction.py

RUN python3 training.py
RUN python3 prediction.py