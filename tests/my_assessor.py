from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime

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
    def process_daily_commits(self, _id, _repo, _date):
        print(f"Processing {_id}'s {_date} commit logs")
        
        result = None
        os.chdir(_id)
        splitedItems = [x for x in _repo.split('/') if x]
        sol_dir = splitedItems[-1].split('.')[0]
        if os.path.exists(sol_dir):
            os.chdir(sol_dir)
            
            os.chdir("..")
        else:
            pass

        os.chdir('..')
        print(os.getcwd())

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        print(data[0])
        
    def output(self):
        
        return None

    def int_trans(self):
        self._cur_state = "MOVE"