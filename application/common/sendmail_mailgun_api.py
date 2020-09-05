# tested by gl on 8/31
import requests
def send_simple_message(sendto,subject,text):
    re = requests.post(
        "https://api.mailgun.net/v3/mg.thundervpn.com/messages",
        auth=("api", "key-191cbaa0852ce9b62f3a588118a9cd1b"),
        data={"from": "Excited User <postmaster@mg.thundervpn.com>",
              "to": [sendto],
              "subject": subject,
              "text": text})
    return re.status_code

if __name__ == '__main__':
    print(send_simple_message("guoliang@enovatemotors.com","这里是标题","<这里是正文>"))