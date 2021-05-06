from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

import statsmodels.api as sm
import numpy as np
import pandas as pd

def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=True):
    """Check Granger Causality of all possible combinations of the Time series.
    The rows are the response variable, columns are predictors. The values in the table
    are the P-Values. P-Values lesser than the significance level (0.05), implies
    the Null Hypothesis that the coefficients of the corresponding past values is
    zero, that is, the X does not cause Y can be rejected.

    data      : pandas dataframe containing the time series variables
    variables : list containing names of the time series variables.
    """
    maxlag=10
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    p_values_array = []
    p_array_count = 0
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=verbose)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            p_values_array.append(p_values)
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
        p_array_count = p_array_count + 1
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]

    #get lag
    p_value_for_optimal_lag = df['Sentiment_x']['Close_y']
    lag = 0
    for i in range(len(p_values_array)):
        for j in range(len(p_values_array[i])):
            if p_values_array[i][j] == p_value_for_optimal_lag:
                lag = j+1
            j=j+1

    return df,lag

#We use adfuller test to test Time Series for Stationarity
# A time series is stationary if mean, variance and autocorrelation structure do not change over time.
def check_for_stationarity(series, signif=0.05, name='', verbose=False):
    """Perform ADFuller to test for Stationarity of given series and print report"""
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue']
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
    if verbose is True:
        print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
        print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
        print(f' Significance Level    = {signif}')
        print(f' Test Statistic        = {output["test_statistic"]}')
        print(f' No. Lags Chosen       = {output["n_lags"]}')

    for key,val in r[4].items():
        if verbose == True:
            print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= signif:
        if verbose == True:
            print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
            print(f" => Series is Stationary.")
        return True
    else:
        if verbose == True:
            print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
            print(f" => Series is Non-Stationary.")

        return False
def make_stationary(data):
    data = data - data.shift(1)
    data = data.dropna()
    return data

def do_granger_causality(data, smooth='Simple', calc_stationairty=True):

    '''
    Performs a granger causality on the data that is passed in. Returns dataframe representing the
    :param data:
    :param smooth:
    :param calc_stationairty:
    :return granger_df, lag:
    '''
    stationary_smoothed_df = None
    for i in range(0, len(data.columns)):
        is_stationary = check_for_stationarity(data[data.columns[i]])
        if is_stationary is False:
            if calc_stationairty is True:
                temp_stationary_df = make_stationary(data[data.columns[i]])
            else:
                temp_stationary_df = data[data.columns[i]]

        else:
            temp_stationary_df = data[data.columns[i]]
        if smooth == 'None':
            if stationary_smoothed_df is None:
                #smoothed_model = SimpleExpSmoothing(temp_stationary_df, initialization_method="estimated").fit()

                #stationary_smoothed_df = pd.DataFrame(smoothed_model.fittedvalues, columns=[data.columns[i]])
                stationary_smoothed_df = pd.DataFrame(temp_stationary_df, columns=[data.columns[i]])
            else:
                stationary_smoothed_df[data.columns[i]] = temp_stationary_df

        elif smooth == 'Simple':
            if stationary_smoothed_df is None:
                smoothed_model = SimpleExpSmoothing(temp_stationary_df, initialization_method="estimated").fit()

                #tationary_smoothed_df = pd.DataFrame(smoothed_model.fittedvalues, columns=[data.columns[i]])
                stationary_smoothed_df = pd.DataFrame(temp_stationary_df, columns=[data.columns[i]])
            else:
                stationary_smoothed_df[data.columns[i]] = temp_stationary_df

    granger_df, lag = grangers_causation_matrix(stationary_smoothed_df, test='ssr_chi2test', variables=data.columns, verbose=False)
    #We shouldn't need the p_vals, but I am leaving them in a variable just in case
    optimal_p_vals = granger_df[data.columns[1] + str('_x')][data.columns[0] + str('_y')]
    return granger_df, lag

def get_optimal_lag(data, smooth='Simple', calc_stationairty=True):

    granger_df, lag = do_granger_causality(data, smooth, calc_stationairty)
    return lag

if __name__ == '__main__':

    stock_data = pd.read_csv('GOOG.csv')
    google_close_df = pd.DataFrame(stock_data['Close'], columns=['Close'])

    rng = np.random.default_rng()
    sentiment_df = pd.DataFrame(np.random.randint(-5, 5, size=(253, 1)).astype(float), columns=['Sentiment'])
    data_for_granger = google_close_df.copy()
    data_for_granger['Sentiment'] = sentiment_df
    lag = get_optimal_lag(data_for_granger, smooth='Simple')
    print(lag)
    #df, lag = do_granger_causality(data_for_granger, smooth='Simple')






