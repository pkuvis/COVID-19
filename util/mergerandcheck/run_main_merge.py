#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
from MergeAndCheck_Main import Merge

WORKSPACE_PATH = '/home/ncp/webhook/'
REPOSITORY_NAME = 'COVID-19'
LOCAL_REPOSITORY_PATH = os.path.join(WORKSPACE_PATH, REPOSITORY_NAME)
CHECK_SCRIPT_PATH = os.path.join(LOCAL_REPOSITORY_PATH, 'util/mergerandcheck')
os.chdir(CHECK_SCRIPT_PATH)

if __name__ == '__main__':
    province = sys.argv[1]
    file_name = sys.argv[2]
    try:
        check_result, log_file_name = Merge(province, file_name)
        print("%s|log_path:%s" % (check_result, log_file_name))
    except Exception as e:
        print("Faile|%s" % str(e))