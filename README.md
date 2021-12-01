# 使用流程🎉

## 一、确保装有 python

使用 `python --version` 命令检查，出现 python + 版本号即可

```shell
python --version
# Python 3.7.4
```



如果没有需要配置 `python` 环境

## 二、项目环境

### 1. 项目克隆

在指定目录（比如桌面）执行以下命令

`git clone https://gitee.com/mayapony/check-homework`

![](https://gitee.com/mayapony/pic-dog/raw/master/imgs/20211201204545.png)

我这里是克隆在了桌面

### 2. 安装依赖

![](https://gitee.com/mayapony/pic-dog/raw/master/imgs/20211201205603.png)

`cd ./check-homework` 进入目录，`pip install -r ./requirements.txt` 安装所需依赖。

### 3. 修改配置文件

- 可添加多个用户
- `school` 为学校全称
- `username` 为手机号 **（推荐）**，使用学号需修改`main.py`，使用`get_code_str()`函数获取验证码后使用`login()`函数登录，使用手机号则不需要修改代码
- `password `为登录密码，与username对应。
- `email` 你的邮件地址，查询结果会通过发送邮件的方式通知
- `courses` 需要查询的课程的全称

下面为样例文件：

```yaml
users:
  - user:
      school: '安徽师范大学'
      username: '180xxxxxxxx' # 手机号
      password: 'xxxxxx'
      email: 'xxxxxxxx@qq.com' # 邮箱地址
      courses:
        - "计算机网络"
        - "计算机网络实验"
        - "人机界面设计"
        - "大学美育"
        - "《数据库原理实验》"
        - "《数据库原理》"
        - "软件工程实验"
        - "软件工程"
```

增加多个用户只需要添加一个 `user` 配置项即可。如下所示：

```yaml
users:
  - user:
      school: '安徽师范大学1'
      username: '180xxxxxxxx' # 手机号
      password: 'xxxxxx'
      email: 'xxxxxxxx@qq.com' # 邮箱地址
      courses:
        - "计算机网络"
  - user:
      school: '安徽师范大学2'
      username: '180xxxxxxxx' # 手机号
      password: 'xxxxxx'
      email: 'xxxxxxxx@qq.com' # 邮箱地址
      courses:
        - "计算机网络"
```

## 三、运行

在项目根目录执行 `python main.py` 即可

结果：

![](https://gitee.com/mayapony/pic-dog/raw/master/imgs/20211201210643.png)

邮件内容：

![](https://gitee.com/mayapony/pic-dog/raw/master/imgs/20211201210755.png)