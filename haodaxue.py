from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime
import time
import uuid
# 好大学在线

class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'https://www.cnmooc.org/home/index.mooc'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'class': 'view-list'})
        if ul is None:
            return course_list
        for x in ul.find_all('li', attrs={"class": "view-item"}):
            course = Course_list_info()
            trem_n = x.find('span', attrs={"class": "cview-time"}).string.strip()
            course_n = x.find('a', attrs={"class": "link-default link-course-detail"}).text.strip()
            if '春' or '秋' in course_n:
                course.term = course_n
            course_name = trem_n + course_n
            id_ = x.find('a').get('courseid')
            openid = x.find('a').get('courseopenid')
            link = 'https://www.cnmooc.org/portal/course/'+ id_ +'/'+ openid+'.mooc'
            platform = '好大学在线'
            if x.find('span', attrs={"class": "start-value"}) is not None:
                start = x.find('span', attrs={"class": "start-value"}).string
                if start is not None:
                    course.start_date = datetime(int(start.strip().split('-')[0]),
                                                 int(start.strip().split('-')[1])
                                                 , int(start.strip().split('-')[2]))
            if x.find('span', attrs={"class": "end-value"}) is not None:
                end = x.find('span', attrs={"class": "end-value"}).string
                if end is not None:
                    course.start_date = datetime(int(end.strip().split('-')[0]),
                                                 int(end.strip().split('-')[1])
                                                 , int(end.strip().split('-')[2]))

            if x.find('h3', attrs={"class": "t-name substr"}) is not None:
                t = x.find('h3', attrs={"class": "t-name substr"}).string
                course.teacher=t

            if x.find('h4', attrs={"class": "t-school substr"}) is not None:
                s = x.find('h4', attrs={"class": "t-school substr"}).string
                course.school=s

            course.course_name = course_name
            course.platform = platform
            course.course_id = str(uuid.uuid1())
            course.url = link
            course.save_time = datetime.now()
            course_list.append(course)
            #print(course.start_date,course.course_name,course.course_id,course.teacher,course.platform)
        return course_list

    def fetch_all_page(self):
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist

        datapage = 1
        nextbtn = self.driver.find_elements_by_css_selector('[pagenum="' + str(datapage) + '"]'' ')
        while ((len(nextbtn) != 0)):
            nextbtn[0].click()
            time.sleep(1)  # 适当增加
            courselist = self.fetch_one_page()
            courselists = courselists + courselist

            datapage += 1
            nextbtn = self.driver.find_elements_by_css_selector('[pagenum="' + str(datapage) + '"]''')
        return courselists
    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.find_element_by_xpath('//*[@id="inner-header"]/div[1]/a[2]/span[1]').click()
        self.driver.maximize_window()


if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))