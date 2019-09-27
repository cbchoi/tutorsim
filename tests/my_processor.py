from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp

class Processor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 1)

        self.insert_input_port("process")
        self.insert_output_port("assess")

        self._event_recv = ""

    def process_ext_event(self, _id, _repo):
        os.chdir(_id)
        splitedItems = [x for x in _repo.split('/') if x]
        sol_dir = splitedItems[-1].split('.')[0]
        if os.path.exists(sol_dir):
            os.chdir(sol_dir)
            sp.run([ "git", "pull", _repo])
        else:
            sp.run([ "git", "clone", _repo])
        os.chdir('..')

    def ext_trans(self,port, msg):
        if port == "process":
            data = msg.retrieve()
            print(data[0])
            splitedItem = data[0].split(', ')

            if not os.path.exists(splitedItem[0]): # First Item denotes student's ID
                os.makedirs(splitedItem[0])

            self.process_ext_event(splitedItem[0], splitedItem[1])
            
            self._event_recv = data[0]
            self._cur_state = "PROCESS"

    def output(self):
        #temp = "[%f]" % (SystemSimulator().get_engine(self.engine_name).get_global_time())
        #print(temp)
        msg = SysMessage(self.get_name(), "assess")
        #print(str(datetime.datetime.now()) + " Assess Object:")
        msg.insert(self._event_recv)
        self._event_recv = ""
        return msg
        

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"