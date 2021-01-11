#!/usr/bin/env python
# coding=utf-8
import os
import requests
import json
import base64
import time,datetime
import glob
import sys
import sqlite3
requests.packages.urllib3.disable_warnings()


class Creat:
    #creat DNS_ACL
    def creat_DNS_ACL(self, DNS_acl_name, DNS_acl_network):
        url = 'https://%s:20120/acls' % (ZDNS_CMS_ADDRESS)
        params = {'name': DNS_acl_name,
                  'networks':DNS_acl_network}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),headers=headers, auth=(CMS_ID, CMS_PASSWD), verify=False)
        return (r.status_code)
    
    #creat DNS_view
    def creat_view(self,view_name, acls):
        url = 'https://%s:20120/views' % (ZDNS_CMS_ADDRESS)
        params = {'name': view_name,
                  'owners': OWNERS,
                  'acls': [acls],
                  'black_acls': [],          #['acl_A', 'acl_B(来源访问控制黑名单，只有存在acls，黑名单才能设置)']，
                  'filter_aaaa': 'no',       #'是否过滤4a查询，取值范围(yes|no)'，
                  'filter_aaaa_ips':['any'],      #'[]表示禁止所有，['any']表示允许所有，[acl_a,acl_b(表示只过滤选择的acl)]'，
                  'recursion_enable': 'yes', #'是否开启递归查询，取值范围(yes|no)'，
                  'non_recursive_acls':[] ,   #'禁止递归查询的acl，必须是已经存在的acl，recursion_enable为yes时设置'，
                  'bind_ips': ['0.0.0.0'] ,            #['目的访问控制IP_A','目的访问控制IP_B(只能是IP，默认0.0.0.0表示不限制)']，
                  'fail_forwarder': '',        #'填写IP，表示视图查询失败后，到次地址转发查询'
                          'dns64s': [],        #['DNS64_A',' DNS64_B'…],
                  'need_tsig_key': 'no'}         #'是否开启tsig key，范围(yes|no),开启后需要传入下边tsig开头的几个参数'，

                 # 'tsig_name':  ''            #'Tsig Key的名称'，
                 # 'tsig_algorithm':         #'Tsig Key的算法，格式：算法名称$位数'，
                 # 'tsig_secret':            # '相应算法对应的密码'，
                 # ‘tsig_host’:              #‘Tsig key作用于的目的IP’

        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),headers=headers, auth=(CMS_ID, CMS_PASSWD), verify=False)
        return (r.status_code)
    
    #creat DNS_zone
    def creatMasterZone(self,view_id, name, zone_content):
        url = 'https://%s:20120/views/%s/zones' % (ZDNS_CMS_ADDRESS, view_id)
        params = {'name': name,
                  'owners': OWNERS,
                  'server_type': 'master',
                  'default_ttl': '3600',
                  'slaves': [],
                  'ad_controller': [],
                  'zone_content': zone_content}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),headers=headers, auth=(CMS_ID, CMS_PASSWD), verify=False)
        return (r.status_code)
    
    
    #creat_shared_DNS_zone
    def creat_shared_zone(self, shared_name, view_name, default_ttl):
        url = 'https://%s:20120/shared-zones' % (ZDNS_CMS_ADDRESS)
        params = {'name': shared_name,
                  'views': view_name,
                  #'create_type': 'select'
                  'default_ttl': default_ttl}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),headers=headers, auth=(CMS_ID, CMS_PASSWD), verify=False)
        return (r.status_code)

    # 日志函数
    def loger(self, content):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = now + ' ' + content
        print content
        f = file('result.log', 'a')
        f.write(content + '\n')
        f.close()
    

    def encodeZoneFile(self, path, file_name):
        f = file(path + file_name, 'r')
        content = f.read()
        f.close()
        zone_content = base64.b64encode(content)
        return zone_content

if __name__ == '__main__':
    t = Creat()
    ZDNS_CMS_ADDRESS = '127.0.0.1'
    DNS_sqlite_name = 'dns.db'
    CMS_ID = 'admin'
    CMS_PASSWD = 'admin'
    OWNERS = ['local.master']

    try:
        if str(sys.argv[1]) :
            print 'creat_icbc_date.py start running~'
    except IndexError :
        print ('Please input arguments!!!    dns_acl/dns_view/dns_zones/shared_zones  or ALL  ') 
        sys.exit()

    if str(sys.argv[1]) == 'dns_acl':
        #创建acl
        conn = sqlite3.connect(DNS_sqlite_name)
        c=conn.cursor()
        dns_acl=c.execute('select * from  acl_table')
        
        #将acl整理为列表
        DNS_ACL = []
        for i in dns_acl:
            DNS_ACL.append(i)
        conn.close()
        #循环列表，进行DNS_ACL的添加
        for i in range(len(DNS_ACL)):
            acl_name=DNS_ACL[i][0]
            acl_network=DNS_ACL[i][1]
            acl_network=acl_network.split(';')

            return_code = t.creat_DNS_ACL(acl_name, acl_network)  
            t.loger('DNS_ACL: %s return_code is %s'%(acl_name, return_code))
        t.loger('DNS_ACL: is created!')

    elif str(sys.argv[1]) == 'dns_view':
        #创建视图
        conn = sqlite3.connect(DNS_sqlite_name)
        c=conn.cursor()
        dns_view=c.execute('select * from  view')
        
        DNS_VIEW = []
        for i in dns_view:
            DNS_VIEW.append(i)
        
        for i in range(len(DNS_VIEW)):
            view = DNS_VIEW[i][1]
            view_acl = DNS_VIEW[i][8]

            return_code = t.creat_view(view,view_acl)
            t.loger('DNS_VIEW: %s return_code is %s'%(view, return_code))
        conn.close()
        t.loger('DNS_VIEW: is created!')

    elif str(sys.argv[1]) == 'dns_zones':
        #创建所有视图中的权威区
        path_view = os.listdir('zone_file')
        for w  in  range(len(path_view) ):
            VIEW_NAME = path_view[w]
            filepath = 'zone_file/%s/'%(VIEW_NAME)
            path_filename = os.listdir(filepath)

            for i  in  range(len(path_filename) ):
                suffix = path_filename[i].split('.')[-1]
                zone_name = path_filename[i].replace(suffix, '')  
                zone_name = zone_name.replace('auth_', '')  

                list_zone_name = zone_name.split('.')
                if '--' in zone_name:  #如果区文件名称有--则存在中文
                    for n in range(len(list_zone_name)-1):
                        if '--' in list_zone_name[n]:   #分割后检测每个域名段是否有中文
                            list_zone_name[n] = list_zone_name[n].replace('xn--','')
                            list_zone_name[n] = list_zone_name[n].decode('punycode').encode('utf-8')

                zone_name = '.'.join(list_zone_name)
                
                return_code = t.creatMasterZone(VIEW_NAME, zone_name ,t.encodeZoneFile(filepath, path_filename[i]))  
                t.loger('%s: DNS_ZONES:%s return_code is %s'%(VIEW_NAME,zone_name, return_code))
                time.sleep(0.4)
            t.loger('VIEW: All authority areas are created')

    elif str(sys.argv[1]) == 'shared_zones':    
        #创建共享区
        conn = sqlite3.connect(DNS_sqlite_name)
        c=conn.cursor()
        shared_zones=c.execute('select * from  sharedzone')

        DNS_SHARED_ZONES = []
        for i in shared_zones:
            DNS_SHARED_ZONES.append(i)

        t.loger('Start creating DNS SHARED ZONES')
        for i in range(len(DNS_SHARED_ZONES)):
            auth_zone = DNS_SHARED_ZONES[i][2]
            shared_zone_view = eval(DNS_SHARED_ZONES[i][3]) #将unicode转换为列表
            shared_zone_ttl = DNS_SHARED_ZONES[i][4]

            return_code = t.creat_shared_zone(auth_zone, shared_zone_view ,shared_zone_ttl)  
            t.loger('DNS_SHARED_ZONES: %s return_code is %s'%(auth_zone, return_code))
        t.loger('DNS_SHARED_ZONES: is created!')
        conn.close()

