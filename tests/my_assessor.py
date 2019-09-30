from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

import os
import subprocess as sp
import datetime
from pathlib import Path 

import pandas as pd
import numpy as np

MONTH = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

from config import *
from instance.config import *
import pygsheets

class Assess(object):
    def __init__(self, month, day):
        self._month = month
        self._day = day
        self.insertion_cnts = 0
        self.deletion_cnts = 0
        self.logs = ""
        pass

    def get_date(self):
        return MONTH[self._month] + self._day

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
        self.insert_state("PROCESS", 1)

        self.insert_input_port("assess")
        self.insert_input_port("report")
        self.insert_output_port("done")

        self.assessed_students = {}
        self.current_student = None
        self.asessment_file_path = ""

    def process_daily_commits(self, _id, _git_id, _date, eval_dir):
        print(f"Evaluating {_id}'s commit logs")
        
        bProcess = False
        stu_log = eval_dir + "/" + _id + ".log"
        with open(stu_log, "rb") as f:
            for line in f:
                line = line.decode().strip()

                if line and ("!!@@##") in line:
                    preprocessed = line.split(',')
                    splitedItems = preprocessed[1].split()
                    date = MONTH[splitedItems[1]] + splitedItems[2]

                    if _id not in self.assessed_students:
                        self.assessed_students[_id] = {}

                    if date not in self.assessed_students[_id]:
                        self.assessed_students[_id][date] = Assess(splitedItems[1], splitedItems[2])
                        self.current_student = self.assessed_students[_id][date]
                    bProcess = True

                if bProcess:
                    bProcess = not self.current_student.check(line)


    def ext_trans(self,port, msg):
        if port == "assess":
            data = msg.retrieve()
            #print(data)
            home_dir = os.getcwd()
            eval_dir = home_dir + "/assessment/" + data[3] # date
            
            self.process_daily_commits(data[0], data[1], data[3], eval_dir)
        
        if port == "report":
            data = msg.retrieve()
            self.asessment_file_path = data[0]
            self._cur_state = "PROCESS"
            

    def output(self):

        df = pd.DataFrame('', index=[], columns=[])
        for key, value in self.assessed_students.items():
            for k, v in value.items():
                df.loc[key, k] = 'O'

        print(df)
        df = df.fillna(value='X')
        df = df.sort_index(axis=1)
        print(df)
        #df.sort_index(axis=0)
        df.to_csv(self.asessment_file_path)

        #authorization
        gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)

        # Create empty dataframe
        #df = pd.DataFrame()

        # Create a column
        #df['name'] = ['John', 'Steve', 'Sarah']

        #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
        sh = gc.open('SIT22005-201902')

        #select the first sheet 
        wks = sh[0]

        #update the first sheet with df, starting at cell B2. 
        wks.set_dataframe(df,(1,1), copy_index=True)
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"