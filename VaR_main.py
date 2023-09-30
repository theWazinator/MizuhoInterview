from VaR_helpermethods import *
import pandas as pd
import numpy as np
from scipy.stats import norm
import copy

# Parameters - standard
alpha = 0.01
closeout_days = 1
price_type = 'Close'
hist_bins = 30
days = 730 # Number of days in a single trial (max 730 for historical)
method = 'historical'

# Parameters - Monte Carlo
tickers = ("COIN_Normalized", "S&P500", "BTCUSD", "DOGEUSD", "ETHUSD")
trials = 1000 # Number of trials to test
starting_day = 0 # Initial asset price
vol_multiplier = 5 # Multiplier of observed vol for risky scenarios
risk_free_rate = 0/365 # daily risk free rate

# Input data
raw_data = pd.read_csv(r"C:\Users\jacob\OneDrive\Documents\Jobs and Internships\2022\Mizuho\VaR_Data.csv")

# Loss calculation method
if method == "historical":

    raw_price_timeseries = list(raw_data['COIN_Normalized_' + price_type])[0:days]
    final_price_timeseries_list = [raw_price_timeseries]

elif method == "monte carlo":

    s_0 = [] # vector of starting prices (5x1)
    vol = [] # vector of volatility (5x1)
    corr_list = [] # correlation matrix (5x5)

    for ticker in tickers:

        open_price_timeseries =  raw_data[ticker + "_Open"].tolist()
        close_price_timeseries = raw_data[ticker + "_Close"].tolist()

        # Get starting price
        s_0.append(close_price_timeseries[starting_day])

        # Calculate volatility
        vol_sum = 0

        for index in range(0, len(open_price_timeseries)):
            daily_vol = abs(open_price_timeseries[index]-close_price_timeseries[index])/(open_price_timeseries[index]+close_price_timeseries[index])
            vol_sum = vol_sum + daily_vol

        vol_average = vol_sum/len(open_price_timeseries)
        vol.append(vol_average*vol_multiplier)

        # Enter price list into correlation matrix entry list
        corr_list.append(close_price_timeseries)

    # Calculation correlation matrix

    corr_matrix = np.corrcoef(corr_list)
    l_matrix = np.linalg.cholesky(corr_matrix)

    print("Initial Price")
    print(s_0)

    print("Volatility")
    print(vol)

    print("Correlation Matrix")
    print(corr_matrix)

    # Simulate 1,000 tries of two years of simulation
    final_price_timeseries_list = []
    for trial_count in range(0, trials):

        if trial_count%100 == 0:
            print("Trial " +str(trial_count)+ " completed.")

        cur_price = copy.copy(s_0) # Must copy the initial price to avoid pointer issues

        trial_dict = {}
        for index, ticker in enumerate(tickers):
            trial_dict[ticker] = [s_0[index]]

        for day in range(0, days-1):

            corr_vector = np.matmul(l_matrix, norm.rvs(size=len(tickers)))

            for index, ticker in enumerate(tickers):

                exponent = (risk_free_rate-vol[index]**2/2)*1+vol[index]*np.sqrt(1)*corr_vector[index]
                cur_price[index] = cur_price[index]*np.exp(exponent)
                trial_dict[ticker].append(cur_price[index])

        final_price_timeseries_list.append(trial_dict["COIN_Normalized"])

# For all methods

dollar_loss, percent_loss, percent_log_loss, sorted_dollar_loss_series, sorted_percent_loss_series, sorted_percent_log_loss_series = calculate_var(final_price_timeseries_list, alpha, closeout_days)
plot_var(alpha, closeout_days, dollar_loss, percent_loss, percent_log_loss, sorted_dollar_loss_series, sorted_percent_loss_series, sorted_percent_log_loss_series, hist_bins, method, vol_multiplier)
expected_dollar_loss, expected_percent_loss = calculate_expected_values(alpha, sorted_dollar_loss_series, sorted_percent_loss_series)

print("VaR of $"+ str(round(dollar_loss, 2))+ " (" +str(round(percent_loss, 2)) +r"%)")
print("Expected shortfall of $" +str(round(expected_dollar_loss, 2))+ " (" +str(round(expected_percent_loss, 2)) +r"%)")

print("Parameters")
print("Lookback period: " +str(days) +str(" days"))
print("Data points: " +str(len(final_price_timeseries_list)*len(final_price_timeseries_list[0])))
print("Alpha: " +str(alpha))
print("Closeout days: " +str(closeout_days))
print("Price Type: " +str(price_type))
print("Method: " +str(method))









