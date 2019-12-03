from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime
import time
import uuid
# 玩课网
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'http://www.wanke001.com/index'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('div', attrs={'class': 'container course'})
        for x in ul.find_all('div', attrs={"class": "course-item-u"}):
            course = Course_list_info()
            courseinfo = x.find('div', attrs={"class": "course-info"})
            a = courseinfo.find('a')
            link = a.get('href')
            course_name = a.get('title')
            spans = courseinfo.find_all('span')
            school = spans[0].string
            crowd = spans[1].string.split('人')[0]
            platform = '玩课网'

            course.url = link
            course.crowd = crowd
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.course_id = str(uuid.uuid1())
            course.save_time = datetime.now()
            course_list.append(course)
            #print(course.url,course.crowd,course.course_name,course.platform,course.school)
        return course_list

    def fetch_all_page(self):
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist
        return courselists
    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.find_element_by_link_text('云课堂').click()
        time.sleep(0.1)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]').click()
        self.driver.maximize_window()
        time.sleep(0.2)

if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))