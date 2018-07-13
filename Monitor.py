# -*- encoding:utf-8 -*-
from hashlib import md5
import json
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host="smtp.126.com"  #设置服务器
mail_postfix="126.com"
mail_user="email@126.com"    #用户名
mail_pass="password"   #口令
receivers = ['123@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendMail(msg):
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = mail_user # 发送者
    message['To'] = ";".join(receivers) # 接收者
    message['Subject'] = Header('file monitor', 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user,  receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print str(e)
        print "发送文件失败"

def generate_file_md5value(fpath):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    m = md5()
    # 需要使用二进制格式读取文件内容
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

## 遍历保存某一路径下所有文件
def get_postfix_file_in_dir(dirname):
    file_list = []
    postfix = set(['php'])  # 设置要保存的文件格式
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                file_list.append(apath)
    return file_list

if __name__ == "__main__":
    msg = []

    fpath = "D:\\xampp\\htdocs\\"

    all_file = get_postfix_file_in_dir(fpath)
    md5_dict = {}
    for item in all_file:
        md5_dict[item] = generate_file_md5value(item)

    if sys.argv[-1] == "init":
        # 初始化MD5文件
        with open("md5_file.json", "w") as fp:
            json.dump(md5_dict, fp)
        print "md5文件生成，结果保存在"
    else:
        # 比较md5变化
        with open("md5_file.json", "r") as fp:
            md5_dict = json.load(fp)

        for item in all_file:
            if item in md5_dict:
                if md5_dict[item] != generate_file_md5value(item):
                    msg.append(item + "发生变化")
            else:
                md5_dict[item] = generate_file_md5value(item)
                msg.append(item + "新增文件")

        with open("md5_file.json", "w") as fp:
            json.dump(md5_dict, fp)

    if len(msg) == 0:
        msg.append("文件无变动")
    sendMail("<br>".join(msg))
