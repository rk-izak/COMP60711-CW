from unittest import result
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class SolutionsForCW2():
    # The following instructions must be followed to allow the University's automarking application to mark your code for Week 3's coursework, specifically Tasks 5.I and 6.I. Please, make sure you:
    # DO NOT change the names of existing attributes and functions they are required for the automatic marking to work
    # DO NOT use additional libraries, the automatic marking environment only supports pandas, numpy and matplotlib
    # DO NOT modify the dataset, the automatic marking environment will use its own copy of the dataset
    # You can do all the setup in the __init__ function
    # You can add any additional attributes and functions as you wish
    # when using matplotlib remember to comment out plt.show() before submitting, otherwise the program will hang and your work might not get marked
    # --------- END OF INSTRUCTIONS ----------------
    #
    #
    #
    # --------- START OF CODE SKELETON -------------
    #
    # You should place/paste your code below, combining it with the provided code skeleton.

    def __init__(self, file1="Datasets/rawpvr_2018-02-01_28d_1083_TueFri.csv",
                 file2="Datasets/rawpvr_2018-02-01_28d_1415_TueFri.csv") -> None:
        # CSV file is read into the dataset.

        # As we will be working with the pandas for ease of use, we automatically load the file as a df instance.
        self.file1 = pd.read_csv(file1)
        self.file2 = pd.read_csv(file2)

        # Check the attribues and general info about the dfs for later usage and possible manipulation.

        """
        print(self.file1.info()) -> result:

        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 503768 entries, 0 to 503767
        Data columns (total 10 columns):
        #   Column          Non-Null Count   Dtype  
        ---  ------          --------------   -----  
        0   Date            503768 non-null  object 
        1   Lane            503768 non-null  int64  
        2   Lane Name       503768 non-null  object 
        3   Direction       503768 non-null  int64  
        4   Direction Name  503768 non-null  object 
        5   Speed (mph)     503749 non-null  float64
        6   Headway (s)     493776 non-null  float64
        7   Gap (s)         489693 non-null  float64
        8   Flags           503768 non-null  int64  
        9   Flag Text       0 non-null       float64
        dtypes: float64(4), int64(3), object(3)
        memory usage: 38.4+ MB

        
        print(self.file2.info()) -> result:

        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 289078 entries, 0 to 289077
        Data columns (total 10 columns):
        #   Column          Non-Null Count   Dtype  
        ---  ------          --------------   -----  
        0   Date            289078 non-null  object 
        1   Lane            289078 non-null  int64  
        2   Lane Name       289078 non-null  object 
        3   Direction       289078 non-null  int64  
        4   Direction Name  289078 non-null  object 
        5   Speed (mph)     289071 non-null  float64
        6   Headway (s)     284020 non-null  float64
        7   Gap (s)         280697 non-null  float64
        8   Flags           289078 non-null  int64  
        9   Flag Text       0 non-null       float64
        dtypes: float64(4), int64(3), object(3)
        memory usage: 22.1+ MB
        """

        # Upon further inspection, it was noticed that the "Date" attribute does not follow the format "%Y-%m-%d %H:%M:%S"
        # in all of the df entries for both files, So, similarly as before (CW1) we need to manipulate its values and 
        # ensure consistency through deleting anything else after the specified format (miliseconds).

        # We can see that the "Date" attribute is in the string format, therefore we can go straight into cleaning.
        # We simply remove the milisecond part where present. We need to do this as inconsistencies in the 
        # attribute format could lead to later issues down the line in terms of data processing or visualisation.
        self.file1["Date"] = self.file1["Date"].apply(lambda x: x[:19] if len(x) > 19 else x)
        self.file2["Date"] = self.file2["Date"].apply(lambda x: x[:19] if len(x) > 19 else x)

        # Now convert the "clean" attribute to datetime object for easier time-based operations/visualizations in later tasks.
        self.file1["Date"] = pd.to_datetime(self.file1["Date"], format="%Y-%m-%d %H:%M:%S")
        self.file2["Date"] = pd.to_datetime(self.file2["Date"], format="%Y-%m-%d %H:%M:%S")

        # Additionally, all calls to specific columns have been checked through df["att_name"].unique() to ensure
        # that all relevant data is being extracted correctly and appropriately, and that no info is missing.
        
        # --------------------- START OF TASK 5 I ---------------------

        # We clear the initial df of entries not within our interested hours. As we have previously
        # set the "Date" attribute to be a datetime, we can perform the following.
        filtered_data_time_tuesdays = self.file1[self.file1["Date"].dt.hour.between(7, 18)]

        # Now we filter again, this time to include only Tuesdays.
        filtered_data_time_tuesdays = filtered_data_time_tuesdays[filtered_data_time_tuesdays["Date"].dt.dayofweek.isin([1])]

        # Now that our data has been filtered to just Tuesdays between 7-18, we can calculate
        # the attribute completeness using the formula as seen in the coursework sheet.

        # To do that, we need to calculate the count of non-nan values and divide it by the
        # total number of cells, which we then multiply by 100 to get the percentage, as seen below.
        self.gap_completeness_task_3_I = (filtered_data_time_tuesdays["Gap (s)"].count() / len(filtered_data_time_tuesdays)) * 100

        # ---------------------- END OF TASK 5 I ---------------------- 

        # -------------------- START OF TASK 5 II ---------------------
        # This section of code will be almost exclusively used for data profiling
        # through plotting, data manipulation, or other information extraction
        # to gain insight regarding the appropriate method of value filling.

        # First, we need to filter the data appropriately to focus on Tusedays only
        # between the hours of 7:00 and 18:59:59 o’clock, adjusting for NB_MID exclusively.

        # We have already cleaned the data to adjust for the first two points,
        # therefore we only need to filter out for the NB_MID lane.
        filtered_data_time_tuesdays_nb_mid = filtered_data_time_tuesdays[filtered_data_time_tuesdays["Lane Name"] == "NB_MID"]

        # Now, using pandas built-in function, let's check the ususal descriptive stats about the frame.
        # Additionally, let us calculate skewness and kurtosis to further investigate the distribution 
        # shape, sharpness of peaks, and weight of tails.
        """
        1) Descriptive Statistics:

        print(filtered_data_time_tuesdays_nb_mid["Gap (s)"].describe()) -> result:

        count    34002.000000
        mean         4.394434
        std          6.311024
        min          0.006000
        25%          1.400000
        50%          2.264000
        75%          4.249000
        max         88.080000
        Name: Gap (s), dtype: float64

        skew = filtered_data_time_tuesdays_nb_mid["Gap (s)"].skew()
        kurt = filtered_data_time_tuesdays_nb_mid["Gap (s)"].kurt()

        print(skew) -> result:
        3.909485207196796

        print(kurt) -> result:
        19.830603300963045
        """

        # Let's also make sure to check completeness for the NB_MID lane only (to make sure its similar to that of whole df).
        """
        2) Completeness of NB_MID.
        print((filtered_data_time_tuesdays_nb_mid["Gap (s)"].count() / len(filtered_data_time_tuesdays_nb_mid)) * 100) -> result:

        98.02519675959293
        """

        # To gain more insight, let us plot relevant graphs.

        # 3) Distribution Visualization through a histogram.
        plt.figure(figsize=(10,6))
        plt.hist(filtered_data_time_tuesdays_nb_mid["Gap (s)"], bins=150, density=False, alpha=0.6, color="blue")
        plt.title("NB_MID Gap (s) values distribution")
        plt.xlabel("Gap (s)")
        plt.ylabel("Frequency")
        # plt.savefig("task_5_II_histogram.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # 4) DDS Visualization through a set of boxplots.
        plt.figure(figsize=(10,6))
        # We need to drop NaN values to make sure to calculate required statistics.
        # Let's also draw for each unique date to visualize a more detailed spread.
        boxplot_uniq_dates = filtered_data_time_tuesdays_nb_mid["Date"].dt.date.unique()
        boxplot_data = [filtered_data_time_tuesdays_nb_mid[filtered_data_time_tuesdays_nb_mid["Date"].dt.date == date]["Gap (s)"].dropna().values \
                        for date in boxplot_uniq_dates]
        plt.boxplot(boxplot_data, vert=True, patch_artist=True, labels=boxplot_uniq_dates)
        plt.title("NB_MID Gap (s) values boxplot for each Tuesday")
        plt.ylabel("Gap (s)")
        plt.xlabel("Date")
        # plt.savefig("task_5_II_boxplot.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # 5) Scatter Plot Visualization using the function: Gap (s) = f(hour).
        plt.figure(figsize=(10,6))

        # Let's filter the data and add another column that corresponds to only the hour part 
        # of the "Date" attribute for easier plotting and analysis.
        filtered_data_time_tuesdays_nb_mid["Hour"] = pd.to_datetime(filtered_data_time_tuesdays_nb_mid["Date"]).dt.hour

        # Let's also generate x-axis values for easier plotting.
        tuesday_uniq_hours = filtered_data_time_tuesdays_nb_mid["Hour"].unique()

        # Generating plots for each hour.
        for hour in tuesday_uniq_hours:
            hour_subset = filtered_data_time_tuesdays_nb_mid[filtered_data_time_tuesdays_nb_mid["Hour"] == hour]
            plt.scatter([hour] * len(hour_subset), hour_subset["Gap (s)"].values, label=f"{hour}:00")

        plt.title("Scatter of Gap (s) values over relevant hours")
        plt.xlabel("Time of day")
        plt.ylabel("Gap (s)")
        plt.xticks(range(7, 19))
        plt.tight_layout()
        # plt.savefig("task_5_II_scatter.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # Let us also check the correlation factors between Gap (s) and Speed (mph)/Headway (s)/Hour assuming variableas as correlated, 
        # as these factors can help us possibly decide a better way of filling in values in the feature (using regression, etc.)

        # 6) Correlation factors (using Pearson).
        """
        correlation_speed = filtered_data_time_tuesdays_nb_mid["Gap (s)"].corr(filtered_data_time_tuesdays_nb_mid["Speed (mph)"])
        correlation_headway = filtered_data_time_tuesdays_nb_mid["Gap (s)"].corr(filtered_data_time_tuesdays_nb_mid["Headway (s)"])
        correlation_hour = filtered_data_time_tuesdays_nb_mid["Gap (s)"].corr(filtered_data_time_tuesdays_nb_mid["Hour"])
        
        print(correlation_speed) -> result:
        0.22363068233251607

        print(correlation_headway) -> result:
        0.8984908713039137

        print(correlation_hour) -> result:
        0.07794064687646104
        """

        # More methods, such as  z-scoring/feature importance using standarisation, or binning analysis could have been also
        # applied to further the insight into data. Yet, the methods above provide precise enough analysis
        # into the Gap (s) attribute. Therefore, we can conclude the profiling as complete.

        # --------------------- END OF TASK 5 II ----------------------

        # No code was generated for Task 5 III.

        # --------------------- START OF TASK 6 I ---------------------

        # Before we do any work, we need to filter the data according to speficiations.
        # As we are only interested in data from Fridays between 17:00 and 17:59:59, we do the following.

        # Get only Friday data for two datasets.
        site_1083_friday = self.file1[self.file1["Date"].dt.dayofweek == 4]
        site_1415_friday = self.file2[self.file2["Date"].dt.dayofweek == 4]

        # Now, we filter by the requested hours.
        site_1083_friday = site_1083_friday[site_1083_friday["Date"].dt.hour == 17]
        site_1415_friday = site_1415_friday[site_1415_friday["Date"].dt.hour == 17]

        # And finally, we filter by the North direction (of value 1, south is 2).
        site_1083_friday = site_1083_friday[site_1083_friday["Direction"] == 1]
        site_1415_friday = site_1415_friday[site_1415_friday["Direction"] == 1]

        # Let's see the completeness of speed columns for each dataframe.
        site_1083_speed_completeness = (site_1083_friday["Speed (mph)"].count() / len(site_1083_friday)) * 100
        site_1415_speed_completeness = (site_1415_friday["Speed (mph)"].count() / len(site_1415_friday)) * 100

        """
        print(site_1083_speed_completeness) -> result:
        100.0

        print(site_1415_speed_completeness) -> result:
        100.0
        """
        
        # We see that we are not missing any values in the filtered sets, now let us see some basic DDS measures.
        """"
        print(site_1083_friday["Speed (mph)"].describe()) -> result:

        count    9950.000000
        mean       27.885475
        std         7.525883
        min         1.244000
        25%        24.233000
        50%        28.584000
        75%        32.310000
        max        69.593000
        Name: Speed (mph), dtype: float64


        print(site_1415_friday["Speed (mph)"].describe()) -> result:

        Name: Speed (mph), dtype: float64
        count    5083.000000
        mean       25.540278
        std         8.344289
        min         1.244000
        25%        20.506000
        50%        26.098000
        75%        31.069000
        max        61.516000
        Name: Speed (mph), dtype: float64
        """

        # We see that these sets have almost exactly the same attributes, therefore we do not
        # need to normalize any of these with respect to other for better representation.
        # It also means the trends/behavior from one site are almost equivalent to the other.

        # Now, to extend our understanding, let us generate relevant plots.

        # Speed boxplots for both sites.
        # Site 1083.
        plt.figure(figsize=(10,6))
        plt.boxplot(site_1083_friday["Speed (mph)"], vert=True, patch_artist=True)
        plt.title("North Lanes Speed (mph) values boxplot for site 1083")
        plt.ylabel("Speed (mph)")
        # plt.savefig("task_6_I_boxplot_1083.png", dpi=300, bbox_inches="tight")

        # Site 1415
        plt.figure(figsize=(10,6))
        plt.boxplot(site_1415_friday["Speed (mph)"], vert=True, patch_artist=True)
        plt.title("North Lanes Speed (mph) values boxplot for site 1415")
        plt.ylabel("Speed (mph)")
        # plt.savefig("task_6_I_boxplot_1415.png", dpi=300, bbox_inches="tight")
        
        # Speed histograms for both sites.
        # Site 1083.
        plt.figure(figsize=(10,6))
        plt.hist(site_1083_friday["Speed (mph)"], bins=150, density=False, alpha=0.6, color="blue")
        plt.title("North Lanes Speed (mph) values distribution for site 1083")
        plt.xlabel("Speed (mph)")
        plt.ylabel("Frequency")
        # plt.savefig("task_6_I_histogram_1083.png", dpi=300, bbox_inches="tight")

        # Site 1415.
        plt.figure(figsize=(10,6))
        plt.hist(site_1415_friday["Speed (mph)"], bins=150, density=False, alpha=0.6, color="blue")
        plt.title("North Lanes Speed (mph) values distribution for site 1415")
        plt.xlabel("Speed (mph)")
        plt.ylabel("Frequency")
        # plt.savefig("task_6_I_histogram_1415.png", dpi=300, bbox_inches="tight")

        # Now, based on the DDS and above graphs, it was decided to remove all values 
        # over 50, as they are extreme outliers, and their introduction would taint
        # the goal of representing the average trend within those sites.

        site_1083_friday = site_1083_friday[site_1083_friday["Speed (mph)"] < 50]
        site_1415_friday = site_1415_friday[site_1415_friday["Speed (mph)"] < 50]

        # Now, the appropriate way of calculating the mean of two sets of different sizes,
        # is to combine the sets together and calculate their mean. We can also calculate each
        # mean individually, and used a weighed mean method based on sizes to get that result as well.
        # If we calculate two means, add them together and divide by two, we will produce inaccurate results
        # due to different weights (sizes) that will not be valid representations of the attribute at hand.

        # First, we get the mean of combined sets.
        site_1083_and_1415_speed_mean = pd.concat([site_1083_friday["Speed (mph)"], site_1415_friday["Speed (mph)"]]).mean()

        """
        Now, to demonstrate, let's see if we calculated means of each set seperately and then divided the sum by two.

        site_1083_speed_mean = site_1083_friday["Speed (mph)"].mean()
        site_1415_speed_mean = site_1415_friday["Speed (mph)"].mean()
        
        Now, when we check the respective methods, we get the following values.
        print((site_1083_speed_mean + site_1415_speed_mean)/2) -> result:
        26.712876279152994

        print(site_1083_and_1415_speed_mean) -> result:
        27.092510144349095

        We can clearly see that those values are different. This is due to not weighing each value with respect to its set size.
        """

        # Now, as the speed mean is in [miles/h], we need to convert it to [km/h] through a convert constant.
        site_1083_and_1415_speed_mean *= 1.609344

        # Now, we can calculate the JT using provided equation.
        site_1083_and_1415_dist = 4.86 # in [km]
        jt_in_hours = site_1083_and_1415_dist / site_1083_and_1415_speed_mean

        # Now, because our JT is in [hours], we need to convert it to minutes through a simple conversion.
        self.avgJT_task_6_I = jt_in_hours * 60

        # ---------------------- END OF TASK 6 I ----------------------
        

    def task_5_I(self) -> float:
        return self.gap_completeness_task_3_I

    def task_6_I(self) -> float:
        return self.avgJT_task_6_I

# Used for testing purposes.
# if __name__ == "__main__":
#     test = SolutionsForCW2()
#     print("Task 3 I")
#     print(test.task_5_I())
#     print("="*30)
#     print("Task 6 I")
#     print(test.task_6_I())