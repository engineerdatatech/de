SRC_DIR = "new_applications"
INPROGRESS_DIR = "inprogress"
SUCCESS_DIR = "success"
FAILURE_DIR = "failure"
COMPLETED_DIR = "completed"
LOGS_DIR = "logs"
INPUT_BIRTHDAY_FORMAT = "%Y-%m-%d"

# for validation.py
LOG_FILENAME = "process_application.log"
BIRTHDAY_AS_OF_DATE = "2022-01-01"
AGE_LIMIT = 18
MOBILE_NUMBER_PATTERN = "[0-9]{8}"
EMAIL_PATTERN = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|net)"

# for pipeline.py
OUTPUT_FILENAME_FORMAT = '%Y%m%d_%H0000'

# for preprocessory.py
LAST_MODIFIED_AT_MINUTES_AGO = 0

# for transformer.py
BIRTHDAY_FORMAT = "%Y%m%d"
MEMBERSHIP_ID_BIRTHDAY_ENCODING = "utf-8"
MEMBERSHIP_ID_SHA_LENGTH = 5