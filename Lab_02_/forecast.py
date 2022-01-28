# Written by Arief Budimen
# Last modified on 29/08/2021

# Import required libraries
from numpy import array, concatenate #numpy
from pandas import RangeIndex, read_csv, Series #pandas
from sklearn.linear_model import LinearRegression #scikit-learn
from matplotlib import pyplot #matplotlib
from zipfile import ZipFile
#Need to download the required specs: numpy pandas scikit-learn matplotlib

# Function to Open the zip files
def read_data(zipname, filename):
    df = read_csv(ZipFile(zipname).open(filename))
    df.dropna(inplace=True)
    df.drop(columns=['entry_id'], inplace=True)
    return df

# Function to add How many days behind used for prediction
def add_lags(df, n):
    colname = df.iloc[:, 1].name
    for s in range(1, n + 1): #n=number of days (Starts from previous day 1 up to day n+1)
        df[f'{colname}_lag_{s}'] = df[colname].shift(s) #shifting value of day to the back

# Main forecast function
def forecast(df, h):
    lags = df.iloc[:, -1].isna().sum() #Check last column number of N/A, summed to calculate for total N (number of previous days)
    X = df.iloc[lags:, 2:] #"Lags:" uses only value without NA (10th column onwards), While taking column 2 data frame
    y = df.iloc[lags:, 1] # Temperature of current temperature
    reg = LinearRegression().fit(X, y) # algorithm used: Linear Regression
    last_obs = df.iloc[-1:, 1:-1].to_numpy()[0] #Convert last row into numpy from pandas.
    predictions = []
    for _ in range(h): #h is horizon (how many days is getting predicted)
        y_hat = reg.predict(array([last_obs])) #Uses previous last observation to predict next temperature (Recording Period)
        predictions.append(y_hat[0]) #Prediction for next temp
        last_obs = concatenate((y_hat, last_obs))[:-1] #Merging the data in 1 array, Previous value of field_1_lag_n will be dropped
    return Series(predictions, name=temp.iloc[:, 1].name)


# Ploting the data
def plot(df, fcast):
    df.iloc[:, 1].plot()
    n = len(df)
    fcast.index = RangeIndex(n, (n + len(fcast)))
    fcast.plot()
    pyplot.show()


# FORECAST (7200)
ZIPNAME = '7200.zip'
LAGS = 10
HORIZON = 100

def main():
    # Open the exported CSV files for Temperature
    temp = read_data(ZIPNAME, '1.csv')
    # Adding lags to data
    add_lags(temp, LAGS)
    # Implement linear regression on the data
    fcast = forecast(temp, HORIZON)
    # Plot the predicted temperature data on the same graph
    plot(temp, fcast)
    # Open the exported CSV files for Temperature
    humidity = read_data(ZIPNAME, '2.csv')
    # Adding lags to data
    add_lags(humidity, LAGS)
    # Implement linear regression on the dat
    fcast = forecast(humidity, HORIZON)
    # Plot the predicted humidity data on the same graph
    plot(humidity, fcast)

# if name equals main, then run main function
if __name__ == '__main__':
    main()
