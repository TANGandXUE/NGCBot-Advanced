from BotServer.MainServer import MainServer
from cprint import cprint

Bot_Logo = """
███▄▄▄▄      ▄██████▄   ▄████████ ▀█████████▄   ▄██████▄      ███     
███▀▀▀██▄   ███    ███ ███    ███   ███    ███ ███    ███ ▀█████████▄ 
███   ███   ███    █▀  ███    █▀    ███    ███ ███    ███    ▀███▀▀██ 
███   ███  ▄███        ███         ▄███▄▄▄██▀  ███    ███     ███   ▀ 
███   ███ ▀▀███ ████▄  ███        ▀▀███▀▀▀██▄  ███    ███     ███     
███   ███   ███    ███ ███    █▄    ███    ██▄ ███    ███     ███     
███   ███   ███    ███ ███    ███   ███    ███ ███    ███     ███     
 ▀█   █▀    ████████▀  ████████▀  ▄█████████▀   ▀██████▀     ▄████▀   
     Version: V2.2 蛇年贺岁版
     Author: 久安信息有限公司旗下-NGC660安全实验室(
     eXM/云山)                                             

"""

if __name__ == '__main__':
    cprint.info(Bot_Logo.strip())
    try:
        Ms = MainServer()
        Ms.processMsg()
    except KeyboardInterrupt:
        Ms.Pms.stopPushServer()
