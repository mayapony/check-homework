import time
import requests
from bs4 import BeautifulSoup
import yaml
from ChaoJiYing import Chaojiying_Client
from school_info import SchoolInfo
from utils import Utils
from headers import *
import datetime


emailApiUrl = "http://121.5.239.20:7001/mailer"
code_img_url: str = "http://passport2.chaoxing.com/num/code?"  # 后加时间戳
login_url: str = "http://passport2.chaoxing.com/unitlogin"

session = requests.session()
v = round(time.time() * 1000)

# 使用验证码
chaojiying = Chaojiying_Client("超级鹰账号", "密码", "922840")


def init_session():
    session.headers = HEADERS
    LOGIN_HEADERS["Host"] = "i.mooc.chaoxing.com"


def get_code_img():
    print("获取二维码图片...")
    session.headers = HEADERS
    try:
        code_img = session.get(code_img_url + str(v))
        fp = open("code.png", "wb")
        fp.write(code_img.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print("二维码无法下载...")


def login(uname: str, password: str, numcode: str, _school_info: dict):
    data = {
        "fid": _school_info["id"],
        "uname": uname,
        "numcode": numcode,
        "password": password,
        "refer": "http://i.mooc.chaoxing.com",
        "t": "true",
    }
    r = session.post(url=login_url, data=data)
    print(r.json())
    print("登陆成功！")


def phone_login(uname: str, password: str, _school_info: dict):
    data = {
        "fid": _school_info["id"],
        "uname": uname,
        "password": password,
        "refer": "http://i.mooc.chaoxing.com",
        "t": "true",
    }
    r = session.post("http://passport2.chaoxing.com/fanyalogin", data=data)
    print("登陆成功")


def get_class_page():
    session.headers = LOGIN_HEADERS
    home = session.get(
        f"http://i.mooc.chaoxing.com/space/index?t={v}", allow_redirects=True
    ).text
    home = BeautifulSoup(home, "html.parser")
    if home.find("a", id="icon-xfy") is not None:
        href = home.find("a", id="icon-xfy")["href"].split("'")[3]
    else:
        href = home.find("a", id="zne_kc_icon")["href"].split("'")[3]
    print(f"href: {href}")
    LOGIN_HEADERS["Host"] = "mooc2-ans.chaoxing.com"
    session.headers = LOGIN_HEADERS
    session.get(href)
    r = session.get(
        f"http://mooc2-ans.chaoxing.com/visit/courses/list?v={v}&rss=1&start=0&size=500&catalogId=0&searchname="
    )
    # print(r.text)
    return r.text


def get_course_info(_page) -> list:
    _page = BeautifulSoup(_page, "html.parser")
    _course_info_divs = _page.findAll("div", class_="course-info")
    _course_infos = []
    for course_info in _course_info_divs:
        # print(course_info)
        course_title = course_info.find("span", class_="course-name")["title"]
        course_href = course_info.find("a")["href"]
        # print(course_title, course_href)
        _course_infos.append({"title": course_title, "url": course_href})
    return _course_infos


def get_works_status(_course_infos: list, _courses: list) -> list:
    _works_status = []
    session.headers = WORK_HEADERS
    for course_info in _course_infos:
        if course_info["title"] not in _courses:
            continue
        print(f"检查{course_info['title']}中...")
        home_str = session.get(f"{course_info['url']}").text
        home = BeautifulSoup(home_str, "html.parser")
        data_url = "https://mooc1.chaoxing.com" + home.find("a", title="作业")["data"]
        work_page_str = session.get(data_url).text
        work_ul = BeautifulSoup(work_page_str, "html.parser").find(
            "ul", class_="clearfix"
        )
        works_li = work_ul.findAll("li", style="padding:30px 0")
        unfinished_works = []
        for work_li in works_li:
            work_status: list = work_li.find("strong").string.split()
            if len(work_status) > 0 and work_status[0] == "待做":
                end_time = work_li.findAll("span", class_="pt5")[1].text
                work_name = work_li.find("a", style="float: left").string.split()[0]
                print(end_time)
                unfinished_works.append({"work_name": work_name, "end_time": end_time})
        if len(unfinished_works) > 0:
            _works_status.append(
                {
                    "course_name": course_info["title"],
                    "unfinished_works": unfinished_works,
                }
            )
    return _works_status


def get_config() -> dict:
    with open("config.yaml", "r", encoding="utf-8") as config_file:
        cfg = yaml.load(config_file, Loader=yaml.SafeLoader)
        return cfg


def get_code_str():
    print("识别验证码...")
    im = open("code.png", "rb").read()
    code_str = chaojiying.PostPic(im, 4004)["pic_str"]
    return code_str


def send_email(_work_status, _reciever):
    _work_status = str(_work_status)
    r = requests.post(
        emailApiUrl,
        data={"title": "学习通作业通知", "content": _work_status, "reciever": _reciever},
    )
    print(r.json())
    # print(r.status_code)
    return r.status_code


def get_works_status_str(_work_status):
    r = ""
    for course in _work_status:
        r = r + f"<ul><strong>{course['course_name']}</strong>"
        for _index, _work in enumerate(course["unfinished_works"]):
            r += f'<li>{_work["work_name"]}，{_work["end_time"]}</li>'
        r += "</ul>"
    return r


def run():
    config = get_config()
    for index, user in enumerate(config["users"]):
        print(f"正在进行第{index + 1}个用户...")
        init_session()
        user = user["user"]
        courses = user["courses"]
        username = user["username"]
        reciever = user["email"]
        _school_info = SchoolInfo.get_school_info(user["school"])
        password = Utils.encrypt_base64(user["password"])
        courses_str = " ".join(user["courses"])
        print(f"将检查以下课程：\n{courses_str}")
        # get_code_img()
        # code = input('输入验证码：')
        # # code = get_code_str()
        # login(username, password, code, _school_info)
        phone_login(username, password, _school_info)
        page = get_class_page()
        course_infos = get_course_info(page)
        works_status = get_works_status(course_infos, courses)
        works_status_str = get_works_status_str(works_status)
        print(works_status)
        status_code = send_email(works_status_str, reciever)
        if status_code == 200:
            print("邮件发送成功！")
        print(f"第{index + 1}个用户执行完毕！")


def main_handler(event, context):
    run()


if __name__ == "__main__":
    run()
