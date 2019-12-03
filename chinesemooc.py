from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime

import time
import uuid
# 华文慕课
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'http://www.chinesemooc.org/'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'id': 'course-list'})

        for x in ul.find_all('li', attrs={'class': 'course-item'}):
            course = Course_list_info()
            link ='http://www.chinesemooc.org' +  x.find('a').get('href')
            course_name = x.find('a', attrs={'class': 'course-name'}).string
            text = x.find('div', attrs={'class': 'course-author'}).string
            #print(text)
            school = text.split('  ')[0]
            teacher = text.split('  ')[1]
            crowd = x.find('div', attrs={'class': 'course-fans'}).string
            platform = '华文慕课'

            course.course_id = str(uuid.uuid1())
            course.save_time = datetime.now()

            course.crowd = crowd
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.url = link
            course.teacher = teacher

            course_list.append(course)
            #print(course.url,course.crowd,course.course_name,course.platform,course.school,course.teacher,course.start_date)
        return course_list

    def fetch_all_page(self):
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist

        return courselists

    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.maximize_window()
        self.driver.find_element_by_link_text('课程').click()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'id': 'course-list'})
        length = len(ul.find_all('li', attrs={'class': 'course-item'}))
        self.driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'id': 'course-list'})
        newlength = len(ul.find_all('li', attrs={'class': 'course-item'}))

        while (newlength != length):
            self.driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
            time.sleep(2)
            length = newlength
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            ul = soup.find('ul', attrs={'id': 'course-list'})
            newlength = len(ul.find_all('li', attrs={'class': 'course-item'}))
        time.sleep(0.5)



if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))