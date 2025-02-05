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
CSV_Path = "/mnt/d/2024.csv"
# Count_Head.Analysis("2025-01-10", "2025-01-20", Pic_Dir)
# Count_Head.Analysis("0", "0", CSV_Path, Pic_Dir, 2)
Count_Head.Analysis_Monthly(CSV_Path, Pic_Dir, 1)