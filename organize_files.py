import glob
import os
import re
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('organize_files.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

class BaseRule:
    base_src = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def get_file_list(self):
        return glob.glob(self.base_src)

class MoveRule(BaseRule):
    base_des = ""

    def get_destination(self, file):
        return self.base_des

    def action(self, file):
        dest_folder = self.get_destination(file)
        if dest_folder:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                logger.info('created folder - {}'.format(dest_folder))
        
            dest_file = os.path.join(dest_folder, os.path.basename(file))
            if not os.path.exists(dest_file):
                os.rename(file, dest_file)
                logger.info('moved - {} to {}'.format(file, dest_file))
            else:
                logger.info('target exists - {}'.format(dest_file))

class FileTypesRule(MoveRule):
    extentions = []

    def get_file_list(self):
        files = []
        for ext in self.extentions:
            files.extend(glob.glob(self.base_src + ext))
        return files

class AnimeRule(FileTypesRule):
    extentions = ["*.mkv"]
    def get_destination(self, file):
        
        s = re.search(r"\[.*\] (.*) - (\d{2,}) ", os.path.basename(file))
        if s:
            show = s.group(1)
            return os.path.join(self.base_des, show)


rules = [
    AnimeRule(base_src="B:\\Downloads\\", base_des="B:\\Collection\\Anime"),
    FileTypesRule(base_src="B:\\Downloads\\", base_des="B:\\Downloads\\Scripts", extentions=["*.ahk", "*.py"]),
]

for rule in rules:
    for file in rule.get_file_list():
        rule.action(file)