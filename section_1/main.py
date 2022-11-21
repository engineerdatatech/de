from preprocessor import Preprocessor
from pipeline import Pipeline
import configs
import os
from datetime import datetime
from logger import get_logger


project_dir = os.path.dirname(configs.__file__)
log_name = f"{datetime.now().strftime(configs.OUTPUT_FILENAME_FORMAT)}.log"
log_path = os.path.join(project_dir, configs.LOGS_DIR, log_name)
logger = get_logger(log_path)

preprocessor = Preprocessor(logger=logger)
preprocessor.start()
inprogress_files, inprogress_filepaths = preprocessor.get_inprogress_files_filepaths()

pipeline = Pipeline(logger=logger, inprogress_files=inprogress_filepaths)
pipeline.start()

preprocessor.move_files_to_completed(files=inprogress_files)