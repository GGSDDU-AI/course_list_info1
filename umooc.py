from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime
import time
import uuid
# 优慕课
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'http://opencourse.umooc.com.cn/index.do'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'class': 'open-elacourseUl'})
        for x in ul.find_all('a', attrs={"target": "_blank"}):
            course = Course_list_info()
            text = x.find('div', attrs={"class": "text"})
            course_name = text.find('h5', attrs={'class': 'name'}).string.strip()
            sandt = text.find('div', attrs={'class': 'open-contentNote'}).string
            school = sandt.split('|')[0].strip()
            teacher = sandt.split('|')[-1].strip()
            crowd = text.find('span', attrs={'class': 'accountNum'}).string
            link = 'http://opencourse.umooc.com.cn' + x.get('href')

            platform = '优慕课'

            course.url = link
            course.crowd = crowd
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.course_id = str(uuid.uuid1())
            course.save_time = datetime.now()
            course.teacher = teacher

            course_list.append(course)
            #print(course.url,course.crowd,course.course_name,course.platform,course.school,course.teacher)
        return course_list

    def fetch_all_page(self):
        courselists = []
        classes = ['理工','文学','医学','管理学','经济学','教育学','农林']
        for item in classes:
            self.driver.find_element_by_link_text(item).click()
            courselist = self.fetch_one_page()
            courselists = courselists + courselist
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