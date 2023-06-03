'''
" #%% " はvisutal studio code上で" #%% " で囲まれた範囲をjupyter notebookのcellのように実行できるようにするものです。
'''

#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%
# csvファイルを読み込み、numpy配列に変換
df = pd.read_csv('sangyohi.csv', header=None)
data = df.values

# %%
