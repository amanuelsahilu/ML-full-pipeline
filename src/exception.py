import sys
from src.logger import logger

class CustomException(Exception):

    def __init__(self, error_message, error_detail):
        super().__init__(error_message)

        _, _, exc_tb = error_detail.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in {self.file_name}, line {self.line_number}: {super().__str__()}"

if __name__ =="__main__":
    try:
        result = 2/0
    except Exception as e:
        logger.info("Task started")
        raise CustomException(e,sys)

