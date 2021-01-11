# creat_icbc_data,
1、该工具通过将zdns的zone文件下面拷贝所有的视图、区文件，实现的权威区批量创建
2、通过分析dns.db实现创建acl/view/shard_zone/DNS_zone

 creat_icbc_data_v1.1.1
#将/usr/local/zddi/dns/zone文件夹下的所有文件放至 ‘zone_file’ 目录中，并删除所有的jnl文件
#将/usr/local/zddi/dns.db 数据库与脚本放在同一目录下。
#编辑在creat_icbc_date.py 文件，指定用户名，密码以及节点名称。
#zddi-master后台使用以下命令将区文件批量创建至zddi
PYTHONPATH=./lib/site-packages  python   creat_icbc_date.py  <aguments>


#创建权威区
PYTHONPATH=./lib/site-packages  python   creat_icbc_date.py  'dns_zones'



#creat_icbc_data_v1.1.2
增加中文区的创建 #需要通过zddi_dnsdb_formatting工具转化的数据



