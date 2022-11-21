import os
import configs
from datetime import datetime, timedelta

class Preprocessor:
    def __init__(self, logger):
        self.logger = logger
        self.project_dir = os.path.dirname(configs.__file__)
        self.src_dir = os.path.join(self.project_dir, configs.SRC_DIR)
        self.inprogress_dir = os.path.join(self.project_dir, configs.INPROGRESS_DIR)
        self.completed_dir = os.path.join(self.project_dir, configs.COMPLETED_DIR)
    
    def is_file(self, filedir, filename):
        # check whether filedir/filename is a file
        filepath = os.path.join(filedir, filename)
        return os.path.isfile(filepath)
    
    def is_mtime_less_than_filter_mtime(self, filedir, filename, filter_mtime):
        # check whether file's mtime is less than required m_time
        filepath = os.path.join(filedir, filename)
        mtime = os.path.getmtime(filepath)
        mtime = datetime.fromtimestamp(mtime)
        return mtime < filter_mtime
    
    def move_files_to_inprogress(self, files):
        # move files from new_applications to inprogress folder
        self.inprogress_files, self.inprogress_filepaths = files, []
        for f in files:
            src_filepath = os.path.join(self.src_dir, f)
            dest_filepath = os.path.join(self.inprogress_dir, f)
            os.rename(src_filepath, dest_filepath)
            self.inprogress_filepaths.append(dest_filepath)
        
    def get_qualified_files(self):
        # get qualified files where m_time < required m_time
        qualified_files = list( filter(lambda f : self.is_file(self.src_dir, f), os.listdir( self.src_dir )) )
        filter_mtime = datetime.now() - timedelta(minutes=configs.LAST_MODIFIED_AT_MINUTES_AGO)
        qualified_files = list( filter(
                                lambda f : self.is_mtime_less_than_filter_mtime(self.src_dir, f, filter_mtime),
                                qualified_files
        ) )
        return qualified_files

    def move_files_to_completed(self, files):
        # move files from inprogress folder to completed
        for f in files:
            src_filepath = os.path.join(self.inprogress_dir, f)
            dest_filepath = os.path.join(self.completed_dir, f)
            os.rename(src_filepath, dest_filepath)
        
    def start(self):
        self.qualified_files = self.get_qualified_files()
        self.logger.info(f"Qualified files = {self.qualified_files}")
        self.move_files_to_inprogress(self.qualified_files)
        self.logger.info(f"Files in inprogress folder = {self.inprogress_filepaths}")
    
    def get_inprogress_files_filepaths(self):
        return self.inprogress_files, self.inprogress_filepaths