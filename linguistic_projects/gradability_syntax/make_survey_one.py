import sys
import os
import pkg_resources
import subprocess

# Get the absolute path of the current script
script_path = os.path.dirname(os.path.abspath(__file__))
script_path = '/'.join(script_path.split('/')[:-2])

# Construct the relative path to the module
module_path = os.path.join(script_path, 'helpful_modules')

# Add the relative path to the sys.path list
sys.path.append(module_path)

def check_dependencies(dependencies_file):
    with open(dependencies_file) as f:
        dependencies = f.read().splitlines()

    # Check if dependencies are installed
    missing_dependencies = []
    for dependency in dependencies:
        try:
            pkg_resources.get_distribution(dependency)
        except pkg_resources.DistributionNotFound:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print("Installing missing dependencies...")
        install_command = ["pip", "install", "-r", dependencies_file]
        subprocess.run(install_command, check=True)
        print("Dependencies installed.")

# Check that all dependencies are present for the imported module from another directory
dependencies_file = os.path.join(module_path, "requirements.txt")
check_dependencies(dependencies_file)

import pandas as pd
import string, os, random, re
from google_drive import GoogleSheetsAPI, GoogleDriveAPI
import matplotlib.pyplot as plt

def count_syllables(word):
    """
    Count the number of syllables in a word using the syllable counting algorithm.

    :param word: str
        The word to count syllables for.
    :return: int
        The number of syllables in the word.
    """
    word = word.lower()
    if word == "i":
        return 1

    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1

    if word.endswith('e'):
        count -= 1

    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1

    return count

def is_word_with_multiple_syllables(word):
    """
    Check if a word has multiple syllables.

    :param word: str
        The word to check.
    :return: bool
        True if the word has multiple syllables, False otherwise.
    """
    syllable_count = count_syllables(word)
    if syllable_count > 1:
        return True
    else:
        return False

def get_adjective_modifier(adjective):
    """
    Get the comparative form of an adjective.

    :param adjective: str
        The adjective to modify.
    :return: str
        The modified adjective.
    """
    result = is_word_with_multiple_syllables(adjective)
    if result:
        return f"more {adjective}"
    else:
        if adjective == "best":
            return "better"
        elif re.search("e$", adjective):
            return f"{adjective}r"
        else:
            return f"{adjective}er"

def random_string(cls: list, seed: int = None) -> str:
    """
    Get a random string from a list.

    :param cls: list
        The list of strings.
    :param seed: int
        The seed value to initialize the random number generator.
    :return: str
        A random string from the list.
    """
    random.seed(seed)
    return random.choice(cls)

def create_phrases(nouns: list, adjective: str, seed: int = None) -> str:
    """
    Create phrases using an adjective and a list of nouns.

    :param nouns: list
        The list of nouns to choose from.
    :param adjective: str
        The adjective to use in the phrases.
    :param seed: int
        The seed value to initialize the random number generator.
    :return: str
        A phrase combining the adjective and a noun.
    """
    noun = random_string(nouns, seed=seed)
    return write_phrase(adjective, noun)

def write_phrase(adjective: str, noun: str) -> str:
    """
    Write a phrase using an adjective and a noun.

    :param adjective: str
        The adjective to use in the phrase.
    :param noun: str
        The noun to use in the phrase.
    :return: str
        The constructed phrase.
    """
    adjective = get_adjective_modifier(adjective)
    phrase = f"""Mary thinks this {noun} is {adjective} than that {noun}.
John doesn't think so.
Can they both be right or must one be wrong?"""
    return phrase

def get_samples(df, sample_size=45, all_categories=True, random_state=None):
    """
    Get a sample of data from a DataFrame.

    :param df: pd.DataFrame
        The DataFrame to sample from.
    :param sample_size: int
        The size of the sample.
    :param all_categories: bool
        Whether to sample from all categories or only specific categories.
    :param random_state: int
        The random seed for reproducible sampling.
    :return: pd.DataFrame
        The sampled data.
    """
    sampled_data = pd.DataFrame()
    if all_categories:
        category_samples = df['category'].value_counts(normalize=True) * sample_size
        type_samples = df.loc[df['category'].isin(category_samples.index)]['type'].value_counts(
            normalize=True) * sample_size
        for type in type_samples.index:
            type_data = df[df['type'] == type] \
                .sample(int(type_samples[type]),
                        random_state=random_state)
            sampled_data = pd.concat([sampled_data, type_data], ignore_index=True)
    else:
        category_samples = df.loc[df['category'].isin(['age', 'physical'])]['category'].value_counts(
            normalize=True) * sample_size
    for category in category_samples.index:
        category_data = df[df['category'] == category] \
            .sample(int(category_samples[category]),
                    random_state=random_state)
        sampled_data = pd.concat([sampled_data, category_data], ignore_index=True)
    return sampled_data

def get_data(df: pd.DataFrame, cls: str, animate=False, sample=False, sample_size=45, random_state=None) -> list:
    """
    Get data from a DataFrame based on the class.

    :param df: pd.DataFrame
        The DataFrame to extract data from.
    :param cls: str
        The class of words to retrieve.
    :param animate: bool
        Whether the words should be animate.
    :param sample: bool
        Whether to sample the data.
    :param sample_size: int
        The size of the sample.
    :param random_state: int
        The random seed for reproducible sampling.
    :return: list
        A list of words that match the specified criteria.
    """
    if sample:
        df = get_samples(df, sample_size, random_state=random_state)
    if animate:
        return df.loc[(df['class'] == cls) & (df['animate'] == True)]['word'].tolist()
    return df.loc[(df['class'] == cls)]['word'].tolist()

def write_questions(sheet, n=45, random_state=None):
    """
    Write survey questions based on the sheet.

    :param sheet: pd.DataFrame
        The sheet containing the data.
    :param n: int
        The number of questions to write.
    :param random_state: int
        The random seed for reproducible question selection.
    :return: list
        A list of generated phrases along with their category and type.
    """
    animate_nouns = get_data(sheet, 'noun', animate=True)
    all_nouns = get_data(sheet, 'noun')
    adjectives = get_data(sheet, 'adjective', sample=True, random_state=random_state)
    phrases = []
    for adjective in adjectives[:n]:
        animate = sheet.loc[sheet['word'] == adjective]['animate'].values[0]
        if animate:
            phrase = create_phrases(animate_nouns, adjective)
        else:
            phrase = create_phrases(all_nouns, adjective)
        category, type = sheet.loc[sheet['word'] == adjective][['category', 'type']].values.tolist()[0]
        phrases.append((phrase, category, type))
    return phrases

def open_sheet(link: str, worksheet_name: str) -> pd.DataFrame:
    """
    Open a Google Sheet and convert it to a DataFrame.

    :param link: str
        The link to the Google Sheet.
    :param worksheet_name: str
        The name of the worksheet to open.
    :return: pd.DataFrame
        The converted DataFrame.
    """
    return GoogleSheetsAPI(link, worksheet_name=worksheet_name).open_csv()

def write_new_sheet(link: str, worksheet_name: str, df: pd.DataFrame):
    """
    Write a new sheet to Google Drive.

    :param link: str
        The link to the Google Sheet.
    :param worksheet_name: str
        The name of the worksheet to write.
    :param df: pd.DataFrame
        The DataFrame to write.
    """
    try:
        GoogleSheetsAPI(link).new_sheet(worksheet_name, df, format_sheet=False)
    except:
        GoogleSheetsAPI(link).update_sheet(worksheet_name, df, format_sheet=False)

def new_data(data: dict = {}, **kwargs):
    """
    Add new data to a dictionary.

    :param data: dict
        The dictionary to add the data to.
    :param kwargs: dict
        The data to add, with keys as the data names and values as the data values.
    """
    for key, value in kwargs.items():
        if key in data.keys():
            data[key].append(value)
        else:
            data[key] = [value]

def get_letter(i):
    """
    Get the letter representation for a given index.

    :param i: int
        The index to get the letter for.
    :return: str
        The letter representation.
    """
    letters = [letter for letter in string.ascii_uppercase]
    if i+1 not in range(len(letters)):
        if i in range(len(letters) * 2):
            i -= len(letters)
            letter = "A" + letters[i]
        else:
            i -= len(letters) * 2
            letter = "B" + letters[i]
    else:
        letter = letters[i + 1]
    return letter

def check_sample_size(sheet_1: pd.DataFrame, sheet_2: pd.DataFrame):
    """
    Compares sampled stimuli with larger set and plots them to ensure that the samples pulled are representative.

    :param sheet_1: pd.DataFrame
        Original set of stimuli
    :param sheet_2: pd.DataFrame
        Sampled set of stimuli
    """
    plt.clf()
    sheet_1_category = sheet_1.loc[sheet_1['class']=='adjective']['category'].value_counts()
    sheet_2_category = sheet_2['category'].value_counts()
    sheet_1_type = sheet_1.loc[sheet_1['class']=='adjective']['type'].value_counts()
    sheet_2_type = sheet_2['type'].value_counts()

    # combine counts into a single DataFrame and fill NaN values with 0
    counts_1 = pd.concat([sheet_1_category, sheet_2_category], axis=1).fillna(0)
    counts_2 = pd.concat([sheet_1_type, sheet_2_type], axis=1).fillna(0)

    # calculate percentage of total for each category and type
    counts_pct_1 = counts_1.apply(lambda x: x / x.sum())
    counts_pct_2 = counts_2.apply(lambda x: x / x.sum())

    # plot the resulting distributions
    plt.figure()
    counts_pct_1.plot(kind='bar', figsize=(10, 6))
    plt.xticks(rotation=45)
    plt.savefig("data/category_distribution.jpg")

    plt.figure()
    counts_pct_2.plot(kind='bar', figsize=(10, 6))
    plt.xticks(rotation=45)
    plt.savefig("data/type_distribution.jpg")

def make_directory_if_not_exist(path):
    os.makedirs(path, exist_ok=True)

if __name__ == '__main__':
    link = "https://docs.google.com/spreadsheets/d/1jxXRnLCp8mHE2MvJ5C8CwXuzFEj36_2tT0MFAaCtBp4/edit#gid=0"
    stimuli_worksheet_name = "adjectives_to_combine"
    survey_worksheet_name = "Faultless Disagreement"
    sheet = open_sheet(link, stimuli_worksheet_name)
    sheet['animate'] = sheet['animate'].map({'TRUE': True, 'FALSE': False})
    phrases = write_questions(sheet, random_state=145)
    survey_data = {}
    i = 0
    for phrase, category, type in phrases:
        letter = get_letter(i)
        new_data(survey_data,
                 question_type='multiple choice',
                 phrase=phrase,
                 option_1='They can both be right.',
                 option_2='One of them must be wrong.',
                 required=True,
                 category=category,
                 type=type,
                 yes=f'COUNTIF(Faultless_Disagreement_Answers!{letter}:{letter}, "They can both be right.")',
                 no=f'COUNTIF(Faultless_Disagreement_Answers!{letter}:{letter}, "One of them must be wrong.")',
                 total=f"SUM(H{i + 2},I{i + 2})",
                 percent_yes=f'H{i + 2}/J{i + 2}')
        i += 1
    survey_data = pd.DataFrame(survey_data)
    path = 'data/'
    make_directory_if_not_exist(path)
    check_sample_size(sheet, survey_data)
    write_new_sheet(link, survey_worksheet_name, survey_data)