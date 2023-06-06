# %%
# 必要なライブラリのインポート
import pandas as pd
import math
import random

# データを読み込む
df = pd.read_excel("sangyohi.xlsx", skiprows=10, usecols="B:AE", index_col=0)

# データのインデックスと値を取得
index = df.index  # ['北海道', '青森',... ]
data = df.values  #

# クラスタの数
k = 6


# ユークリッド距離
def euclidean_distance(x, y):
    num_dimensions = len(x)
    return math.sqrt(sum((x[i] - y[i]) ** 2 for i in range(num_dimensions)))


# %%
# 各データ間の距離を計算し、距離の和が小さい順にk個のデータを選ぶ
def calc_representative_data(n_cluster=2):
    representative_data = [None] * n_cluster
    for k in range(n_cluster):
        min_distance_sum = float("inf")  # 代表データの距離の和の最小値を無限大で初期化

        # 各データ間の距離を計算
        for i in range(len(data)):
            distance_sum = 0  # データの距離の和を初期化

            # すでに代表データとして選ばれているデータはスキップ
            if i in representative_data:
                continue

            # データiと他のデータとの距離の和を計算
            for j in range(len(data)):
                distance = euclidean_distance(data[i], data[j])
                distance_sum += distance

            # 距離の和が小さいデータを代表データとして選ぶ
            if distance_sum < min_distance_sum:
                min_distance_sum = distance_sum
                representative_data[k] = i

    return representative_data


# %%
# 各クラスタの重心を計算して更新する
def calc_centroids(n_cluster=2, centroids=None, clusters=None):
    # データの次元数
    num_dimensions = len(data[0])
    # 新しい重心を格納するリスト
    new_centroids = [None] * n_cluster

    for k in range(n_cluster):
        cluster_data = [data[i] for i in range(len(data)) if clusters[i] == k]
        cluster_size = len(cluster_data)
        centroid = [sum(dim) / cluster_size for dim in zip(*cluster_data)]
        new_centroids[k] = centroid

    # ここに重心を計算するコードを書く
    return new_centroids


# %%
def kmanes(n_cluster=2):
    # 代表データを獲得
    centroids = calc_representative_data(n_cluster)
    # クラスタを初期化
    clusters = [None] * len(data)

    while True:
        # クラスタ割り当ての更新
        for i in range(len(data)):
            distances = [
                euclidean_distance(data[i], data[centroid]) for centroid in centroids
            ]
            clusters[i] = distances.index(min(distances))

        # 重心の更新
        new_centroids = calc_centroids(n_cluster, centroids, clusters)

        # 重心が収束したかどうかの判定
        if new_centroids == centroids:
            break

        centroids = new_centroids

    return clusters


# %%
clusters = kmanes(n_cluster=k)
print(clusters)
