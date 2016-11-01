#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess
from wxbot import WXBot

class MyWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)
        self.robot_switch = True
        self.away_status = False
        self.ai_status = False

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'机器人退下']
        away_cmd = u'afk'
        start_cmd = [u'三花聚顶', u'飞龙在天', u'反清复明']
        back_cmd = u'btk'
        ai_on_cmd = u'う'
        ai_off_cmd = u'え'
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Bot.v3] ' + u'机器人已关闭！', msg['to_user_id'])
            if msg_data == away_cmd and self.away_status == False:
                self.away_status = True
                self.send_msg_by_uid(u'[Bot.v3] ' + u' Master away from keyboard！', msg['to_user_id'])
            elif msg_data == back_cmd and self.away_status == True:
                self.away_status = False
                self.send_msg_by_uid(u'[Bot.v3] ' + u' Master! Welcome back！', msg['to_user_id'])
            elif msg_data == ai_on_cmd and self.ai_status == False:
                self.ai_status = True
                self.send_msg_by_uid(u'[Bot.v3] ' + u' AI turned on！', msg['to_user_id'])
            elif msg_data == ai_off_cmd and self.ai_status == True:
                self.ai_status = False
                self.send_msg_by_uid(u'[Bot.v3] ' + u' AI turned off！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Bot.v3] ' + u'机器人已开启！', msg['to_user_id'])

    def tell_fortune():
        reply = '[Bot.v3] '
        response = subprocess.Popen(['fortune', '-a'], stdout=subprocess.PIPE).communicate()[0]
        reply += response
        return reply
    def tell_poem():
        reply = '[Bot.v3] '
        response = subprocess.Popen(['fortune', '-e', 'tang300', 'song100'], stdout=subprocess.PIPE).communicate()[0]
        reply += response
        return reply
    def tell_dirty():
        reply = '[Bot.v3] '
        response = subprocess.Popen(['fortune', '-e', 'aj'], stdout=subprocess.PIPE).communicate()[0]
        reply += response
        return reply

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            self.send_msg_by_uid(u'[Bot.v3] ' + u'机器人已关闭... 請稍後再聯系！', msg['to_user_id'])
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            # print(msg["content"]["data"])
            master_input = msg["content"]["data"]
            if u'好无聊' in master_input:
                self.send_msg_by_uid(tell_fortune(), msg['to_user_id'])
            elif u'来首诗歌' in master_input:
                self.send_msg_by_uid(tell_poem(), msg['to_user_id'])
            else:
                self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            if self.away_status == True:
                self.send_msg_by_uid(u'[Bot.v3] ' + u' 主人不在, 请稍后联系! ', msg['user']['id'])
                # TODO Add some functions!
                return
            if msg['user']['name'] == u'明明':
                master_input = msg["content"]["data"]
                if u'污一个' in master_input:
                    self.send_msg_by_uid(self.tell_dirty(), msg['user']['id'])
                elif u'来首诗歌' in master_input:
                    self.send_msg_by_uid(self.tell_poem(), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break

                if is_at_me:
                    # print(msg)
                    if self.away_status == True:
                        self.send_msg_by_uid(u'[Bot.v3] ' + u' 主人不在, 请稍后联系! ', msg['user']['id'])
                        return
                    src_name = msg['content']['user']['name']
                    reply = '[Bot.v3] @' + src_name + ' : '
                    if msg['content']['type'] == 0:  # text message
                        if self.ai_status == True:
                            # TODO Add some functions!
                        else:
                            response2 = u'(你好, 我是第3代机器人.  请直接输入 "好无聊" 或 "来首诗歌"!) '
                            reply += response2
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])
                else:
                    if msg['content']['type'] == 0:  # text message
                        user_input = msg["content"]["desc"]
                        src_name = msg['content']['user']['name']
                        # reply = '[Bot.v3] @' + src_name + ' : '
                        if u'好无聊' in user_input:
                            self.send_msg_by_uid(self.tell_fortune(), msg['user']['id'])
                        elif u'来首诗歌' in user_input:
                            self.send_msg_by_uid(self.tell_poem(), msg['user']['id'])
                        elif u'讲个污笑话' in user_input or u'乐一个' in user_input:
                            self.send_msg_by_uid(self.tell_dirty(), msg['user']['id'])

        elif msg['msg_type_id'] == 5 and msg['content']['type'] == 0:
            # if msg['user']['name'] == u'小冰':
                # user_input = msg["content"]["data"]
                # response = 'WTF!'
                # self.send_msg_by_uid(response, msg['user']['id'])

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()

if __name__ == '__main__':
    main()
