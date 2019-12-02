from datetime import datetime


class Course_list_info:

    kStatusEnd = 0  # 结束
    kStatusOn = 1  # 进行中
    kStatusLaterOn = 2  # 未开始
    kStatusUnkown = 3  # 未知

    def __init__(self):
        self.id = None
        self.course_id = ''
        self.url = ''
        self.course_name = ''
        self.term = ''
        self.team = []
        self.platform = ''
        self.school = ''
        self.teacher = ''
        self.start_date = datetime(1999, 1, 1)
        self.end_date = datetime(1999, 1, 1)
        self.save_time = datetime(1999, 1, 1)
        self.crowd = '' #参与人数
        self.clicked = ''#点击量
        self.status = Course_list_info.kStatusUnkown
        self.extra = ''
