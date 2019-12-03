from course_list_info import Course_list_info
import abc

from selenium import webdriver


class BaseFetcher:
    kWaitSecond = 5

    def __init__(self):
        self.driver = webdriver.Chrome()

    @abc.abstractmethod
    def fetch_one_page(self) -> list:
        pass

    @abc.abstractmethod
    def fetch_all_page(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass