# -*- coding: utf-8 -*-
import json, requests, time
import urllib

def upload_slack(channel, title, msg, files):
    url='https://slack.com/api/files.upload'
    token = '**************'

    textmod = {
        #'token': token,
        'channels':channel, 
        'title': title,
        'initial_comment': msg, 
        #'file': file
        #'filename': 'a.png'
        #'filetype': 'png'
    }
    #textmod = json.dumps(textmod)
    print(textmod)
    #输出内容:{"params": {"password": "zabbix", "user": "admin"}, "jsonrpc": "2.0", "method": "user.login", "auth": null, "id": 1}
    header_dict = {
        "Authorization": "Bearer {}".format(token)
    }
    res = requests.post(url=url, data=textmod, headers=header_dict, files=files)
    list_res = json.loads(res.text)
    print(list_res)
    if list_res["ok"]:
        print("send success!")
    else:
        print("send error: %s" % list_res["error"])

def send_slack(channel, msg, attachments):
    #api doc: https://api.slack.com/methods/chat.postMessage
    url='http://slack.com/api/chat.postMessage'
    token = '*******************'

    textmod = {
        'token':token, 
        'channel':channel, 
        'text': msg, 
        'attachments': attachments,
        #'link_names': 'miragelu'
    }
    params = urllib.parse.urlencode(textmod)
    res = requests.get(url = url, params = params)
    print(res.url)
    list_res = json.loads(res.text)
    print(list_res)
    if list_res["ok"]:
        print("send success!")
    else:
        print("send error: %s" % list_res["error"])

if __name__ == "__main__":
    now = time.time()
    channel = 'CAF8QRX4N' #test-api:CAF8QRX4N
    #message demo: https://api.slack.com/docs/messages/builder?msg=%7B%22attachments%22%3A%5B%7B%22fallback%22%3A%22Required%20plain-text%20summary%20of%20the%20attachment.%22%2C%22color%22%3A%22%2336a64f%22%2C%22pretext%22%3A%22Optional%20text%20that%20appears%20above%20the%20attachment%20block%22%2C%22author_name%22%3A%22Bobby%20Tables%22%2C%22author_link%22%3A%22http%3A%2F%2Fflickr.com%2Fbobby%2F%22%2C%22author_icon%22%3A%22http%3A%2F%2Fflickr.com%2Ficons%2Fbobby.jpg%22%2C%22title%22%3A%22Slack%20API%20Documentation%22%2C%22title_link%22%3A%22https%3A%2F%2Fapi.slack.com%2F%22%2C%22text%22%3A%22Optional%20text%20that%20appears%20within%20the%20attachment%22%2C%22fields%22%3A%5B%7B%22title%22%3A%22Priority%22%2C%22value%22%3A%22High%22%2C%22short%22%3Afalse%7D%5D%2C%22image_url%22%3A%22http%3A%2F%2Fmy-website.com%2Fpath%2Fto%2Fimage.jpg%22%2C%22thumb_url%22%3A%22http%3A%2F%2Fexample.com%2Fpath%2Fto%2Fthumb.png%22%2C%22footer%22%3A%22Slack%20API%22%2C%22footer_icon%22%3A%22https%3A%2F%2Fplatform.slack-edge.com%2Fimg%2Fdefault_application_icon.png%22%2C%22ts%22%3A123456789%7D%5D%7D
    attachments = [
        {
            "pretext": "--------------", 
            "author_name": "Unassigned",  
            "title": "open:0 | On Hold:0 | OverDue:0", 
            "title_link": "https://api.slack.com/",
            "text": "You are good.\nAnd i am good too :smile:.", 
            "color":"#7CD197",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": int(now)
        }
    ]
    msg = 'Hi <!here> <@miragelu>, this is ME Notification'

    send_slack(channel, msg, attachments)

    #files = {'file': open('D:\\try_do\Python\\try_do\\capture.png', 'rb')}
    #upload_slack(channel, 'title', msg, files)