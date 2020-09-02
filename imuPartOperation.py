#!/usr/bin/env python
# encoding: utf-8
'''
Define some common function
  
Create on 2019-05-29
@author: Hong He
@Change time: 
'''
import os
import sys
import logging
import numpy as np
import linecache


# import matplotlib.pyplot as plt


class Imu(object):
    """ the class that parse the input imu and adds noise to imu """

    def __init__(self, imu_file):
        self.file = imu_file
        self.rows = 0
        self.info = np.array(["", 0, 0])
        self.a, self.w, self.timestamp = np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0])
        self.end_info = np.array([0, 0, 0])
        self.get_data()

    def get_data(self):
        """
        Parse imu data , the third column is the timestamp, the 4-6 column is the acceleration,
        and the 7-9 column is the rotation angle. The number of rows is reduced by 1 because the
        first behavior when initializing the array is 0.
        """
        try:
            for line in linecache.getlines(self.file):
                self.info = np.vstack((self.info, line.split(",")[0:3]))
                self.timestamp = np.vstack((self.timestamp, line.split(",")[-1]))
                self.a = np.vstack((self.a, line.split(",")[3:6]))
                self.w = np.vstack((self.w, line.split(",")[6:9]))
                self.end_info = np.vstack((self.end_info, line.strip("\n").split(",")[9:12]))
            self.rows = self.a.shape[0] - 1
        except IndexError:
            logging.error("please check the input file, it has the wrong format")

    def normal(self, mean, variance):
        return np.random.normal(mean, variance, self.rows)

    def add_noise(self, bias_list, mean_list, variance_list, affect_range=None):
        """
        Add Gaussian noise to the data
        :param bias_list: The default is constant , https://confluence.ygomi.com:8443/display/RRT/Comparing+Accelerometer+Bias+of+SBG+and+SparkFun+IMUs
        :param mean_list: The mean of per column of Gaussian noise
        :param variance_list: The variance of each column of Gaussian noise
        :param affect_range: Set the range of lines to add noise , the default is all.
               For example, [0,10] means starting from line 0 to line 10 (including line 10)
               and [0,0] represents the 0th line.
        """
        # for i in range(3):
        #     if affect_range:
        #         # affect_range[0] + 1 indicates that the initialization data of the first behavior 0 is ignored.
        #         # affect_range[1] + 2 indicates that the range of action is closed
        #         self.a[1:, i] = self.a[1:, i].astype(float) + bias_list[i]
        #         self.a[affect_range[0] + 1:affect_range[1] + 2, i] = self.a[affect_range[0] + 1:affect_range[1] + 2,
        #                                                              i].astype(float) + np.random.normal(mean_list[i],
        #                                                                                                  variance_list[
        #                                                                                                      i],
        #                                                                                                  affect_range[
        #                                                                                                      1] -
        #                                                                                                  affect_range[
        #                                                                                                      0] + 1)
        #         self.w[1:, i] = self.w[1:, i].astype(float) + bias_list[i + 3]
        #         self.w[affect_range[0] + 1:affect_range[1] + 2, i] = self.w[affect_range[0] + 1:affect_range[1] + 2,
        #                                                              i].astype(float) + np.random.normal(
        #             mean_list[i + 3],
        #             variance_list[i + 3],
        #             affect_range[1] -
        #             affect_range[0] + 1)
        #     else:
        #         self.a[1:, i] = self.a[1:, i].astype(float) + bias_list[i] + np.random.normal(mean_list[i],
        #                                                                                       variance_list[i],
        #                                                                                       self.rows)
                # self.w[1:, i] = self.w[1:, i].astype(float) + bias_list[i + 3] + np.random.normal(mean_list[i + 3],
                #                                                                                   variance_list[i + 3],
                #                                                                                   self.rows)
        self.w[1:, 0]=0

    def change_timestamp(self, area, affect_range=None):
        """
        Add a random no. to the timestamp
        :param area: Range of random numbers
        :param affect_range: Consistent with the above description
        """
        if affect_range:
            self.timestamp[affect_range[0] + 1:affect_range[1] + 2] = self.timestamp[
                                                                      affect_range[0] + 1:affect_range[1] + 2].astype(
                int) + area
        else:
            self.timestamp = self.timestamp.astype(int) + area

    def save(self, tag):
        """
        Save the modified imu, the new file name will add a "noised" field
        :return:Imu data after adding noise
        """
        # object[1:,] indicates that the initialization data of the first behavior 0 is ignored.
        data = np.hstack((self.info[1:, ], self.a[1:, ], self.w[1:, ], self.end_info[1:, ], self.timestamp[1:, ]))
        new_imu = os.path.splitext(self.file)[0] + "_" + str(tag) + '.imu'
        np.savetxt(new_imu, data, delimiter=',', fmt='%s')
        # Draw(new_imu).show()
        return data


def main():
    try:
        # for item in range(20):
            # imu = Imu(sys.argv[1])
            # imu = Imu("/home/user/test_code/vtd_data/airsim/pic4_30hz.imu")
            # # imu.add_noise(bias_list=[0.02, 0.02, -0.04, 0.02, 0.02, 0.02], mean_list=[0, 0, 0, 0, 0, 0], variance_list=[0.01, 0.00005, 0.001, 0.01, 0.5, 0.01], affect_range=[1000, 2000])
            # imu.change_timestamp(area=(item + 1) * 100)
            # imu.save((item + 1) * 100)
        imu = Imu("/home/user/test_code/vtd_data/vtd_obd_xianlong/PEQI-3583/PEQI-3583.imu")
        imu.add_noise(bias_list=[0.02, 0.02, -0.04, 0.02, 0.02, 0.02], mean_list=[0, 0, 0, 0, 0, 0], variance_list=[0.01, 0.00005, 0.001, 0.01, 0.5, 0.01], affect_range=[1000, 2000])
        # imu.change_timestamp(area=-200)
        imu.save(0)

    except IndexError:
        logging.error("You should enter the imu file parameter")


if __name__ == "__main__":
    main()
