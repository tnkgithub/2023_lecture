'''
" #%% " はvisutal studio code上で" #%% " で囲まれた範囲をjupyter notebookのcellのように実行できるようにするものです。
'''

#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%
# データを読み込み、numpy配列(float)に変換
df = pd.read_csv('sangyohi.csv')
features = df.to_numpy()
features = features.astype(np.float32)

# %%
# クラスタ数
n_clusters = [2, 3, 4, 5, 6]
