#!/usr/bin/env python
# coding=utf-8
import sqlite3
import os

db_path_name = 's_file/A_system/clouddns.db'

conn = sqlite3.connect(db_path_name)
c=conn.cursor()
dns_view=c.execute('select *  from  key_table;')

os.system('mkdir -p zone_file')

DNS_VIEW = []
for i in dns_view:
    DNS_VIEW.append(i)

view_zone = {}
for i in range(len(DNS_VIEW)):
    view = DNS_VIEW[i][0]
    view_key = DNS_VIEW[i][1]
    os.system('mkdir -p zone_file/%s'%(view))  #在zone目录下创建所有的视图

    #搜索数据库中以视图名称开头的所有区文件名称
    now_tables = c.execute('Select name From sqlite_master where type = \'table\' and name like  \'%s%%%%\' ;'%(view)) 
    res = c.fetchall()
    
    #将每个视图中的区文件整理为字典
    view_zone[view.encode('utf-8')] = []
    for n in  res:
        view_zone[view].append(n[0].encode('utf-8'))
    #print view_zone[view]

    for db_zone_nmae in view_zone[view]:    #遍历每个视图下的区文件
        file_path= 'zone_file/%s/%s'%(view,db_zone_nmae + '.txt')
        suffix = view + '_'
        file_path = file_path.replace(suffix,'')
        f = open(file_path,'w')
        DNS_data = c.execute('select name,ttl,type,rdata,is_enable from \'%s\''%(db_zone_nmae)) #查询数据库中的区文件
        for dns_data in DNS_data:  #遍历每个视图下的记录
            #当区文件中存在中文时需要在进行一层判断，将其转换为utf-8的格式
            try: 
                dns_data = map(str,list(dns_data)) #将元组形式的unicode转换为列表形式的str
            except UnicodeEncodeError:
                list_dns_data = list(dns_data)
                list_dns_data[0] = list_dns_data[0].encode('utf8')
                list_dns_data[-2] = list_dns_data[-2].encode('utf8')
                
                dns_data = map(str,list_dns_data)
            if dns_data[-1] == 'no':
                print ('view:%s,zonename:%s:\ndns_record:%s '%(file_path.split('/')[1],file_path.split('/')[2],dns_data))
                continue
            else :
                del(dns_data[-1])
            print dns_data
            f.write('\t'.join(dns_data)+ '\n')
        f.close()

    
