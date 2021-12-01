import requests

HEADERS = {
    "Host": "passport2.chaoxing.com",
    "Origin": "https://passport2.chaoxing.com",
    "Referer": "https://passport2.chaoxing.com/login",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36, X-Requested-With: XMLHttpRequest"
}
SEARCH_URL = 'https://passport2.chaoxing.com/org/searchforms'


class SchoolInfo:
    @staticmethod
    def get_school_info(school_name: str) -> dict:
        data = {
            'allowjoin': '0',
            'filter': school_name,
            'pid': '-1'
        }
        r = requests.post(SEARCH_URL, data=data, headers=HEADERS).json()
        _school_info = r['froms'][0]
        if _school_info['name'] == school_name:
            _school_info['succeed'] = True
            return _school_info
        else:
            return {
                'succeed': False,
                'message': '请确定输入的学校名称无误！'
            }
