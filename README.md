# webSiteMonitor
网站目录监控脚本 监控某一路径下文件的新增及变变动， 发现是否有webshell等文件上传

# 使用方式

1 修改发送及接收邮件地址 

2 python Monitor.py init 初始化，计算当前路径的文件MD5值保存入json文件

3 使用crontab 添加定时器，运行文件 python monitor.py
