# coding=utf-8
import requests
from application.common.apig_sdk import signer

def send_simple_message(sendto,subject,text):
    sig = signer.Signer()
    sig.Key = "11ae306001f34eb78709f5c1682d5082"
    sig.Secret = "b21f418a3b3642a98a83da642957da72"
    sendfrom = "support@cloud.dearcc.net"
    body = "?emailType=0&from=support@cloud.dearcc.net&to=guoliang@enovatemotors.com&html=laskdjflk&subject=hahaha"

    # r = signer.HttpRequest("POST",
    #                        "http://mail01.apistore.huaweicloud.com/email/send"+body,
    #                        {"x-stage": "RELEASE"},
    #                        "body")
    r = signer.HttpRequest("POST",
                           "http://mail01.apistore.huaweicloud.com/email/send?emailType=0&from={}&to={}&html={}&subject={}".format(sendfrom,sendto,text,subject),
                           {},
                           "")
    sig.Sign(r)
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
    return (resp.status_code)

if __name__ == '__main__':
    import time
    print(send_simple_message("guoliang@enovatemotors.com","这里是标题","<h1>你已成功打卡</h1><p>{}</p>".format(str(int(time.time())))))