import csv
from config import LOG_FILE

class Logger:
    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file

    def record_response(self, data: dict):
        """
        Append a dict of check-in fields and answers to CSV.
        """
        # TODO: open CSV and write row
        pass