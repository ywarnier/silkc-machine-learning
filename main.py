import json
import argparse
import config.config_loading
from data import sql_reader
import pandas as pd
from data.preprocessing.text_features_extraction import extract_features_from_text
from machine_learning.clustering import training_kmeans, save_model

args = argparse.ArgumentParser()
args.add_argument('--database_configuration', '-dbc', type=str, help="The path to the configuration of the database connection", required=False)
args.add_argument('--machine_learning_configuration', '-mlc', type=str, help="The path to the configuration of the machine learning")
args.add_argument('--train', help="Activate the training for the machine learning model", required=False, action='store_true')
args.add_argument('--dataset', help="Get the dataset from file", type=str, required=False)
parsed = args.parse_args()

#%% get configuration
#db_conf = config.config_loading.get_configuration(parsed.database_configuration)

#%% First step is dedicated to obtain all the data from the database
#%% create the dictionary that push all together.

#%% Connect to the database
#db = sql_reader.connect_to_database(db_conf['db_host'], db_conf['db_user'], db_conf['db_passwd'], db_conf['db_name'], db_conf['db_port'])

#%% Opening Machine Learning configuration
with open(parsed.machine_learning_configuration, 'r') as config_file:
    ml_config = json.load(config_file)

#%% Create the base configuration
if parsed.train:
    print("Preparing the training of the model")
    if parsed.dataset is not None:
        dataframe = pd.read_csv(parsed.dataset)
    else:
        dataframe = "dataset" #TODO get data from SQL
    features = extract_features_from_text(ml_config, dataframe, ['occupation_preferred_label', 'occupation_description',
                                                              'isco_preferred_label', 'isco_group_description',
                                                              'occupation_skill_skill_type'], "english", True,
                                          "hashing")


    km = training_kmeans(ml_config, features)
    save_model(ml_config, km)