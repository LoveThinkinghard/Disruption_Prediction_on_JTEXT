# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 21:07:51 2018

@author: LoveThinkhard
"""

import numpy as np
import scipy.signal as sgl
import matplotlib.pyplot as plt


def simplify(ip, time):
    """
    sample some point, and fliter with medfilter（取样，并使用中值滤波法滤波）
    
    Parameters
    ----------
    
    ip : a list of single ip
    
    time : a list of corresponding time
    
    Return
    -------
    
    ip_smp : simplified ip
    
    time_smp : corresponding simplified time
    """
    ip = np.array(ip)
    time = np.array(time)
    sample = np.arange(0, time.size, 10)
    time_smp = time[sample]
    ip_smp = sgl.medfilt(ip[sample], 51)
    return list(ip_smp), list(time_smp)


def find_the_point(ip, time):
    """
    find a drop point roughly

    Parameters
    ----------
    
    ip : a list of single ip
    
    time : a list of corresponding time
    
    Return
    -------
    
    drop_time : time or False
        If can't find drop point, then return False
    """
    ip_smp, time_smp = simplify(ip, time)
    ip_smp = np.array(ip_smp)
    time_smp = np.array(time_smp)
    sample = np.arange(0, time_smp.size, 5)
    ip_k = [ip_smp[sample][i+1]-ip_smp[sample][i] for i in range(len(ip_smp[sample])-1)]
    drop_point = np.where(np.array(ip_k)<-26)[0][0] if np.where(np.array(ip_k)<-26)[0].size else False
    if drop_point:
        while(ip_k[drop_point-1]<-8):
            drop_point -= 1
    return time_smp[sample][drop_point]


def find_the_point_2(ip, time):
    """
    find a drop point precisely

    Parameters
    ----------
    
    ip : a list of single ip
    
    time : a list of corresponding time
    
    Returns
    -------
    
    drop_time : time or False
        If can't find drop point, then return False
    """
    x = find_the_point(ip, time)
    time = np.array(time)
    if x.size>0:
        index_x = np.where(time==x)[0][0]
        zoom = np.hstack((np.arange(index_x-50, index_x), \
                          np.arange(index_x, index_x+70)))
        ip = np.array(ip)[zoom]
        ip_flt = sgl.medfilt(ip, kernel_size=5)
        sample = np.arange(0, zoom.size, 6)
        sample_k = np.array([ip_flt[sample][n+1]-ip_flt[sample][n] for n in range(len(sample)-1)])
        point_id = list(np.where((sample_k<=-3))[0])
        isWrong = True
        while(isWrong):
            if point_id[1]-point_id[0]<3:
                isWrong = False
            else:
                isWrong = True
                del point_id[0]
        t = time[zoom][sample[point_id[0]]]
        return t
    else:
        print('Fail to find the point, maybe it doesn\'t exist')
        return False


def check_point(ip, time, break_time=0.2723, shot_no='unknow', etd=50, pic_path=False ,picks=False):
    """
    check the point you get by zoom in

    Parameters
    ----------
    
    ip : a list of single ip
    
    time : a list of corresponding time
    
    break_time : drop time you get from you judger
        If not break_time : no zoom

    shot_no : shot no
    
    etd : decide how much you zoom in
    
    pic_path : whether to save pic
    
    picks : bool default: False
        If Ture: mark every point in the zoomed graph
    
    Returns
    -------

    None
    """
    # 传入炮号与破裂时间，画出图像，人工检查判断结果
    ip = np.array(ip)
    time = np.array(time)
    if not break_time:
        plt.title('Shot No.{}'.format(shot_no))
        plt.plot(time, ip)
        plt.annotate('No Disruption?', xy=(time.min(), ip.max()/2))
        plt.ylabel('ip (kA)')
        plt.xlabel('t (s)')
        plt.grid()
        if pic_path:
            plt.savefig(pic_path)
        plt.show()
    else:
        index_x = np.where(time==break_time)[0][0]
        zoom = np.hstack((np.arange(index_x-etd, index_x), np.arange(index_x, index_x+etd)))  # 左取50个点， 右取60个点，可调
        plt.figure(1)
        plt.subplot(211)
        plt.title('Shot No.{}'.format(shot_no))
        plt.plot(time, ip, break_time, ip[index_x], 'x')
        plt.ylabel('ip (kA)')
        plt.grid()
        plt.subplot(212)
        plt.plot(time[zoom], ip[zoom], break_time, ip[index_x], 'o')
        if picks:
            plt.plot(time[zoom], ip[zoom], 'x')
        plt.annotate('Disrupt at about {:.4f}s ?'.format(break_time), xy=(break_time+0.00001*etd, ip[index_x]))
        plt.ylabel('ip (kA)')
        plt.xlabel('t (s)')
        plt.grid()
        if pic_path:
            plt.savefig(pic_path)
        plt.show()
    return