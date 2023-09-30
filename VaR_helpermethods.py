import matplotlib.pyplot as plt
import numpy as np

# From an unsorted dollar price series with a given alpha and closeout period, calculate the Var
def calculate_var(price_timeseries_list, alpha, closeout_days):

    unsorted_percent_loss_series = []
    unsorted_dollar_loss_series = []

    for index in range(0, len(price_timeseries_list)):

        price_timeseries = price_timeseries_list[index]

        for entry_day in range(0, len(price_timeseries)-closeout_days):

            dollar_loss =  price_timeseries[entry_day]-price_timeseries[entry_day+closeout_days]

            percent_log_loss = np.log(price_timeseries[entry_day])-np.log(price_timeseries[entry_day+closeout_days])*100

            percent_loss = (price_timeseries[entry_day]-price_timeseries[entry_day+closeout_days])/price_timeseries[entry_day]*100

            unsorted_dollar_loss_series.append(dollar_loss)
            unsorted_percent_loss_series.append(percent_loss)

    sorted_dollar_loss_series = sorted(unsorted_dollar_loss_series, reverse=True)
    sorted_percent_loss_series = sorted(unsorted_percent_loss_series, reverse=True)
    sorted_percent_log_loss_series = sorted(unsorted_percent_loss_series, reverse=True)

    series_length = len(sorted_percent_loss_series)

    dollar_loss = sorted_dollar_loss_series[round(series_length*alpha)]
    percent_loss = sorted_percent_loss_series[round(series_length*alpha)]
    percent_log_loss = sorted_percent_log_loss_series[round(series_length * alpha)]

    return dollar_loss, percent_loss, percent_log_loss, sorted_dollar_loss_series, sorted_percent_loss_series, sorted_percent_log_loss_series

# From a sorted series and a given alpha, calculate the expected shortfall in dollars and percent
def calculate_expected_values(alpha, sorted_dollar_loss_series, sorted_percent_loss_series):

    var_length = round(len(sorted_percent_loss_series)*alpha)
    expected_dollar_loss = 0
    expected_percent_loss = 0

    for index in range(0, var_length):

        expected_dollar_loss = expected_dollar_loss + sorted_dollar_loss_series[index]
        expected_percent_loss = expected_percent_loss + sorted_percent_loss_series[index]

    expected_dollar_loss = expected_dollar_loss/var_length
    expected_percent_loss = expected_percent_loss/var_length

    return expected_dollar_loss, expected_percent_loss

# Plot the distribution of losses
def plot_var(alpha, closeout_days, dollar_loss, percent_loss, percent_log_loss, sorted_dollar_loss_series, sorted_percent_loss_series, sorted_percent_log_loss_series, bins, method, vol_multiplier):

    percent_graph = plt.figure(1)
    plt.title("Loss in Percent for " +str(closeout_days)+ " closeout day(s).")
    plt.xlabel("% Loss")
    plt.ylabel("Frequency")
    plt.hist(sorted_percent_loss_series, bins=bins, ec="black")
    plt.hist(sorted_percent_log_loss_series, bins=bins, ec="blue")
    plt.axvline(percent_loss)
    plt.savefig("Method" + method +"_alpha" +str(alpha) + "_closeout_days" +str(closeout_days) + "_percent_loss" +"_vol_multiplier" + str(vol_multiplier) +"_bins" + str(bins) +".png")

    dollar_graph = plt.figure(2)
    plt.title("Loss in Dollars for " +str(closeout_days)+ " closeout day(s).")
    plt.xlabel("$ Loss")
    plt.ylabel("Frequency")
    plt.hist(sorted_dollar_loss_series, bins=bins, ec="black")
    plt.axvline(dollar_loss)
    plt.savefig("Method" + method +"_alpha" +str(alpha) + "_closeout_days" +str(closeout_days) + "_dollar_loss" +"_bins" + str(bins) +".png")

    plt.show()

    return 0





