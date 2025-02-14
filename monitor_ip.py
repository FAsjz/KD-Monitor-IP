import ping3
import smtplib
import time
import re,yaml,sys
import worktime,fp_service
from email.mime.text import MIMEText
from datetime import datetime
from prettytable import PrettyTable, prettytable
from Work_WX import message_send,make_pic
import pandas as pd



# 配置邮件发送方和接收方的信息
smtp_server = 'mail.twkd.com'  # SMTP服务器地址
smtp_port = 587  # SMTP服务器端口
smtp_user = 'kd_monitor@twkd.com'  # 你的邮箱账号
smtp_password = 'Kd62522989'  # 你的邮箱密码或授权码
recipients = ['shkdmis@twkd.com','11020798@twkd.com ','11020990@twkd.com','YujenLin@twkd.com','kdmismsg@twkd.com']  # 接收邮件的邮箱地址
#recipients = ['shkdmis@twkd.com']
rec_service = ['shkdmis@twkd.com','YujenLin@twkd.com','11021001@twkd.com']
pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b' #获取ip地址正则表达式
file_config_ip = r'D:\PycharmProjects\pythonProject\KD_Monitor_IP\config_ip.yml'
file_config_service = r'D:\PycharmProjects\pythonProject\KD_Monitor_IP\config_service.yml'
ips_process = list(yaml.safe_load(open(file_config_ip)).keys())
ips_service = list(yaml.safe_load(open(file_config_service)).keys())
# touser ='20400002|11020081'
touser ='20400002'
toparty = '441'

# 创建一个 PrettyTable 对象
table = PrettyTable()
# 设置边框样式为 DOUBLE（双边框）
table.border = True
table.hrules = prettytable.ALL  # 添加所有水平边框
table.vrules = prettytable.ALL  # 添加所有垂直边框

# 设置列对齐方式
#table.align["City"] = "l"  # 左对齐
table.align["Country"] = "c"  # 居中对齐
# 添加列名
table.field_names = ["------ip地址------", "------分公司------", "------位置------"]

# 读取IP地址列表的txt文件路径
ip_list_file = r'D:\monitor_ips\ips_to_monitor-test.txt'
ip_interval = 1800

def send_email(subject, body,rec = recipients):
    msg = MIMEText(body, 'plain')
    msg['From'] = smtp_user
    msg['To'] = ", ".join(rec)
    msg['Subject'] = subject

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, rec, msg.as_string())
    server.quit()

def check_send_email(ip,type='Process'):
    file = file_config_ip
    if type == 'Service':
        file = file_config_service
    program = yaml.safe_load(open(file))[ip]
    result = fp_service.process_or_service(ip, program,type)
    if result:
        subject = f"{program}程序中断!" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"{ip}服务器中{program}程序中断,请及时处理.error code:{result}\n1表示程序未运行\n2表示检测程序出错"
        send_email(subject, body,rec_service)

def ping_ip(ip, timeout=5, count=5):
    for _ in range(count):
        try:
            response = ping3.ping(ip, timeout)
            if response is None:
                continue  # No response received, try again
            elif response >= 0 and response is not False:
                return True  # IP is reachable
        except Exception as e:
            print(f"Warning: Exception occurred while pinging {ip}: {e}")
            continue  # Ignore this ping and try again
    return False  # IP is not reachable after multiple attempts

def monitor_ips_from_file(file_path, interval):
    while True:
        # 读取IP地址列表
        with open(file_path, 'r', encoding='utf-8') as file:
            ips_to_monitor = [line.strip() for line in file if line.strip()]
        # 获取当前时间
        now = datetime.now()
        current_time = now.time()
        current_weekday = now.weekday()  # 0 (Monday) to 6 (Sunday)

        if worktime.is_workday_and_time("00:00", "23:50", current_weekday, current_time):
            down_ips = []
            data = []
            for i in ips_to_monitor:
                #检测字符串开头是否为--
                if i.startswith("--"):
                    # 跳过这次循环
                    continue
                # print(i)
                #返回字符串引号里面的内容，并输出列表
                matches = re.findall(r"'([^']*)'", i)
                ip = matches[0]
                #print(ip)
                if not ping_ip(ip):
                    down_ips.append(i)
                    data.append(matches)
                    table.add_row(matches)
                    print(ip+' ping is not response')

                #检测所有需检测ip程序
                if ip in ips_process:
                    check_send_email(ip)

                if ip in ips_service:
                    check_send_email(ip,'Service')

            if down_ips:
                # 如果有断线的IP，发送邮件
                subject = f"监控异常警告"+now.strftime("%Y-%m-%d %H:%M:%S")
                #body = f"检测到以下监控点设备无法访问，请及时处理：\n{'\n'.join(down_ips)}"
                body = f"检测到以下监控点设备无法访问，请及时处理：\n{table}"
                # send_email(subject, body)
                print('提醒邮件已发送')
                #企业微信提醒
                # 创建DataFrame
                df = pd.DataFrame(data, columns=['IP', '地区', '设备名称'])
                # print(df)
                path = make_pic.make_pic(df)
                media_id = message_send.work_wx_upload_pic(path)
                # ACCESS_TOKEN = message_send.get_token()
                # print(ACCESS_TOKEN)
                # send_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}'
                # result = message_send.work_wx_send(touser,toparty,f"检测到线路异常请及时处理，断线IP: {', '.join(down_ips) if down_ips else '无'}",send_url)
                result = message_send.work_wx_send_pic_msg(touser,media_id, f"检测到线路异常请及时处理，断线IP: {', '.join(down_ips)}")
                print('企业微信提醒结果：',result)

            print(f"检查完成，断线IP: {', '.join(down_ips) if down_ips else '无'}",now.strftime("%Y-%m-%d %H:%M:%S"))
            print(table)
            time.sleep(interval)
            table.clear_rows()

if __name__ == "__main__":
    monitor_ips_from_file(ip_list_file, ip_interval)  # 每隔x秒检查一次
