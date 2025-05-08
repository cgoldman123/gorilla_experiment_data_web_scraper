from gorilla_bot import run_bot
from unzip_and_process import process_zipped_files

"""
===============================================================================
main_gorilla_bot_process.py

This is the main entry point for automating the daily download and processing 
of behavioral data from the Gorilla platform for the Theory of Mind (TOM) task.

Steps Performed:
1. Logs into Gorilla using automated Selenium script (see `gorilla_bot.py`).
2. Regenerates and downloads the most recent dataset for a specific experiment.
3. Extracts, renames, and relocates individual subject files to the proper 
   DataSink directory using session metadata and Prolific IDs (see `unzip_and_process.py`).
4. Prints confirmation upon successful completion.

To Use:
- Ensure login credentials are stored in:
    - `carter_gorilla_email.txt`
    - `carter_gorilla_password.txt`
- Ensure ChromeDriver is compatible and `chromedriver` is accessible.
- Run as a standalone script or schedule via SLURM (see `run_daily_prolific.ssub`).

===============================================================================
"""


run_bot()
process_zipped_files()
print("Job complete!!!")