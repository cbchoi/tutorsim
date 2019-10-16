from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime
from pathlib import Path 
from subprocess import STDOUT, check_output, TimeoutExpired

import pandas as pd
import numpy as np

MONTH = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

from config import *
from instance.config import *
import pygsheets

class Assess(object):
    def __init__(self, _id, problem_list):
        self._id = _id
        self.assessments = {}
        for problem in problem_list:
            self.assessments[problem] = ""

    def get_id(self):
        return self._id

    def get_assessments(self):
        return self.assessments

    def assess(self, problem):
        if os.path.isfile('pass.assess'):
            with open('pass.assess', 'rb') as f:
                self.assessments[problem] = f.read().decode('utf8')
        elif os.path.isfile('wrong.assess'):
            with open('wrong.assess', 'rb') as f:
                self.assessments[problem] = f.read().decode('utf8')
        elif os.path.isfile('c_error.assess'):
            with open('c_error.assess', 'rb') as f:
                self.assessments[problem] = f.read().decode('utf8')
        elif os.path.isfile('t_exipred.assess'):
            with open('t_exipred.assess', 'rb') as f:
                self.assessments[problem] = f.read().decode('utf8')
        else:
            self.assessments[problem] = "unknown"


class Assessor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 1)

        self.insert_input_port("assess")
        self.insert_input_port("report")
        self.insert_output_port("done")

        self.assessed_students = {}
        self.current_student = None
        self.asessment_file_path = ""

    def process_examination(self, _id, eval_dir):
        print(f"Assessing {_id}'s answers")
        
        self.assessed_students[_id] = Assess(_id, PROBLEM_LIST)

        for problem in PROBLEM_LIST:
            problem_path = os.path.join(eval_dir, problem)
            os.chdir(problem_path)
            cmd = ['python3', "grade_criteria.py"]
            sp.run(cmd)

            self.assessed_students[_id].assess(problem)
            os.chdir(eval_dir)


    def ext_trans(self,port, msg):
        if port == "assess":
            data = msg.retrieve()
            #print(data)
            home_dir = os.getcwd()
            eval_dir = os.path.join(home_dir, "assessment","repository", data[0], data[2]) # date
            self.process_examination(data[0], eval_dir)
            os.chdir(home_dir)

        if port == "report":
            data = msg.retrieve()
            self.asessment_file_path = data[0]
            self._cur_state = "PROCESS"
            

    def output(self):
        df = pd.DataFrame('', index=[], columns=[])
        for key, value in self.assessed_students.items():
            for k, v in value.get_assessments().items():
                df.loc[key, k] = v

        df = df.fillna(value='X')
        df = df.sort_index(axis=1)

        #authorization
        gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)

        sh = gc.open(GOOGLE_SPREADSHEET_NAME)

        #select the first sheet 
        wks = sh.worksheet('title','midterm01')

        #update the first sheet with df, starting at cell B2. 
        wks.set_dataframe(df,(1,1), copy_index=True)
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"