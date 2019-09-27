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


    def process_daily_commits(self, _id, _repo, _date):
        print(_id)
        print(_repo)
        print(_date)
        
        os.chdir(_id)
        splitedItems = [x for x in _repo.split('/') if x]
        sol_dir = splitedItems[-1].split('.')[0]
        if os.path.exists(sol_dir):
            os.chdir(sol_dir)
            result = sp.run(['git', 'log', '--pretty=format:\'\"%cn, %cd, %s\"\'',
                    '--stat','--after=', "-".join([_date[0:4], _date[4:6], _date[6:]]) + " 00\:00\:00"], stdout = sp.PIPE)
            
    #mv ./*.log "../assessment/"
            print("-".join([_date[0:4], _date[4:6], _date[6:]]))
            #sp.run([ "git", "pull", _repo])
            os.chdir("..")
        else:
            #sp.run([ "git", "clone", _repo])
            # TODO: Exception Handling
            pass

        os.chdir('..')
        print(os.getcwd())
        f = open("/".join([".", "assessment",_date, _id + ".log"]), "w")
        #f.write(result.stdout)
        print(result.stdout.decode("utf-8") )
        f.close()

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        if not os.path.exists('assessment'): # Check assessment folder
           os.makedirs('assessment')

        splitedItem = data[0].split(', ')
        check_date = datetime.datetime.now().strftime("%Y%m%d")

        if not os.path.exists('assessment/' + check_date): # Check assessment folder
            os.makedirs('assessment/'+ check_date)

        self.process_daily_commits(splitedItem[0], splitedItem[1], check_date)

    def output(self):
        
        return None

    def int_trans(self):
        self._cur_state = "MOVE"