# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 21:07:51 2018

@author: LoveThinkhard
"""

import numpy as np
import csv
from MDSplus import connection


def readFromServer(shot_no_start=1047630, shot_no_stop=1047634, signal_name='\ip', singal_dicimals=3, time_dicimals=4):
    # 从服务器读数据
    c = connection.Connection('211.67.27.7')
    print('{} shots to read'.format(shot_no_stop-shot_no_start+1))
    signals = []
    shots = []
    time = []
    print('Start Reading signal {} ...'.format(signal_name))
    for i in range(shot_no_stop-shot_no_start+1):
        shot_no = shot_no_start + i
        print('Shot No.{}'.format(shot_no))
        try:
            c.openTree('jtext', shot=shot_no)
            singal = c.get(r'{}'.format(signal_name)).tolist()
            if i == 0 or not time:
                time = c.get(r'DIM_OF(BUILD_PATH({}))'.format(signal_name)).tolist()
                time_round = list(np.round(np.array(time), time_dicimals))
            singal_round = list(np.round(np.array(singal), singal_dicimals))
        except:
            print('ATTENTION: Shot No.{} read fail, it might don\'t exist.'.format(shot_no))
            singal_round = []
        signals.append(singal_round)
        shots.append(shot_no)
    c.closeAllTrees()
    print('Reading finished')
    return shots, signals, time_round


def read_csv(file_path='signal_x.csv'):
    # 读取csv文件
    shots = []
    ips = []
    time = []
    with open(file_path, 'r') as adi:
        reader = csv.reader(adi)
        timer = 0
        for line in reader:
            if not time:
                signal_name = line[0]
                print('Start Reading signal {} ...'.format(signal_name))
                time = [float(ip) for ip in line[1:]]
            else:
                timer += 1
                shots.append(int(line[0]))
                print('Shot No.{}'.format(int(line[0])))
                ips.append([float(ip) for ip in line[1:]])
        print('Reading Finished, {} shots totally'.format(timer))
    return shots, ips, time


def write_csv(shots, signals, time, signal_name='x', file_path='signal_x.csv'):
    # write csv
    with open(file_path, 'w', newline='') as adi:
        print('Start Writing signal {} ...'.format(signal_name))
        writer = csv.writer(adi)
        row = [signal_name]
        row.extend(time)
        writer.writerow(row)
        for i in range(len(shots)):
            row = [shots[i]]
            row.extend(signals[i])
            writer.writerow(row)
            print('Shot No.{}'.format(shots[i]))
        print('Writing Finished, {} shots totally'.format(len(shots)))
    return


def get_shot(shots, signals, shot_no):
    """ 
    find singal_index with shot_no
    Parameters
    ----------
    
    shots : a set of shots
    
    signals : a set of signals
    
    shot_no : the shot_no you want to find
    
    Return
    -------
    
    signal : the signal of the shot_no you want
    """
    return signals[shots.index(shot_no)]


def select(signal, time, start_time, stop_time,):
    # 选取时间片段
    time = np.array(time)
    zoom_part = np.where((time>=start_time)&(time<=stop_time))
    return list(np.array(signal)[zoom_part]), list(time[zoom_part])
    