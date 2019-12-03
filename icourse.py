from course_list_info import Course_list_info
from base_fetcher import BaseFetcher

PlatformMainpage = ''


class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.driver.get(PlatformMainpage)

    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_info_list = []
        # course_list_info = Course_list_info()
        pass

    def fetch_all_page(self):
        pass

    def run(self):
        self.fetch_all_page()
