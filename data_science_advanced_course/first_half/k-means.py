#%%
import csv
import math
import random

# csvファイルのパス
csv_file = 'sangyohi.csv'

# データを格納するリスト
data = []

# データのインデックス
index = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県',
    '山形県', '福島県', '茨城県', '栃木県', '群馬県',
    '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県',
    '富山県', '石川県', '福井県', '山梨県', '長野県',
    '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県',
    '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県',
    '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県',
    '鹿児島県', '沖縄県'
]

# csvファイルからデータを読み込む
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append([float(value) for value in row])

# データの次元数
num_dimensions = len(data[0])

# クラスタの数
k = 6

# 各データ点をランダムに初期クラスタに割り当てる
clusters = [random.randint(0, k-1) for _ in range(len(data))]

# 中心点を再計算する
def recalculate_centroids():
    centroids = [[] for _ in range(k)]
    for i, point in enumerate(data):
        cluster = clusters[i]
        centroids[cluster].append(point)
    return [list(map(lambda x: sum(x) / len(x), zip(*centroid_points))) for centroid_points in centroids]

# k-means法でクラスタリングを行う
num_iterations = 20  # 反復回数
iter = 0
for _ in range(num_iterations):
    centroids = recalculate_centroids()

    # 各データ点を最も近い中心点に割り当てる
    new_clusters = []
    for point in data:
        distances = [math.sqrt(sum((point[i] - centroids[j][i]) ** 2 for i in range(num_dimensions))) for j in range(k)]
        nearest_cluster = min(range(k), key=lambda x: distances[x])
        new_clusters.append(nearest_cluster)

    # クラスタの割り当てが変わらなければ終了
    # if new_clusters == clusters:
    #     break
    clusters = new_clusters
    iter += 1

print('iter:', iter)

# クラスタリング結果を表示
for i in range(k):
    print('クラスタ', i+1)
    for j in range(len(data)):
        if clusters[j] == i:
            print(index[j], end=' ')
    print()


# %%
