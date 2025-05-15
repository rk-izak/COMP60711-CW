import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class SolutionsForCW1:

    # --------- START OF INSTRUCTIONS --------------------
    # The following instructions must be followed to allow the University's automarking application to mark your code for Week 2's coursework, specifically Tasks 2.I, 2.II, 2.III and 3.I. Please, make sure you:
    #
    # (1) DO NOT change the names of the provided attributes and functions as they are required for the automatic marking to work. These are shown in the provided code skeleton, which given at the bottom of this file, following all the instructions provided in this file (as comments), as well as in the class name shown above (i.e., 'class SolutionsForCW1').
    #
    # (2) DO NOT use any additional libraries, given that the automatic marking environment only supports pandas, numpy and matplotlib.
    #
    # (3) DO NOT modify the dataset, given that the automatic marking environment will use its own copy of the dataset, which is the one provided to you via Blackboard.
    #
    # (4) You can do all the setup in the __init__ function.
    #
    # (5) You can add any additional attributes and function as required.
    #
    # (6) When using matplotlib, remember to comment out plt.show() before submitting, otherwise the program will hang and your work might not get automatically marked.
    #
    # (7) Use this single file for all the Python code you have developed for the coursework, i.e., for all of Tasks 2.I, 2.II, 2.III and 3.I. 
    #
    # Please, make sure you return the result of each task as a dictionary, as shown in the two dictionary templates shown below. 
    #
    # To build the dictionary for each of Tasks 2.I, 2.II and 2.III, you must do (a) and (b), described below. Note that 'VALUE' should be replaced with the value your Python code calculates for each DDS measure.
    #
    #    (a) use the code given in the coursework description document to represent each of the DDS measures, as suggested below, (i.e., "R" for Range, "Q1" for 1st Quartile, "Q2" for 2nd Quartile, "Q3" for 3rd Quartile, and "IQR" for Interquartile Range.
    #    (b) use the name of each of the lanes, exactly as found in the CSV data file (i.e., "SB_NS", "SB_MID", "SB_OS","NB_NS","NB_MID","NB_OS"). 
    # 
    #
    # for task II
    # {
    #     "R": {"NAME_OF_LANE_1": VALUE,
    #          "NAME_OF_LANE_2": VALUE,
    #           ...}
    #     "Q1": {"NAME_OF_LANE_1": VALUE,
    #          "NAME_OF_LANE_2": VALUE,
    #           ...},
    #     ...
    # }
    #
    #
    #To build the dictionary for Task 3.I, you must do (a) and (b), described below. Note that 'VALUE' should be replaced with the value your Python code calculates for each hourly traffic volume.
    #
    #    (a) use integers to refer to each of the hours of the day specified in the coursework description document as suggested below, (i.e., 7 for 7:00:00, 8 for 8:00:00, ... .
    #    (b) use "Tuesday" and "Friday" to refer to the weekdays.
    #
    #
    # for task III
    # {
    #     "Tuesday": {7: VALUE,
    #                 8: VALUE,
    #                 ...}
    #     "Friday": {7: VALUE,
    #                8: VALUE,
    #               ...},
    # }
    #
    #
    # Note that, if it helps, you can convert a dataframe to a dictionary using .to_dict()
    #
    # --------- END OF INSTRUCTIONS ----------------
    #
    #
    #
    # --------- START OF CODE SKELETON -------------
    #
    # You should place/paste your code below, combining it with the provided code skeleton.


    def __init__(self, file="Datasets/rawpvr_2018-02-01_28d_1083_TueFri.csv"):
        # 
        # For the automatic marking to work you need to load the data using the `file` variable - the one you see in the above line of code.

        # As we will be working with the pandas for ease of use, we automatically load the file as a df instance.
        self.file = pd.read_csv(file)

        # Check the attribues and general info about the df for later usage and possible manipulation.

        """
        print(self.file.info()) -> result:

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
        """

        # Upon further inspection, it was noticed that the "Date" attribute does not follow the format "%Y-%m-%d %H:%M:%S"
        # in all of the df entries, therefore we need to manipulate its values and ensure consistency through deleting
        # anything else after the specified format (miliseconds).

        # As we can see, the "Date" attribute is already in string format.
        # If it was not, we could have used the following to ensure consistency (in case it was datetime):
        # self.file["Date"] = self.file["Date"].astype(str)

        # Now, we simply remove the milisecond part where present. We need to do this as inconsistencies in the 
        # attribute format could lead to later issues down the line in terms of data processing or visualisation.
        self.file["Date"] = self.file ["Date"].apply(lambda x: x[:19] if len(x) > 19 else x)

        # Now convert the "clean" attribute to datetime object for easier time-based operations/visualizations in later tasks.
        self.file["Date"] = pd.to_datetime(self.file["Date"], format="%Y-%m-%d %H:%M:%S")

        # We create a filtering mask based on the specified criteria of Task 2 to only account for 
        # Tuesdays between 09:00 am and 09:59:59 am and the chosen Direction Name (North/South) in the analysis. 
        def get_mask_t2(df: pd.DataFrame, direction: str) -> pd.Series:
            mask = (
                (df["Date"].dt.weekday == 1)  # Tuesday is represented by 1
                & (df["Date"].dt.time >= pd.to_datetime("09:00:00").time())
                & (df["Date"].dt.time <= pd.to_datetime("09:59:59").time())
                & (df["Direction Name"] == direction)
            )
            return mask

        # We retrieve specified DDS attributes (Range  (R),  1st Quartile (Q1), 2nd Quartile (Q2), 3rd Quartile (Q3), 
        # and Interquartile Range (IQR)) and output a df with lane names for the previously chosen direction.
        def get_dds_by_attribute_t2(df: pd.DataFrame, att: str) -> pd.DataFrame:

            # Initalize a dummy dataframe to be later filled with DDS values.
            dds = pd.DataFrame(columns=["Lane Name", "R", "Q1", "Q2", "Q3", "IQR"])
            
            for lane_name, entries in zip(df["Lane Name"], df[att]):
                # As some entries are not of the required float type (2 for the North direction for example)
                # we filter through checking the instance and isnan method. We do this to further ensure only
                # valid values are analysed and to keep data integrity.
                # As the number of missing entries is small, we can simply discard them; if that number
                # was greater, we should strive for more sophisticated methods of filling in missing values.
                entries = [entry for entry in entries if not np.isnan(entry)]
                
                # Acquire specified DDS measures through the NumPy library and fill the df.
                range = np.max(entries) - np.min(entries)
                q1 = np.percentile(entries, 25)
                q2 = np.percentile(entries, 50)
                q3 = np.percentile(entries, 75)
                iqr = q3 - q1
                dds.loc[len(dds.index)] = [lane_name, range, q1, q2, q3, iqr]
            return dds

        # Change the df format for a given attribute into the required dict format for task 2 automatic marking.
        def change_ans_format_t2(dds: pd.DataFrame, att: str) -> dict:
            ans_dict = {}
            for column in dds.columns:
                if column != att:
                    ans_dict[column] = dict(zip(dds[att], dds[column]))
            return ans_dict
        
        # -------------------- START OF TASK 2 I --------------------

        # We filter the df by applying previously established rules in the 
        # mask function and the "Direction Name" attribute.
        mask_north = get_mask_t2(self.file, "North")
        filtered_data_north = self.file[mask_north]

        # Now we group by "Lane Name" and aggregate by speeds for later DDS extraction.
        grouped_by_lane_north = filtered_data_north.groupby("Lane Name")["Speed (mph)"].agg(list).reset_index()

        # We retrieve the DDS measures and start the visulisation process for descriptive tasks.
        dds_speed_north = get_dds_by_attribute_t2(grouped_by_lane_north, "Speed (mph)")

        # Saving the df as dict for automatic marking.
        self.task_2_I_answer = change_ans_format_t2(dds_speed_north, "Lane Name")

        # Plotting box plots for speeds of north lanes.
        # Later refered to as Figure 1.
        # Commented out for automatic grading purposes.
        _, ax = plt.subplots()

        # Prepare data for plotting (deleting nans).
        speeds_north = [list(filter(lambda x: not np.isnan(x), speed_list)) 
                for speed_list in grouped_by_lane_north["Speed (mph)"]]

        # Plot boxplots, add labels and title.
        ax.boxplot(speeds_north)
        ax.set_xticklabels(grouped_by_lane_north["Lane Name"])
        ax.set_title("Box plot of Speeds for each North Lane")
        ax.set_ylabel("Speed (mph)")
        # plt.savefig("task_2_I_boxplot.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # --------------------- END OF TASK 2 I ----------------------

        # -------------------- START OF TASK 2 II --------------------
        # As the Task 2 II has the exact same procedure as Task 2 I, 
        # we repeat the steps, changing only the "Direction Name". 

        mask_south = get_mask_t2(self.file, "South")
        filtered_data_south= self.file[mask_south]
        grouped_by_lane_south = filtered_data_south.groupby("Lane Name")["Speed (mph)"].agg(list).reset_index()
        dds_speed_south = get_dds_by_attribute_t2(grouped_by_lane_south, "Speed (mph)")
        self.task_2_II_answer = change_ans_format_t2(dds_speed_south, "Lane Name")

        # Plotting box plots for speeds of south lanes.
        # Later refered to as Figure 2.
        # Commented out for automatic grading purposes.
        _, ax = plt.subplots()

        # Prepare data for plotting (deleting nans).
        speeds_south = [list(filter(lambda x: not np.isnan(x), speed_list)) 
                for speed_list in grouped_by_lane_south["Speed (mph)"]]
        ax.boxplot(speeds_south)
        ax.set_xticklabels(grouped_by_lane_south["Lane Name"])
        ax.set_title("Box plot of Speeds for each South Lane")
        ax.set_ylabel("Speed (mph)")
        # plt.savefig("task_2_II_boxplot.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # --------------------- END OF TASK 2 II ----------------------

        # -------------------- START OF TASK 2 III --------------------
        # Using the North lane as the example, we take the previously 
        # filtered tables and concat them to save both our time and computation time.
        filtered_data_north_south = pd.concat([filtered_data_north, filtered_data_south])

        # We normalize the dates to the  "%Y-%m-%d format to obtain a Traffic Volume Series 
        # for each Tuesday of the month for each unique lane which will enable us to perform DDS.
        filtered_data_north_south["Date"] = filtered_data_north_south["Date"].dt.normalize()
        filtered_data_north_south = filtered_data_north_south.groupby(["Date", "Lane Name"]).size().reset_index(name="row_count")

        # Making sure we keep the int datatype, as it might have been changed during operations.
        # It is also necessary for the get_dds... function to keep the datatype integrity.
        filtered_data_north_south["row_count"] = filtered_data_north_south["row_count"].astype(int)

        # Moving the row count for each Lane and each Tuesday into a list and storing it for that lane in a "Volume" column; 
        # we do this to utilize the previously used function as well for easier data access and reading.
        filtered_data_north_south = filtered_data_north_south.groupby("Lane Name")["row_count"].apply(list).reset_index()
        filtered_data_north_south.columns = ["Lane Name", "Volume"]
        dds_volume_north_south = get_dds_by_attribute_t2(filtered_data_north_south, "Volume")

        # Saving the df as dict for automatic marking.
        self.task_2_III_answer = change_ans_format_t2(dds_volume_north_south, "Lane Name")
        
        # Plotting box plots for speeds of north lanes.
        # Later refered to as Figure 3.
        # Commented out for automatic grading purposes.
        _, ax = plt.subplots()

        # Plot boxplots, add labels and title.
        ax.boxplot(filtered_data_north_south["Volume"].tolist())
        ax.set_xticks(range(1, len(filtered_data_north_south["Lane Name"]) + 1))
        ax.set_xticklabels(filtered_data_north_south["Lane Name"].tolist())
        ax.set_title("Box plots of Traffic Volume for each North and South lane")
        ax.set_ylabel("Traffic Volume")
        # plt.savefig("task_2_III_boxplot.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # --------------------- END OF TASK 2 III ---------------------


        # --------------------- START OF TASK 3 I ---------------------

        # Firstly, we clear the initial df of entries not within our interested hours. As we have previously
        # set the "Date" attribute to be a datetime, we can perform the following.
        filtered_data_time_all = self.file[self.file["Date"].dt.hour.between(7, 23)]

        # Now we filter again, this time to include only Tuesdays and Fridays.
        filtered_data_time_all = filtered_data_time_all[filtered_data_time_all['Date'].dt.dayofweek.isin([1, 4])]

        # We add additional column "Hour" by extracting it from the datetime object
        # for easier formatting and storing answers down later on.
        filtered_data_time_all["Hour"] = filtered_data_time_all["Date"].dt.hour

        # We obtain the number of Fridays and Tuesdays to get the average later on.
        # Although it should be equal to 4, it is better to sanity check anyways.
        no_of_tuesdays = filtered_data_time_all[filtered_data_time_all["Date"].dt.dayofweek == 1]["Date"].dt.date.nunique()
        no_of_fridays = filtered_data_time_all[filtered_data_time_all["Date"].dt.dayofweek == 4]["Date"].dt.date.nunique()

        # Now, knowing each row represent one vehicle, we can group by the established "Hour" and day of the
        # week, count the resultant rows, and calculate an average for each hour.
        filtered_data_time_all = filtered_data_time_all.groupby(["Hour", filtered_data_time_all["Date"].dt.dayofweek]).size().unstack(fill_value=0)
        filtered_data_time_all["Tuesday"] = filtered_data_time_all[1] / no_of_tuesdays
        filtered_data_time_all["Friday"] = filtered_data_time_all[4] / no_of_fridays

        # We remove the columns which correspond to total volumes.
        filtered_data_time_all.drop(columns=[1, 4], inplace=True)

        # Make sure the hours are set as integers.
        filtered_data_time_all.index = filtered_data_time_all.index.astype(int)

        # Plotting histograms to see the Traffic Volume per each hour.
        # Later refered to as Figure 4.
        # Commented out for automatic marking purposes.
        _ = filtered_data_time_all.plot(kind="bar", figsize=(12, 6), color=["blue", "orange"])
        plt.title("Average Traffic Volume for Tuesday and Friday")
        plt.xlabel("Hour")
        plt.ylabel("Frequency")
        plt.legend(title="Day of the Week")
        plt.tight_layout()
        # plt.savefig("task_3_I_historgam.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # Plotting boxplots to see the Traffic Volume per each day.
        # Later refered to as Figure 5.
        # Commented out for automatic marking purposes.
        _, ax = plt.subplots()

        # Prepare required data for box-plotting.
        box_plot_data = [filtered_data_time_all["Tuesday"],
                        filtered_data_time_all["Friday"]]
        # Plot boxplots, add labels and title.
        ax.boxplot(box_plot_data)
        ax.set_xticks([1, 2])
        ax.set_xticklabels(["Tuesday", "Friday"])
        ax.set_title("Box plot of Traffic Volume for Tuesday and Friday (7:00 to 23:59)")
        ax.set_ylabel("Traffic Volume")
        # plt.savefig("task_3_I_boxplot.png", dpi=300, bbox_inches="tight")
        # plt.show()

        # Saving the df as dict for automatic marking.
        self.task_3_I_answer = filtered_data_time_all.to_dict(orient="dict")

        # ---------------------- END OF TASK 3 I ----------------------

    def task_2_I(self) -> dict:
        return self.task_2_I_answer

    def task_2_II(self) -> dict:
        return self.task_2_II_answer

    def task_2_III(self) -> dict:
        return  self.task_2_III_answer

    def task_3_I(self) -> dict:
        return self.task_3_I_answer

# Used for personal testing purposes.
# if __name__ == "__main__":
#     test = SolutionsForCW1()
#     print("Task 2 I")
#     print(test.task_2_I())
#     print("="*30)
#     print("Task 2 II")
#     print(test.task_2_II())
#     print("="*30)
#     print("Task 2 III")
#     print(test.task_2_III())
#     print("="*30)
#     print("Task 3 I")
#     print(test.task_3_I())