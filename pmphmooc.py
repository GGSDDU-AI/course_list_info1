from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime

import time
import uuid
# 人卫社MOOC
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'http://www.pmphmooc.com/'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'id':'mooc'})

        for x in ul.children:
            course = Course_list_info()
            link ='http://www.pmphmooc.com' +  x.find('a').get('href')
            text = x.find('div', attrs={'class': 'class-wrap-T'})
            course_name = text.find('h3').text
            if text.find('p') is not None:
                school = text.find('p').string
            else:
                school = None
            if len(text.find_all('span')) != 1:
                status = text.find_all('span')[1].string
                if status == '开课中':
                    course.status = 1
                if status == '即将开课' or status == '课程预告':
                    course.status = 2
            if len(text.find_all('span')) == 1:
                time = text.find('span').string
                course.start_date=datetime(int(time.split('-')[0]),int(time.split('-')[1]),int(time.split('-')[2]))
            text1 = x.find('div', attrs={'class': 'class-wrap-B'})
            if text1.find('li') is not None:
                crowd = text1.find('li').string
            else:
                crowd = None
            platform = '人卫社MOOC'

            course.course_id = str(uuid.uuid1())
            course.save_time = datetime.now()

            course.crowd = crowd
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.url = link

            course_list.append(course)
            #print(course.url,course.crowd,course.course_name,course.platform,course.school,course.status,course.start_date)
        return course_list

    def fetch_all_page(self):
        self.driver.find_element_by_link_text('慕课').click()
        time.sleep(1)
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist

        counter = 1
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        num = soup.find('label', attrs={'id': 'totalPage'}).string
        while (True):
            counter+=1
            self.driver.find_element_by_id('xiayiye').click()
            time.sleep(1)
            courselist = self.fetch_one_page()
            courselists = courselists + courselist
            if counter == int(num):
                break

        self.driver.find_element_by_link_text('公开课').click()
        time.sleep(2)
        courselist = self.fetch_one_page()
        courselists = courselists + courselist

        counter = 1
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        num = soup.find('label', attrs={'id': 'totalPage'}).string
        while (True):
            counter += 1
            self.driver.find_element_by_id('xiayiye').click()
            time.sleep(5)
            courselist = self.fetch_one_page()
            courselists = courselists + courselist
            if counter == int(num):
                break
        return courselists

    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.maximize_window()
        time.sleep(0.2)


if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))