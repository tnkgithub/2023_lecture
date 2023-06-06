"""
" #%% " はvisutal studio code上で" #%% " で囲まれた範囲をjupyter notebookのcellのように実行できるようにするものです。
"""

# %%
import numpy as np
import pandas as pd

# %%
# csvファイルを読み込む
df = pd.read_excel("sangyohi.xlsx", skiprows=10, usecols="B:AE", index_col=0)
labels = df.index

print(labels)

n_cluster = 2


# %%
# ユークリッド距離
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


print(euclidean_distance(df.values[0], df.values[1]))


# %%
# k-means法
def kmeans(x, k=2, max_iter=1000):
    # データの次元数
    dim = x.shape[1]
    # データ数
    n = x.shape[0]
    # 代表データを事例データからランダムに選ぶ
    mu = x[np.random.choice(n, k, replace=False)]
    # 代表データの属するクラスターを表す行列
    r = np.zeros((n, k))
    # 収束する or 最大繰り返し回数に達するまで繰り返す
    for _ in range(max_iter):
        # 代表データと事例データとの距離を計算
        d = np.zeros((n, k))
        for i in range(k):
            for j in range(n):
                d[j, i] = euclidean_distance(mu[i], x[j])
        # 事例データを最も近い代表データのクラスターに割り当てる
        r = np.zeros((n, k))
        for i in range(n):
            r[i, np.argmin(d[i])] = 1
        # 代表データを更新
        mu = np.zeros((k, dim))
        for i in range(k):
            mu[i] = np.sum(r[:, i].reshape(n, 1) * x, axis=0) / np.sum(r[:, i])

    return mu, r


# %%
# k-means法を実行
mu, r = kmeans(df.values, n_cluster)

# 結果を表示
for i in range(n_cluster):
    print("クラスター{}:".format(i))
    print(labels[r[:, i] == 1])
    print()

# %%
