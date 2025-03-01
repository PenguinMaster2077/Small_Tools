import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'Head_Files'))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import zhplot
from datetime import datetime, timedelta
# Self-Defined
import Count_Head

Pic_Dir = "/home/penguin/Small_Tools/Count_Money/Pics"
CSV_Path = "/mnt/e/账本/2024.csv"
Count_Head.Analysis_Monthly(CSV_Path, Pic_Dir)
Count_Head.Analysis_All(CSV_Path, Pic_Dir)

 