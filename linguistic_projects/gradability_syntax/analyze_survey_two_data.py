from make_survey_one import open_sheet
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import kruskal

def get_scale_data(survey_data: pd.DataFrame, path: str = "data/word_order_results.jpg"):
    """
    Generate a bar plot of mean preference ratings and save it to a file.

    :param survey_data: pd.DataFrame
        Survey data containing the Likert scale ratings.
    :param path: str
        File path to save the plot.
    """
    plt.clf()
    plt.figure(figsize=(9, 7))
    # Calculate the mean preference ratings for each description

    survey_data_averages = survey_data[['1', '2', '3', '4', '5']].mean()
    survey_data_averages = pd.DataFrame({'Rating': survey_data_averages.index, 'Average': survey_data_averages.values})

    ax = sns.barplot(data=survey_data_averages,
                     x='Rating',
                     y='Average',
                     color='steelblue')

    ax.set_xticklabels(["Strong Preference\nfor Alternate", "Slight Preference\nfor Alternate",
                        "No Preference\nfor Either",
                        "Slight Preference\nfor Scontras", "Strong Preference\nfor Scontras"])

    plt.xlabel('Rating')
    plt.ylabel('Average Preference Rating')
    plt.title('Mean Preference Ratings')

    # Show the plot
    plt.savefig(path)

def find_statistical_significance(category_1: list, category_2: list, neutral_category: list) -> tuple:
    """
        Perform the Kruskal-Wallis test to find statistical significance.

        :param category_1: list
            List of preference ratings for the category 1.
        :param neutral_category: list
            List of neutral preference ratings.
        :param category_2: list
            List of preference ratings for the category 2.
        ":return: tuple
            The test statistic and p_value
        """
    return kruskal(category_1, neutral_category, category_2)


if __name__ == '__main__':
    link = "https://docs.google.com/spreadsheets/d/1jxXRnLCp8mHE2MvJ5C8CwXuzFEj36_2tT0MFAaCtBp4/edit#gid=0"
    survey_sheet_name = "Word Order Preference"
    survey_data = open_sheet(link, survey_sheet_name)

    alt_preference = survey_data['1'].tolist() + survey_data['2'].tolist()
    neutral_preferences = survey_data['3'].tolist()
    scontras_preference = survey_data['4'].tolist() + survey_data['5'].tolist()

    statistic, p_value = find_statistical_significance(alt_preference, scontras_preference, neutral_preferences)

    get_scale_data(survey_data)

    print(f"Kruskall statistic: {statistic}")
    print(f"P-value: {p_value}")