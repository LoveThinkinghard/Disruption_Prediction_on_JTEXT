import csv
import numpy as np
import scipy.signal as sgl

# shot_data_ip.csv里的数据结构：一行为一炮数据，每行第一个数为炮号，后面就是-0.1s到0.9s的ip值（精度为小数点后3位）

# ip序列对应的时间，时间间隔为0.0001
time = np.linspace(-0.1, 0.9, 10001)


def read_ip_csv(file_path='shot_data_ip.csv'):
    # 读取shot_data_ip.csv文件，得到两个数组，ips是一系列的ip值，shots则是对应的炮号
    shots = []
    ips = []
    with open(file_path, 'r') as adi:
        reader = csv.reader(adi)
        for line in reader:
            shots.append(int(line[0]))
            ips.append([float(ip) for ip in line[1:]])
    return shots, ips

shots, ips = read_ip_csv()


def simplify(ips, time=time):
    # sample some point, and fliter with medfilter（取样，并使用中值滤波法滤波）
    sample = np.arange(0, 10000, 10)
    time_smp = time[sample]
    ips_smp = [sgl.medfilt(np.array(ips[i])[sample], 51) for i in range(len(ips))]
    return ips_smp, time_smp


def get_shot(shot_no, shots_t=shots):
    # find ip with shot_no（使用炮号找到对应的ip值，返回引索值）
    return shots.index(shot_no)


def find_the_point(ips_smp, time_smp, shot_no=1047741):
    # 如果有大突降，则返回这个点，否则返回空数组，注意shot_no需要是一个能在数据库中找到的炮号
    index = get_shot(shot_no)
    sample = np.arange(0, 1000, 20)
    ip_k = [ips_smp[index][sample][i+1]-ips_smp[index][sample][i] for i in range(len(ips_smp[index][sample])-1)]
    drop_point = np.where(np.array(ip_k)<-40)[0][0] if np.where(np.array(ip_k)<-40)[0].size else False
    if drop_point:
        while(ip_k[drop_point-1]<-2):
            drop_point -= 1
    return time_smp[sample][drop_point], ips_smp[index][sample][drop_point]
