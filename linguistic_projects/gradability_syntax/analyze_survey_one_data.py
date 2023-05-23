from make_survey_one import open_sheet
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def get_data_from_survey(survey_data: pd.DataFrame, path: str = "data/faultless_results.jpg"):
    survey_data['percent_yes'] = survey_data['percent_yes'].str.replace("%", "").astype(float)

    # Determine the order of semantic categories based on the mean faultless disagreement ratings
    category_order = survey_data.groupby(['category', 'type'])['percent_yes'].mean().sort_values(ascending=False)
    category_order = category_order.reset_index()

    plt.figure(figsize=(15, 15))

    sns.set(font_scale=1.75)

    ax = sns.barplot(data=category_order,
                x='category',
                y='percent_yes',
                hue="type",
                order=category_order['category'].unique()
                )

    ax.set_xticklabels(ax.get_xticklabels(), rotation=40)
    plt.xlabel("Adjective Class")
    plt.ylabel("Mean Rate of Faultless Disagreement (Percentage)")
    plt.title("Predicted Adjective Order based on Mean Faultless Disagreement Rate")

    plt.savefig(path)

if __name__ == '__main__':
    # Preprocess the data from Google Sheets into a Pandas DataFrame
    link = "https://docs.google.com/spreadsheets/d/1jxXRnLCp8mHE2MvJ5C8CwXuzFEj36_2tT0MFAaCtBp4/edit#gid=0"
    suvery_sheet_name = "Faultless Disagreement"
    survey_data = open_sheet(link, suvery_sheet_name)

    # Visualize the Data
    get_data_from_survey(survey_data)