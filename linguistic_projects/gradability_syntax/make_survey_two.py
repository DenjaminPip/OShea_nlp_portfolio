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
import random
from make_survey_one import write_new_sheet, open_sheet, new_data

def write_new_prompt(noun: str, adjective_1: str, adjective_2: str) -> tuple:
    """
    Simple function to write out the two word orders that users can rate.

    :param noun: str
        The noun
    :param adjective_1: str
        The first adjective
    :param adjective_2: str
        The second adjective
    :return: tuple
        The two strings with the adjectives in their respective orders
    """
    return f"the {adjective_1} {adjective_2} {noun}", f"the {adjective_2} {adjective_1} {noun}"

def get_survey_data(nouns: list, age_adjectives: list, physical_adjectives: list, n: int = 10, random_seed:int = None) -> dict:
    """
    Function that creates the survey stimuli by randomly selecting items from three lists of stimuli. Items saved to a
    dictionary, for later processing.

    :param nouns:
        The list of nouns
    :param age_adjectives:
        The list of adjectives in the semantic class 'age'
    :param physical_adjectives:
        The list of adjectives in the semantic class 'physical'
    :param n:
        The number of stimuli to produce for this task
    :param random_seed:
        The random seed for reproducibility.
    :return: dict
        The dictionary object with all the stimuli organized for this task
    """
    random.seed(random_seed)
    df = {}
    for i in range(n):
        noun = random.choice(nouns)
        age = random.choice(age_adjectives)
        physical = random.choice(physical_adjectives)
        scontras, alt = write_new_prompt(noun, age, physical)
        new_data(df,
                 question="Please select on the scale which word order you prefer.",
                 type="scale",
                 required=True,
                 start=f"1,5,{alt},{scontras}",
                 end="")
    return df

if __name__ == '__main__':
    # Prepare the DataFrame of stimuli
    link = "https://docs.google.com/spreadsheets/d/1jxXRnLCp8mHE2MvJ5C8CwXuzFEj36_2tT0MFAaCtBp4/edit#gid=2106397498"
    stimuli_worksheet_name = "word_order_adjectives"
    sheet = open_sheet(link, stimuli_worksheet_name)

    # The name of the new worksheet that will be used to create the survey
    survey_worksheet_name = "Word Order Preference"

    # The lists of stimuli
    nouns = sheet.loc[sheet['class'] == 'noun']['word'].tolist()
    age_adjectives = sheet.loc[sheet['category'] == 'age']['word'].tolist()
    physical_adjectives = sheet.loc[sheet['category'] == 'physical']['word'].tolist()

    # Run the program and write to new Google Sheet
    survey_data = get_survey_data(nouns, age_adjectives, physical_adjectives, n=10, random_seed=58)
    survey_data = pd.DataFrame(survey_data).drop_duplicates(subset=['start'])
    write_new_sheet(link, survey_worksheet_name, survey_data)