from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime

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

    def process_student(self, _id, _date, _home):
        print(f"Processing {_id}'s {_date} commit logs")
        sp.run([ "git", "pull"])
        result = sp.run(['git', 'log', '--pretty=format:\'\"%cn, %cd, %s\"\'',
                '--stat','--after=', "-".join([_date[0:4], _date[4:6], _date[6:]]) + " 00\:00\:00"], stdout = sp.PIPE)

        
        f = open(_home + "/assessment/" + _date + "/" + _id + ".log", "w")
        f.write(result.stdout.decode("utf-8"))
        f.close()
        os.chdir("..")

    def process_ext_event(self, _id, _repo, _date):
        #os.chdir(_id)
        splitedItems = [x for x in _repo.split('/') if x]
        
        home_dir = os.getcwd()
        stud_dir = home_dir + "/assessment/repository/" + _id
        solu_dir = stud_dir + '/' + splitedItems[-1].split('.')[0]
        
        if not os.path.exists(solu_dir):
            os.chdir(stud_dir)
            sp.run([ "git", "clone", _repo])
            os.chdir(home_dir)

        os.chdir(solu_dir)
        self.process_student(_id, _date, home_dir)
        os.chdir(home_dir)

    def ext_trans(self,port, msg):
        if port == "process":
            data = msg.retrieve()
            #print(data[0])
            splitedItem = data[0].split(', ')
            
            if not os.path.exists('assessment/repository/'): # Check assessment folder
                os.makedirs('assessment/repository/')

            if not os.path.exists('assessment/repository/' + splitedItem[0]): # First Item denotes student's ID
                os.makedirs('assessment/repository/' + splitedItem[0])
            
            check_date = datetime.datetime.now().strftime("%Y%m%d")

            if not os.path.exists('assessment/' + check_date): # Check assessment folder
                os.makedirs('assessment/'+ check_date)

            self.process_ext_event(splitedItem[0], splitedItem[1], check_date)
            
            self._event_to_send = [splitedItem[0], splitedItem[1], check_date] # Send Student ID
            self._cur_state = "PROCESS" 

    def output(self):
        #temp = "[%f]" % (SystemSimulator().get_engine(self.engine_name).get_global_time())
        #print(temp)
        msg = SysMessage(self.get_name(), "assess")
        msg.extend(self._event_to_send)
        self._event_to_send = None
        return msg
        

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"