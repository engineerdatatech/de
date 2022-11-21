import os
from datetime import datetime
import numpy as np
import pandas as pd
import configs
from validation import Validation
from transformer import Transformer

class Pipeline:
    def __init__(self, logger, inprogress_files):
        self.logger = logger
        self.inprogress_files = inprogress_files
        self.output_filename = f"{datetime.now().strftime(configs.OUTPUT_FILENAME_FORMAT)}.csv"
        self.project_dir = os.path.dirname(configs.__file__)
        self.success_output = os.path.join(self.project_dir, configs.SUCCESS_DIR, self.output_filename)
        self.failure_output = os.path.join(self.project_dir, configs.FAILURE_DIR, self.output_filename)
        
    def load_applications(self, f):
        try :
            applications = pd.read_json(f)
        except Exception as e:
            self.logger.error(f"Failed to read file {f}\n{e}")
        return applications
    
    def preprocess_applications(self, applications):
        applications["full_name"] = applications["full_name"].str.strip().str.lower()
        applications["mobile_number"] = applications["mobile_number"].astype(str)
        applications["birthday"] = pd.to_datetime( applications["birthday"] )
        return applications
    
    def validate_applications(self, applications):
        # return boolean mask for valid applications
        validation = Validation(logger=self.logger, applications=applications)
        is_valid_application = validation.validate_applications()
        return is_valid_application
    
    def append_to_file(self, filename, df):
        if not os.path.isfile(filename):
            df.to_csv(filename, header=True, index=False)
        else:
            df.to_csv(filename, header=False, mode='a', index=False)
            
    def save_failed_application(self, failed_application):
        # save failed_application to file
        self.append_to_file(self.failure_output, failed_application)
        
    def save_successful_application(self, successful_application):
        # transform successful_application according to required format
        transformer = Transformer(logger=self.logger, successful_application=successful_application)
        successful_application = transformer.transform()

        # save successful_application to file
        self.append_to_file(self.success_output, successful_application)
        
    def process_application(self, f):
        applications = self.load_applications(f)
        applications = self.preprocess_applications(applications)
        is_valid_application = self.validate_applications(applications)
        
        failed_application = applications[np.logical_not(is_valid_application)].copy()
        self.save_failed_application(failed_application)
        
        successful_application = applications[is_valid_application].copy()
        self.save_successful_application(successful_application)
        
    def start(self):
        for f in self.inprogress_files:
              self.process_application(f)