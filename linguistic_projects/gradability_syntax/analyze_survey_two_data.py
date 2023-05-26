from make_survey_one import open_sheet
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import kruskal
from statistics import stdev as standard_deviation

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

if __name__ == '__main__':
    link = "https://docs.google.com/spreadsheets/d/1jxXRnLCp8mHE2MvJ5C8CwXuzFEj36_2tT0MFAaCtBp4/edit#gid=0"
    survey_sheet_name = "Word Order Preference"
    survey_data = open_sheet(link, survey_sheet_name)

    average = lambda values: round(sum(values) / len(values), 2)
    find_statistical_significance = lambda category_1, category_2, neutral_category: kruskal(category_1, neutral_category, category_2)

    # Participants that preferred the alternate word order
    alt_preference = survey_data['1'].tolist() + survey_data['2'].tolist()

    # Participants that preferred neither
    neutral_preference = survey_data['3'].tolist()

    # Participants that preferred the Scontras and Cinque word order
    scontras_preference = survey_data['4'].tolist() + survey_data['5'].tolist()

    mean_alt = average(alt_preference)
    sd_alt = standard_deviation(alt_preference)
    print("Alt_Preference (M: %.2f, SD: %.2f)\n" % (mean_alt, sd_alt))

    mean_neutral = average(neutral_preference)
    sd_neutral = standard_deviation(neutral_preference)
    print("Neutral_Preference (M: %.2f, SD: %.2f)\n" % (mean_neutral, sd_neutral))

    mean_scontras = average(scontras_preference)
    sd_scontras = standard_deviation(scontras_preference)
    print("Scontras_Preference (M: %.2f, SD: %.2f)\n" % (mean_scontras, sd_scontras))

    statistic, p_value = find_statistical_significance(alt_preference, scontras_preference, neutral_preference)
    print(f"Kruskall statistic: {statistic}")
    print(f"P-value: {p_value}")

    get_scale_data(survey_data)