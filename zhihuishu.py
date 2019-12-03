from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime
import time
import uuid
# 智慧树网
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'https://www.zhihuishu.com/'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'class': 'clearfix verticalTop'})
        counter = 1
        for x in ul.find_all('li', attrs={"class": "verticalItem"}):
            js = "var q=document.documentElement.scrollTop=0"
            self.driver.execute_script(js)
            course = Course_list_info()
            course_name = x.find('p', attrs={'class': 'courseName'}).string
            school = x.find('span', attrs={'class': 'schoolName'}).string
            teacher = x.find('span', attrs={'class': 'teacherName'}).string
            crowd = x.find('span', attrs={'class': 'countNum'}).string.split('人')[0]
            platform = '智慧树'

            course.course_id = str(uuid.uuid1())
            course.save_time = datetime.now()

            course.crowd = crowd
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.teacher = teacher

            xpath = '//*[@id="app"]/div/div[1]/div[1]/div[2]/ul/li[' + str(counter) + ']/div/div[2]/p[1]'
            self.driver.find_element_by_xpath(xpath).click()
            time.sleep(1)
            link = self.driver.current_url
            course.url = link
            self.driver.back()
            time.sleep(1)
            counter += 1

            course_list.append(course)
            #print(course.url,course.crowd,course.course_name,course.platform,course.school,course.teacher)
        return course_list

    def fetch_all_page(self):
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist
        counter = 1
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        num = soup.find_all('li', attrs={'class': 'number'})[-1].string
        while (True):
            counter += 1
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div[2]/div/div/button[2]/span').click()
            time.sleep(1)
            courselist = self.fetch_one_page()
            courselists = courselists + courselist
            if counter == int(num):
                break
        return courselists
    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.maximize_window()
        self.driver.find_element_by_link_text('课程').click()
        self.driver.find_element_by_css_selector('i[class="el-dialog__close el-icon el-icon-close"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[4]/div/div[2]/div/div[1]/div/div[1]/div[2]').click()
        time.sleep(0.2)
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[-1])


if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))