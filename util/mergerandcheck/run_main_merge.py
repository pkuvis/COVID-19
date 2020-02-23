#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import logging
import sys

WORKSPACE_PATH = '/home/ncp/webhook/'
REPOSITORY_NAME = 'COVID-19'
LOCAL_REPOSITORY_PATH = os.path.join(WORKSPACE_PATH, REPOSITORY_NAME)
CHECK_SCRIPT_PATH = os.path.join(LOCAL_REPOSITORY_PATH, 'util/mergerandcheck')
CHECK_SCRIPT_NAME = 'MergeAndCheck_Main.py'
sys.path.append(CHECK_SCRIPT_PATH)
os.chdir(CHECK_SCRIPT_PATH)
from MergeAndCheck_Main import Merge
# reload(Merge)
ANACONDA_PYTHON_PATH = '/home/ncp/anaconda3/bin/python'

if __name__ == '__main__':
    province = sys.argv[1]
    # province = 'anhui'
    file_name = sys.argv[2]
    # file_name = 'anhuiCaseStatistics_20200212.xlsx'
    try:
        check_result, log_file_name = Merge(province, file_name)
        if check_result == 'Pass':
            print('Pass')
        elif check_result is None:
            print("None")
        else:
            print('Fail')
    except Exception as e:
        logging.error(str(e))