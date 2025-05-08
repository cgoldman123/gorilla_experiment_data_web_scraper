# Prolific Gorilla Data Automation

This project automates the collection, downloading, and preprocessing of participant data from Gorilla and Prolific platforms, used in longitudinal behavioral studies.

To run, use the conda environment named gorilla_env
Found in C:\Users\CGoldman\AppData\Local\anaconda3\envs\gorilla_env
Or you can separately download the packages in environment.yml

## Folder Overview

- **`gorilla_bot.py`**: Automates login and data download from the Gorilla experiment platform using Selenium.
- **`main_gorilla_bot_process.py`**: Orchestrates the full pipeline for downloading data, extracting zip files, and triggering processing scripts.
- **`unzip_and_process.py`**: Unzips downloaded Gorilla `.zip` data files, then extracts and consolidates relevant `.csv` data into an analysis-ready format.
- **`environment.yml`**: Conda environment file specifying all Python dependencies (e.g., `selenium`, `pandas`, `requests`, `trio`, etc.) for reproducibility.
- **`README.txt`**: Legacy readme containing initial documentation.

## Environment Setup

Use the provided Conda environment:

```bash
conda env create -f environment.yml
conda activate gorilla_env
