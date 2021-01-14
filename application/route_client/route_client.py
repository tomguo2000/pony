# -*- coding: utf-8 -*-
import socket,json,os,logging,pymysql,psutil,datetime,time
import sys
VERSION = '1.1'

def initLog():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #这里设置日志的级别
    # 输出到文件
    file_handler = logging.FileHandler("pony.log", mode='a', encoding='utf-8')
    # 输出到控制台
    stream_handler = logging.StreamHandler()
    # 错误日志单独输出到一个文件
    error_handler = logging.FileHandler('error.log', mode='a', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    #注意这里，错误日志只记录ERROR级别的日志
    # 将所有的处理器加入到logger中
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    #logger.addHandler(error_handler)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    # 设置格式化
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)


def getTrojanVer():
    os.system("trojan -v 2> sss.tmp")
    with open ("sss.tmp", "r") as f:
        temp = f.readline()
        result = temp.strip()[18:]
    return result

def getCertExpDate():
    os.system('openssl s_client -connect localhost:443 < /dev/null 2> /dev/null|openssl x509 -text 2> /dev/null| grep "Not After"|sed -e "s/^ *//g"| cut -d " " -f 4,5,6,7,8 > sss.tmp')
    with open ("sss.tmp", "r") as f:
        temp = f.readline()
        result = temp.strip()
    return result

def renewCert():
    os.system("~/.acme.sh/acme.sh --renew-all > sss.tmp")
    with open ("sss.tmp","r") as f:
        temp = f.read()
        print (temp)
    return temp
def checkAll():
    checkAllData = {}
    dbConfig = {"db_server": '127.0.0.1', "db_server_port": 3306, "db_user": 'trojan', "db_password": '1234',
                "db_name": 'trojan'}
    dbSS = pymysql.connect(dbConfig['db_server'], dbConfig['db_user'], dbConfig['db_password'], dbConfig['db_name'], charset='utf8')
    cursorSS = dbSS.cursor()
    sqlSelect = "select count(*) from users where username = '' "
    try:
        cursorSS.execute(sqlSelect)
        availablePwd = cursorSS.fetchone()[0]
    except:
        logger.error('get available pwd amount from DB error')
    finally:
        dbSS.close()
    checkAllData.update({"availablePwd":availablePwd})

    os.system("netstat -anpt|grep trojan| grep ESTAB| wc -l > sss.tmp")
    with open ("sss.tmp","r") as f:
        temp = f.readline()
        onlineUserAmount = temp.strip()

    checkAllData.update({"onlineUserAmount":int(onlineUserAmount)})

    cpu = psutil.cpu_percent(interval=None)
    checkAllData.update({"cpuPercent":cpu})

    mem = psutil.virtual_memory().percent
    checkAllData.update({"memoryPercent":mem})

    networkIO = psutil.net_io_counters()
    checkAllData.update({"netBytesSent":networkIO.bytes_sent})
    checkAllData.update({"netBytesRecv":networkIO.bytes_recv})

    startTime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    checkAllData.update({"startTime":startTime})

    return str(checkAllData)


def restartTrojan():
    if os.system("systemctl restart trojan") == 0:
        return ("restart trojan success")
    else:
        return ("restart trojan failed")
def restartNginx():
    if os.system("systemctl restart nginx") == 0:
        return ("restart nginx success")
    else:
        return ("restart nginx failed")
def runSpeedTest():
    sys.exit(0)
def getTrojanLog():
    os.system("journalctl -n 30 -u trojan.service > sss.tmp")
    with open ("sss.tmp","r") as f:
        temp = f.read()
    return temp
def getNginxLog():
    os.system("journalctl -n 30 -u nginx.service > sss.tmp")
    with open ("sss.tmp","r") as f:
        temp = f.read()
    return temp
def getClientLog():
    os.system("tail -n 50 pony.log > sss.tmp")
    with open ("sss.tmp","r") as f:
        temp=f.read()
    return temp
def upgradePonyClient():
    os.system("curl -O https://obs-9bcf.obs.cn-north-1.myhuaweicloud.com:443/release/ponyclient.py")
    return "upgradePonyClient done"

def verify(data):
    try:
        aaa=json.loads(data)
        cmd = aaa['command']
        return cmd
    except:
        return False


if __name__ == "__main__":

    initLog()
    print ("Hello world!!! This is ponyclient V"+VERSION)
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = ('0.0.0.0', 8000)
    logger.info('starting up on'+str(server_address))
    #print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(3)
    while True:
        # Wait for a connection
        logger.info('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            logger.info('connection from:'+str(client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(256)
                logger.info('received:'+str(data))

                if data:
                    cmd = verify(data)
                    logger.info('doing new command:'+str(cmd))
                    if cmd == 'getTrojanVer':
                        re = getTrojanVer()
                        connection.sendall(re.encode())
                        logger.info('getTrojanVer done:'+re)
                        break
                    elif cmd == 'renewCert':
                        re = renewCert()
                        connection.sendall(re.encode())
                        logger.info('renewCert done:'+re)
                        break
                    elif cmd == 'checkAll':
                        re=checkAll()
                        connection.sendall(re.encode())
                        logger.info('checkAll done:'+re)
                        break
                    elif cmd == 'restartTrojan':
                        re = restartTrojan()
                        connection.sendall(re.encode())
                        logger.info('restartTrojan done:'+re)
                        break
                    elif cmd == 'restartClient':
                        connection.sendall("restartClient received".encode())
                        logger.info('restartClient done!')
                        connection.close()
                        time.sleep(1)
                        sys.exit(0)
                        break
                    elif cmd == 'restartNginx':
                        re = restartNginx()
                        connection.sendall(re.encode())
                        logger.info('restartNginx done:'+re)
                        break
                    elif cmd == 'getCertExpDate':
                        re = getCertExpDate()
                        connection.sendall(re.encode())
                        logger.info('getCertExpDate done:'+re)
                        break
                    elif cmd == 'runSpeedTest':
                        connection.sendall(runSpeedTest())
                        break
                    elif cmd == 'getTrojanLog':
                        re = getTrojanLog()
                        connection.sendall(re.encode())
                        logger.info('getTrojanLog done')
                        break
                    elif cmd == 'getNginxLog':
                        re = getNginxLog()
                        connection.sendall(re.encode())
                        logger.info('getNginxLog done')
                        break
                    elif cmd == 'getClientLog':
                        re = getClientLog()
                        connection.sendall(re.encode())
                        logger.info('getClientLog done')
                        break
                    elif cmd == 'upgradePonyClient':
                        re = upgradePonyClient()
                        connection.sendall(re.encode())
                        logger.info('upgradePonyClient done')
                        break
                    else:
                        logger.error('incoming data VERIFY error')
                        connection.sendall('verifyerror'.encode())
                        break
                else:
                    logger.info('no more data incoming:'+str(client_address))
                    break
        except Exception as e:
            logger.error(e)

        finally:
            # Clean up the connection
            connection.close()

