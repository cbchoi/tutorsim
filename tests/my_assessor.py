from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime
from pathlib import Path 

class Assessor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("assess")
        self.insert_output_port("done")

    def assess_daily_commits(self):
        pass
    def process_daily_commits(self, _id, eval_dir):
        print(f"Evaluating {_id}'s commit logs")
        
        stu_log = eval_dir + "/" + _id + ".log"
        with open(stu_log, "r") as f:
            for line in f:
                print(line)

    def ext_trans(self,port, msg):
        if port == "assess":
            data = msg.retrieve()
            #print(data)
            home_dir = os.getcwd()
            eval_dir = home_dir + "/assessment/" + data[2] # date
            
            self.process_daily_commits(data[0], eval_dir)

    def output(self):
        
        return None

    def int_trans(self):
        self._cur_state = "MOVE"