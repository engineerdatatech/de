from datetime import datetime
import re
import configs
import numpy as np

class Validation :
    # validate whether application is successful

    def __init__(self, logger, applications):
        self.logger = logger
        self.applications = applications
        
    def is_valid_name(self, full_name):
        # check whether full_name is empty
        return full_name != ""
    
    def is_valid_birthday(self, birthday):
        # check whether age > age_limit (i.e. 18) based on birthday
        birthday_as_of_date = datetime.strptime(configs.BIRTHDAY_AS_OF_DATE, configs.INPUT_BIRTHDAY_FORMAT)
        age = ( birthday_as_of_date - birthday ) / np.timedelta64(1, 'Y')
        return age > configs.AGE_LIMIT
    
    def is_valid_mobile_number(self, mobile_number):
        # check whether mobile number is valid (8 digit number)
        pattern = re.compile(configs.MOBILE_NUMBER_PATTERN)
        # if pattern does not match, it will return None
        return (pattern.match(mobile_number) is not None) and len(mobile_number)==8
    
    def is_valid_email(self, email):
        # check whether email is valid
        pattern = re.compile(configs.EMAIL_PATTERN)
        # if pattern does not match, it will return None
        return pattern.match(email) is not None
    
    def validate_applications(self):

        try:
            self.logger.info("Validating applications : start")
            # run all validations
            self.logger.info("Validating full name")
            valid_name = self.applications["full_name"].apply(self.is_valid_name)
            self.logger.info("Validating birthday")
            valid_birthday = self.applications["birthday"].apply(self.is_valid_birthday)
            self.logger.info("Validating email")
            valid_email = self.applications["email"].apply(self.is_valid_email)
            self.logger.info("Validating mobile_number")
            valid_mobile_number = self.applications["mobile_number"].apply(self.is_valid_mobile_number)

            # consolidate successful applications
            valid_application = np.logical_and.reduce( (valid_name, valid_birthday, valid_email, valid_mobile_number) )
            self.logger.info("Validating applications : success")
            return valid_application
        except Exception as e:
            self.logger.error(f"Validating applications : fail.\n{e}")
            raise Exception(e)
        