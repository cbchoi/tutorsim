from config import *
from instance.config import *

import pygsheets
import pandas as pd
import numpy as np

DAILY, VERIFY_DAILY_ID, VERIFY_DAILY_PW, VERIFIED_DAILY = range(4)

#authorization
gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)

sh = gc.open(GOOGLE_SPREADSHEET_NAME)
wks = sh.worksheet('title','Daily')

student_list_df = wks.get_as_df()
res = student_list_df.loc[student_list_df['ID'] == 21900000, :]

columns = list(res)
for i in columns:
    print(i, str(res[i].values[0]))
    #print(res[i][0])