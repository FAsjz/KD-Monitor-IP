import requests
import yaml


def get_token():
   cropid = 'ww5c54aa97ecd16ce0'
   corpsecret = yaml.safe_load(open(r'D:\PycharmProjects\pythonProject\Work_WX\config.yml'))['send_secret']
   url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={cropid}&corpsecret={corpsecret}'
   r = requests.get(url)
   # print(r.json())
   return r.json()['access_token']

# ACCESS_TOKEN = get_token('send_secret')
# # print(ACCESS_TOKEN)
# send_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}'
#
# back_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/recall?access_token={ACCESS_TOKEN}'

data = {
   "touser" : "20400002",
   "toparty" : "441",
   "msgtype" : "text",
   "agentid" : 1000122,
   "text" : {
       "content" : "我就试一下,请忽略。by---冀泽"
   },
   "safe":0
}

back_data = {
	"msgid": "mrVtVXE39it1tWVvd57npCiMFAX05unByDMjhWZKzx8BRefMgGQ_LjFevpJkim06XeZ2pSkIVW5RzXvvR9AtTA"
}
#
# res = requests.post(send_url,json=data)
# print(res.json())

# res = requests.post(back_url,json=back_data)
#
# print(res.json())

def work_wx_send(touser,toparty,context,url):
   data = {
      "touser": touser,
      "toparty": toparty,
      "msgtype": "text",
      "agentid": 1000122,
      "text": {
         "content": context
      },
      "safe": 0
   }
   res = requests.post(url, json=data)
   return res.json()['errmsg']


def work_wx_send_pic_msg(touser,media_id,content):
   ACCESS_TOKEN = get_token()
   send_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}'
   data = {
      "touser": touser,
      "msgtype": "mpnews",
      "agentid": 1000122,
      "mpnews": {
         "articles": [
            {
               "title": "设备断线通知，请及时处理!",
               "thumb_media_id": media_id,
               "content": content,
            }
         ]
      },
   }
   res = requests.post(send_url, json=data)
   return res.json()['errmsg']

def work_wx_upload_pic(file_path):
   ACCESS_TOKEN = get_token()
   upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={ACCESS_TOKEN}&type=image'
   files = {
      'media': (file_path, open(file_path, 'rb'), 'image/jpeg')  # 注意这里的'image/jpeg'是图片的MIME类型
   }

   # 发送POST请求
   response = requests.post(upload_url, files=files)

   # 检查响应状态码并处理响应数据
   if response.status_code == 200:
      result = response.json()
      print('图片上传成功！')
      print('Media ID:', result['media_id'])  # 上传成功后，企业微信会返回一个media_id
      return result['media_id']
   else:
      print(f'图片上传失败。状态码：{response.status_code}')
      print('错误信息：', response.text)

# work_wx_send_pic_msg(20400002)
# work_wx_upload_pic(r'C:\Users\Administrator\Desktop\照片\1.png')
# Media_ID='39F9sHL6LBRI8zQWeXIoyike77KBI71-MaoHP7nUFSvUoE1NctFruEoFRiwTjlIaHnYt0HJhrWuZFGLo5IDX5Wg'
# print(work_wx_send_pic_msg(20400002,Media_ID))
