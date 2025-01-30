from BotServer.MsgHandleServer.FriendMsgHandle import FriendMsgHandle
from BotServer.MsgHandleServer.RoomMsgHandle import RoomMsgHandle
from PushServer.PushMainServer import PushMainServer
from DbServer.DbInitServer import DbInitServer
import FileCache.FileCacheServer as Fcs
from FileCache.ImageCacheServer import ImageCache
from threading import Thread
from OutPut.outPut import op
from cprint import cprint
from queue import Empty
from wcferry import Wcf
import re


class MainServer:
    def __init__(self):
        self.wcf = Wcf()
        # 添加图片缓存服务
        self.wcf.image_cache = ImageCache()
        self.Dis = DbInitServer()
        # 开启全局接收
        self.wcf.enable_receiving_msg()
        self.Rmh = RoomMsgHandle(self.wcf)
        self.Fmh = FriendMsgHandle(self.wcf)
        self.Pms = PushMainServer(self.wcf)
        # 初始化服务以及配置
        Thread(target=self.initConfig, name='初始化服务以及配置').start()

    def isLogin(self, ):
        """
        判断是否登录
        :return:
        """
        ret = self.wcf.is_login()
        if ret:
            userInfo = self.wcf.get_user_info()
            # 用户信息打印
            cprint.info(f"""
            \t========== NGCBot V2.2 ==========
            \t微信名：{userInfo.get('name')}
            \t微信ID：{userInfo.get('wxid')}
            \t手机号：{userInfo.get('mobile')}
            \t========== NGCBot V2.2 ==========       
            """.replace(' ', ''))

    def processMsg(self, ):
        # 判断是否登录
        self.isLogin()
        
        # 输出所有消息类型
        msg_types = self.wcf.get_msg_types()
        op(f"[Debug] 所有消息类型: {msg_types}")
        
        while self.wcf.is_receiving_msg():
            try:
                msg = self.wcf.get_msg()
                
                # 调试输出
                op(f"""
                [Debug] 收到消息:
                - 类型: {msg.type}
                - 内容: {msg.content}
                - XML: {msg.xml}
                - 所有属性: {dir(msg)}
                """)
                
                # 原有的消息处理逻辑
                if '@chatroom' in msg.roomid:
                    Thread(target=self.Rmh.mainHandle, args=(msg,)).start()
                # 好友消息处理
                elif '@chatroom' not in msg.roomid and 'gh_' not in msg.sender:
                    Thread(target=self.Fmh.mainHandle, args=(msg,)).start()
                else:
                    pass
            except Empty:
                continue

    def initConfig(self, ):
        """
        初始化数据库 缓存文件夹 开启定时推送服务
        :return:
        """
        self.Dis.initDb()
        Fcs.initCacheFolder()
        Thread(target=self.Pms.run, name='定时推送服务').start()


if __name__ == '__main__':
    Ms = MainServer()
    Ms.processMsg()
