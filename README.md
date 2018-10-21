# Disruption_Prediction_on_JTEXT
## 数据处理函数包（dataprocess）
### 结构
>dataprocess(package)
>>main(module)  
>>ip(module)  

### 使用
0.把整个dataprocess文件夹放到当前程序运行的目录

1.导入

```python
import dataprocess.main as dpm
import dataprocess.ip as dpi
```

2.主要函数使用示例

* 从服务器读数据：
```python
shots, ips, time = dpm.readFromServer(1047639, 1047649, '\ip')
```
* 保存数据到csv
```python
dpm.write_csv(shots, ips, time, signal_name='ip', file_path='signal_ip.csv')
```
* 从csv文件读数据
```python
shots_t, ips_t, time_t = dpm.read_csv(file_path='signal_ip.csv')
```
* 根据炮号获取信号值
```python
ip = dpm.get_shot(shots, signals=ips, shot_no=1047642)
```
* 判断是否有并寻找破裂点，有：返回时间，无：返回False
```python
disruptime = dpi.find_the_point_2(ip, time)
```
* 画图检查判断效果
```python
dpi.check_point(ip, time, break_time=disruptime, shot_no=1047642)
```
一般情况的效果：

![画图检查的效果](https://github.com/LoveThinkinghard/Disruption_Prediction_on_JTEXT/blob/master/check_point_demo.png)

若`break_time`为`False`，则：

![画图检查的效果2](https://github.com/LoveThinkinghard/Disruption_Prediction_on_JTEXT/blob/master/check_point_demo_2.png)
