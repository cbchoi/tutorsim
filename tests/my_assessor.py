from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime
from pathlib import Path 

MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class Assess(object):
    def __init__(self, month, date):
        pass

class Assessor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("assess")
        self.insert_output_port("done")

        self.assessed_students = {}

    def assess_daily_commits(self, _assess):
        pass
    def process_daily_commits(self, _id, _git_id, _date, eval_dir):
        print(f"Evaluating {_id}'s commit logs")
        
        bStart = False
        stu_log = eval_dir + "/" + _id + ".log"
        with open(stu_log, "r") as f:
            for line in f:
                line = line.strip()

                if ("!!"+_git_id) in line:
                    if _id not in self.assessed_students:
                        self.assessed_students[_id] = {}

                    if _date not in self.assessed_students[_id]:
                        self.assessed_students[_id][_date] = []

                    splitedItems = line.split()
                    print(splitedItems)
                    self.assessed_students[_id][_date].append(Assess(splitedItems[2], splitedItems[3]))
                    bStart = True

                if bStart:
                    self.assess_daily_commits(self.assessed_students[_id][_date][-1])


    def ext_trans(self,port, msg):
        if port == "assess":
            data = msg.retrieve()
            print(data)
            home_dir = os.getcwd()
            eval_dir = home_dir + "/assessment/" + data[3] # date
            
            self.process_daily_commits(data[0], data[1], data[3], eval_dir)

    def output(self):
        
        return None

    def int_trans(self):
        self._cur_state = "MOVE"