#zddi_dnsdb_formatting
该工具可以将zddi中clouddns.dns数据库转换为区文件


zddi_dnsdb_formatting_v1.1.1
使用步骤：
将clouddns.db放置s_file/A_system目录中
执行 python  zddi_dnsdb_formatting.py
工具会分析clouddns.db数据库，将dns记录按照视图、写到相应的zone文件在


本工具会将数据中is_enable为no的打印出来，供使用者手动加入web界面


zddi_dnsdb_formatting_v1.1.2
增加识别数据库中的中文

