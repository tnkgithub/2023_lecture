# %%
import numpy as np
import pandas as pd

# xlsxファイルを読み込む
df = pd.read_excel("sangyohi.xlsx", skiprows=10, usecols="B:AE", index_col=0)
# 都道府県名を取得
labels = df.index
# 見やすいよう成形
labels = np.array(labels.str.replace(" ", "").str.replace("　", ""))

# データをnumpy配列に変換
df = df.values

# クラスタの数
n_cluster = 8


# ユークリッド距離を計算する関数
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


# k-means法
def kmeans(x, k=2, max_iter=1000):
    # データの次元数
    dimention = x.shape[1]
    # データ数
    n = x.shape[0]
    # # 事例データから代表データをランダムに選ぶ
    centroids = x[np.random.choice(n, k, replace=False)]
    # 収束する or 最大繰り返し回数に達するまで繰り返す
    for iter in range(max_iter):
        distance = np.zeros((n, k))
        for i in range(k):
            for j in range(n):
                # 重心と事例データとの距離を計算
                distance[j, i] = euclidean_distance(centroids[i], x[j])

        # クラスタを入れる配列を用意
        clusters = np.zeros((n, k))
        for i in range(n):
            # 最も距離が近い重心のクラスタに割り当てる
            clusters[i, np.argmin(distance[i])] = 1

        # 新しい重心を入れる配列を用意
        new_centroids = np.zeros((k, dimention))
        # クラスタごとに重心を計算
        for i in range(k):
            # クラスタiに属するデータの平均を計算
            new_centroids[i] = np.mean(x[clusters[:, i] == 1], axis=0)
        # 収束判定
        # 重心が変化しなければ終了
        if np.allclose(centroids, new_centroids):
            break
        # 重心を更新
        centroids = new_centroids

    return centroids, clusters


# k-means法を2000回実行し、最も良い結果を表示する
# 重心と事例データとの距離の和を保存する辞書
result = {}
for _ in range(2000):
    # k-means法を実行
    centroids, clusters = kmeans(df, n_cluster)
    # 距離の和を初期化
    distance_sum = 0

    # 全クラスタの重心と事例データとの距離の和を計算
    for k in range(n_cluster):
        for i in range(len(df)):
            if clusters[i, k] == 1:
                distance_sum += euclidean_distance(centroids[k], df[i])

    # 結果を保存
    result[distance_sum] = (centroids, clusters)

# 重心と事例データとの距離の和が最小のものを選ぶ
centroids, clusters = result[min(result.keys())]

# 結果を表示
for i in range(n_cluster):
    print("クラスタ{}:".format(i))
    print(labels[clusters[:, i] == 1])
    print()
# %%