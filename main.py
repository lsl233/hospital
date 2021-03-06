import requests
import sys
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time

s = requests.session()
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 5

my_sender = '1156021653@qq.com'
my_pass = 'tsqjvexjaiejhiai'
my_user = ['1498484626@qq.com', '1156021653@qq.com']
# my_user = '1498484626@qq.com'


# send_mail 函数
def send_mail(content):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["发件人昵称", my_sender])
        msg['To'] = formataddr(["收件人昵称", 'lsl'])
        msg['Subject'] = content

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()
    except:
        ret = False
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


def fetch_data(date, update_time):
    api = 'https://wcchapp.cdwit120.com/Hospital/AjaxQueryDoctorForDept'
    r = requests.post(api, headers={
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) "
                      "Mobile/13E233 MicroMessenger/6.3.15 NetType/WIFI Language/zh_CN "
    }, data={
        'date': date, 'deptID': '044102'
    })
    bs = BeautifulSoup(r.text, "html.parser")
    html = bs.find_all(class_='doctors')
    doctor_zcr = ''
    number = ''
    for html in html:
        name = html.find(text='周从容')
        if name is not '':
            doctor_zcr = name
            number = html.find(class_='am-fl').get_text()
            break

    content = 'update time:' + update_time + '查询时间:' + date + '查询医生:' + doctor_zcr + '数量:' + number
    print(content)

    if doctor_zcr is not '' and not None:
        send_mail(content)
        sys.exit(0)
    else:
        print('周从容没有出诊')


def main():
    print('程序开始')
    while True:
        # date = (datetime.datetime.now() + datetime.timedelta(days=+7)).strftime('%Y-%m-%d %H:%M:%S')
        date = '2018-5-5'
        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            fetch_data(date, update_time)
        except IOError:
            print('error:', IOError)
            fetch_data(date, update_time)
        time.sleep(60 * 5)

main()
