from scrapy import signals
from scrapy.http import HtmlResponse
from szlc.settings import USER_AGENT_LIST
import requests
import base64
import random


# 随机UA
class RandomUserAgent(object):

    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua


# 随机IP
class RandomProxy(object):

    def __init__(self):
        self.ip_list = self.get_ip_list()

    def get_ip_list(self):
        '''
        ip 池接口
        :return:
        '''
        url = 'http://api.wandoudl.com/api/ip?app_key=fffbcf689ef5ecafaf6607f713f70ed9&pack=216497&num=20&xy=2&type=2&lb=\r\n&mr=1&'
        resp = requests.get(url)
        resp_dict = resp.json()
        ip_dict_list = resp_dict.get("data")
        list_ip = []
        if ip_dict_list != None:
            for ip_dict in ip_dict_list:
                ip_port = '{ip}:{port}'.format(ip=ip_dict.get('ip'), port=str(ip_dict.get('port')))
                list_ip.append(ip_port)
        return list_ip

    def process_request(self, request, spider):
        proxy = random.choice(self.ip_list)
        request.headers['Proxy-Authorization'] = 'Basic %s' % (self.base_code('15616122577@163.com', 'Zhang0612'))
        request.meta['proxy'] = proxy

    def base_code(self, username, password):
        str = '%s:%s' % (username, password)
        encodestr = base64.b64encode(str.encode('utf-8'))
        return '%s' % encodestr.decode()

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        # 在库中删除无效ip
        del_ip = request.meta.get('proxy')[2:]
        print(f'ip失效{del_ip}')
        self.ip_list.remove(del_ip)

        # 返回request，重新发送请求
        return request

