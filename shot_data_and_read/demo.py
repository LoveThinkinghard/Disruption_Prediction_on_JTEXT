import data_ip_process as dip
import matplotlib.pyplot as plt

# 一.获得ip值
# 方法1：读取文件，得到两个数组，ips是一系列的ip值，shots则是对应的炮号
shots, ips = dip.read_ip_csv()
# 方法2：直接调用
shots = dip.shots
ips = dip.ips

# 二.使用炮号寻找数据
index = dip.get_shot(1047645)
# 通过画图显示数据
plt.plot(dip.time, ips[index])
plt.title('shot No.{}'.format(1047645))
plt.xlabel('t (s)')
plt.ylabel('ip (kA)')
plt.grid()
plt.savefig('shot ip No.{}.png'.format(1047645))
plt.show()


# 三.简化数据（取样，滤波）
ips_smp, time_smp = dip.simplify(ips)
# 画图显示简化后的数据
plt.plot(time_smp, ips_smp[dip.get_shot(1047645)])
plt.title('shot No.{}'.format(1047645))
plt.xlabel('t (s)')
plt.ylabel('ip (kA)')
plt.grid()
plt.savefig('shot ip simplified No.{}.png'.format(1047645))
plt.show()


# 四.寻找突降点，精度低（约0.01s）
# 1.指定炮号
shot_no = 1047741
# 2.找到突降点
t, ip = dip.find_the_point(ips_smp, time_smp, shot_no)
# 3.画图显示
plt.title('shot No.{}'.format(shot_no))
plt.grid()
plt.xlabel('t (s)')
plt.ylabel('ip (kA)')
plt.plot(time_smp, ips_smp[dip.get_shot(shot_no)], t, ip, 'x')
if t.size>0:
    plt.annotate('Bang! at about {:.2f}s'.format(t), xy=(t+0.05, ip))
plt.show()