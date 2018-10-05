# Disruption_Prediction_on_JTEXT
## ip数据模块（shot_ip_data）
### ip数据库（shot_data_ip.csv）
结构：一行为一炮数据，每行第一个数为炮号，后面为对应的从-0.1s到0.9s的ip值（保留到整数位）  
规模：共261行，即261炮（从1047630炮到1047903炮，有些炮号没有数据）  
### ip数据图像库（shot_ip_img）
与ip数据库对应的ip图像库，有助于增加对数据的直观理解
### ip数据读取及处理函数包（data_ip_process.py）
1.数据读取：read_ip_csv()  
2.数据简化（采样，滤波）：simplify()  
3.根据炮号寻找数据：get_shot()  
具体使用方法，请参考demo
