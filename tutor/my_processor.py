from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime

from config import *
from instance.config import *

class Processor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 1)

        self.insert_input_port("process")
        self.insert_output_port("assess")

        self._event_to_send = None

    def process_student(self, _id, _home):
        print(f"Compiling {_id}'s submission")
        sp.run(["make"])

        
    def process_ext_event(self, _id, _repo):
        splitedItems = [x for x in _repo.split('/') if x]
        repo_name = splitedItems[-1].split('.')[0]
        userid = splitedItems[-2]

        home_dir = os.getcwd()
        assess_dir = home_dir + "/assessment"
        stud_dir = assess_dir + "/repository/" + _id
        solu_dir = stud_dir + '/' + repo_name
        
        if not os.path.exists(solu_dir):
            os.chdir(stud_dir)

            data = _repo.split("https://")
            new_command = "https://{0}:{1}@{2}".format(GIT_USER_ID, GIT_USER_PASSWORD, data[1])
            sp.run(["git", "clone", new_command])
            for problem in PROBLEM_LIST:
                sp.run(["cp", "-Rf", os.path.join(assess_dir, SOLUTION_DIR, '2019/midterm01/', problem), solu_dir])
            os.chdir(home_dir)

        os.chdir(solu_dir)
        self.process_student(_id, home_dir)
        os.chdir(home_dir)

        return repo_name

    def ext_trans(self,port, msg):
        if port == "process":
            data = msg.retrieve()
            splitedItem = data[0].split(',')
            
            if not os.path.exists('assessment/repository/'): # Check assessment folder
                os.makedirs('assessment/repository/')

            if not os.path.exists('assessment/repository/' + splitedItem[0]): # First Item denotes student's ID
                os.makedirs('assessment/repository/' + splitedItem[0])
            
            #print(splitedItem)
            repo_name = self.process_ext_event(splitedItem[0], splitedItem[2])
            
            self._event_to_send = [splitedItem[0], splitedItem[2], repo_name] # Send Student ID
            self._cur_state = "PROCESS" 

    def output(self):
        msg = SysMessage(self.get_name(), "assess")
        msg.extend(self._event_to_send)
        self._event_to_send = None
        return msg
        

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"