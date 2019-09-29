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
    def __init__(self, month, day):
        self._month = month
        self._day = day
        self.insertion_cnts = 0
        self.deletion_cnts = 0
        self.logs = ""
        pass

    def check(self, line):
        self.logs += line + '\n'

        done_flag = False
        if 'files changed' in line:
            done_flag = True

        if 'insertions' in line:
            self.insertion_cnts += 1
            done_flag = True

        if 'deletions' in line:
            self.deletion_cnts += 1
            done_flag = True

        return done_flag

    def __str__(self):
        return f'{self._month}-{self._day} I:{self.insertion_cnts} D:{self.deletion_cnts}'


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
        self.current_student = None

    def assess_daily_commits(self, _assess, line):

        pass

    def process_daily_commits(self, _id, _git_id, _date, eval_dir):
        print(f"Evaluating {_id}'s commit logs")
        
        bProcess = False
        stu_log = eval_dir + "/" + _id + ".log"
        with open(stu_log, "rb") as f:
            for line in f:
                line = line.decode().strip()

                if line and ("!!"+_git_id) in line:
                    splitedItems = line.split()
                    date = splitedItems[2] + splitedItems[3]

                    if _id not in self.assessed_students:
                        self.assessed_students[_id] = {}

                    if date not in self.assessed_students[_id]:
                        self.assessed_students[_id][date] = Assess(splitedItems[2], splitedItems[3])
                        self.current_student = self.assessed_students[_id][date]
                    bProcess = True

                if bProcess:
                    bProcess = not self.current_student.check(line)
                    

        for key, value in self.assessed_students.items():
            for k, v in value.items():
                print(v)

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