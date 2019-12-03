from course_list_info import Course_list_info
from base_fetcher import BaseFetcher
from bs4 import BeautifulSoup
from datetime import datetime
import time
import uuid
# 微知库数字校园学习平台
class IcourseFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.forum_info_list = list()
        url = 'http://wzk.36ve.com/home/index'
        self.driver.get(url)
        self.locate_page()
    def fetch_one_page(self) -> list:
        # 下面写自己的函数,爬完一页返回一次数据
        course_list = []
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        ul = soup.find('ul', attrs={'class': 'list-group'})
        for x in ul.find_all('li', attrs={"class": "col-lg-4 list-group-item"}):
            course = Course_list_info()
            course_name = x.find('a', attrs={"href": "javascript:;"}).string
            platform = '微知库数字校园学习平台'
            school = x.find('span', attrs={"class": "col-lg-7 text-left text-overflow"}).string
            teachers = x.find('span', attrs={"class": "col-lg-5 text-right text-overflow"}).string
            if x.find('span', attrs={"class": "col-lg-6 text-left"}) is not None:
                start_time = x.find('span', attrs={"class": "col-lg-6 text-left"}).string
            else:
                start_time = '1999-1-1'
            crowd = x.find('b').string
            courseID = x.find('h5', attrs={"style": "cursor:pointer"}).get('courseid')
            bcourseid = x.find('h5', attrs={"style": "cursor:pointer"}).get('bcourseid')
            link = 'http://wzk.36ve.com/index.php/CourseCenter/course/course-list-info?courseId='+courseID+'&bcourseId='+bcourseid

            course.crowd = crowd
            course.url = link
            course.course_name = course_name
            course.platform = platform
            course.school = school
            course.teacher = teachers
            course.course_id = str(uuid.uuid1())
            start_time = str(start_time)
            course.save_time = datetime.now()
            course.start_date = datetime(int(start_time.strip().split('-')[0]), int(start_time.strip().split('-')[1])
                                         , int(start_time.strip().split('-')[2]))
            course_list.append(course)
            #print(course.start_date,course.course_name,course.course_id,course.teacher,course.platform)
        return course_list

    def fetch_all_page(self):
        courselists = []
        courselist = self.fetch_one_page()
        courselists = courselists + courselist

        datapage = 1
        nextbtn = self.driver.find_elements_by_css_selector('[data-page="' + str(datapage) + '"]'' ')
        while ((len(nextbtn) != 0)):
            nextbtn[0].click()
            time.sleep(0.5)  # 适当增加
            courselist = self.fetch_one_page()
            courselists = courselists + courselist

            datapage += 1
            nextbtn = self.driver.find_elements_by_css_selector('[data-page="' + str(datapage) + '"]''')
        return courselists
    def run(self):
        return self.fetch_all_page()

    def locate_page(self):
        self.driver.find_element_by_link_text('课程中心').click()
        self.driver.maximize_window()


if __name__ == '__main__':
    a= IcourseFetcher()
    lists = a.run()
    for i in lists:
        print(i.__dict__)
    print(len(lists))