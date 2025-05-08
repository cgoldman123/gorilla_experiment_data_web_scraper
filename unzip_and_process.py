import time,os,zipfile
import pandas as pd
import math
"""
===============================================================================
unzip_and_process.py

This script performs automated unzipping and renaming of behavioral data files 
downloaded from Gorilla for the Theory of Mind (TOM) task.

Functionality:
- Scans the user's Downloads directory for the most recent Gorilla data zip file 
  that matches a specific naming pattern (e.g., "data_exp_169510").
- Unzips the file to a target directory.
- Parses the associated questionnaire file to build a mapping between private 
  participant IDs and Prolific IDs.
- Iterates through the task data files, filters and extracts data by participant, 
  and renames them using the Prolific ID, session date, and task node.
- Saves the renamed files to a standardized directory:
    L:/NPC/DataSink/StimTool_Online/WB_Theory_Of_Mind/

Assumptions:
- Data files follow Gorilla v5 naming conventions (e.g., "v5_task").
- Questionnaire file must be present in the zip and include the relevant ID mapping.
- Script should be run with all output files closed, or the write step will fail.

Notes:
- This script will need to be updated if Gorilla changes experiment version numbers 
  (e.g., v6), or if the file naming scheme changes.

Usage:
- Import and call `process_zipped_files()` in another script (e.g., main_gorilla_bot_process.py),
  or uncomment the final line to run standalone.

===============================================================================
"""

def process_zipped_files():
    current_time = time.time()
        
    # Initialize the most recent file and its modification time
    most_recent_file = None
    most_recent_time = 0
    folder_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads') + "\\"
    # Walk through the directory to get most recent zip file
    for filename in os.listdir(folder_path):
        # Check if the file ends with .zip and contains the specific string
        if filename.endswith('.zip') and "data_exp_169510" in filename:
            # Full path of the file
            file_path = os.path.join(folder_path, filename)
            
            # Get the last modified time of the file
            modification_time = os.path.getmtime(file_path)
            
            # Check if this file is the most recent
            if modification_time > most_recent_time:
                most_recent_file = filename
                most_recent_time = modification_time


    if most_recent_file is not None:
        # Get the current time in seconds since the Epoch
        #current_time = time.time()
        # convert it to tuple
        #local_time = time.localtime(current_time)
        # Format the time tuple as a string
        #formatted_time = time.strftime("%Y-%m-%d_%H_%M_%S", local_time)
        #new_dir = f"L:/rsmith/lab-members/cgoldman/Wellbeing/prolific/TOM_data/TOM_data_{formatted_time}"
        #os.mkdir(new_dir)
        unzipped_dir =  f"L:/rsmith/wellbeing/tasks/QC/getting_gorilla_data/TOM_data/TOM_data_unzipped"
        
        # Unzip the file
        with zipfile.ZipFile(os.path.join(folder_path,most_recent_file), 'r') as zip_ref:
            zip_ref.extractall(unzipped_dir)
        print(f"Successfully saved the behavioral files to {unzipped_dir}")

    # read in the file that links prolific IDs to private IDs
    file = pd.read_csv(f'{unzipped_dir}/data_exp_169510-v5_questionnaire-qoiw.csv')
    cleaned_file = file.dropna(subset=['UTC Timestamp'])
    if cleaned_file['Experiment Version'][0] == 5.0:
        # Remove rows where 'Response' column is either 'BEGIN' or 'END'
        cleaned_further_file = cleaned_file[~cleaned_file['Response'].isin(['BEGIN', 'END'])]
        id_dictionary = dict(zip(cleaned_further_file['Participant Private ID'], cleaned_further_file['Response'].astype(str)))
    elif cleaned_file['Experiment Version'][0] == 4.0:
        id_dictionary = dict(zip(cleaned_file['Participant Private ID'], cleaned_file['Prolific_ID object-3 Value'].astype(str)))


    # copy the files to a different folder with changed filenames
    for x in os.listdir(unzipped_dir):
        if x.__contains__("v5_task"):
            file = pd.read_csv(f'{unzipped_dir}/{x}')
            if 'Participant Private ID' in file.columns:
               for private_id in file['Participant Private ID'].unique():
                        if math.isnan(private_id):
                            continue
                        participants_data = file[file['Participant Private ID'] == private_id].reset_index(drop=True)
                        prolific_id = id_dictionary[private_id]
                        date = participants_data['Local Date and Time'][0]
                        date = date.replace("/", "-").replace(" ", "_").replace(":", "_")
                        if participants_data['Tree Node Key'][0] == 'task-bc6q':
                            file_type = "useless_data"
                        elif participants_data['Tree Node Key'][0] == "task-a79e":
                            file_type = "practice"
                        else:
                            file_type = participants_data['Tree Node Key'][0]
                        new_file = f"tom_{file_type}_{prolific_id}_{date}"
                        new_file_path = f"L:/NPC/DataSink/StimTool_Online/WB_Theory_Of_Mind/{new_file}.csv"
                        if not os.path.exists(new_file_path):
                            participants_data.to_csv(new_file_path, index=False)
               
                # if not math.isnan(file['Participant Private ID'][0]):
                #     for private_id in file['Participant Private ID'].unique():
                #         if math.isnan
                #     key = file['Participant Private ID'][0]
                #     prolific_id = id_dictionary[key]
                #     date = file['Local Date and Time'][1]
                #     date = date.replace("/", "-").replace(" ", "_").replace(":", "_")
                #     new_file = f"tom_task_{prolific_id}_{date}"
                #     new_file_path = f"L:/NPC/DataSink/StimTool_Online/WB_Theory_Of_Mind/{new_file}.csv"
                #     if not os.path.exists(new_file_path):
                #         file.to_csv(new_file_path, index=False)


# process_zipped_files()


            