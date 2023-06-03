// k-means法によるクラスタリング

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

// csvファイルの読み込み
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class question_1 {
    public static void main(String[] args) {
        // csvファイルの読み込み
        List<String[]> data = new ArrayList<String[]>();
        try {
            BufferedReader br = new BufferedReader(new FileReader("sangyohi.csv"));
            String line;
            while ((line = br.readLine()) != null) {
                data.add(line.split(","));
            }
            br.close();
        } catch (IOException e) {
            System.out.println(e);
        }

        // データの整形
        double[][] data_array = new double[data.size()][2];
        for (int i = 0; i < data.size(); i++) {
            data_array[i][0] = Double.parseDouble(data.get(i)[0]);
            data_array[i][1] = Double.parseDouble(data.get(i)[1]);
        }

        // クラスタリング
        int k = 3;
        int[] cluster = k_means(data_array, k);

        // 結果の表示
        for (int i = 0; i < data_array.length; i++) {
            System.out.println(data_array[i][0] + "," + data_array[i][1] + "," + cluster[i]);
        }
    }

    // k-means法によるクラスタリング
    public static int[] k_means(double[][] data, int k) {
        // データの次元数
        int dim = data[0].length;

        // クラスタの初期化
        double[][] cluster = new double[k][dim];
        Random rand = new Random();
        for (int i = 0; i < k; i++) {
            cluster[i] = data[rand.nextInt(data.length)];
        }

        // クラスタリング
        int[] cluster_index = new int[data.length];
        while (true) {
            // クラスタの更新
            int[] cluster_count = new int[k];
            double[][] cluster_sum = new double[k][dim];
            for (int i = 0; i < data.length; i++) {
                // 最も近いクラスタを探索
                int min_index = 0;
                double min_dist = Double.MAX_VALUE;
                for (int j = 0; j < k; j++) {
                    double dist = 0;
                    for (int l = 0; l < dim; l++) {
                        dist += Math.pow(data[i][l] - cluster[j][l], 2);
                    }
                    if (dist < min_dist) {
                        min_index = j;
                        min_dist = dist;
                    }
                }

                // クラスタの更新
                cluster_count[min_index]++;
                for (int j = 0; j < dim; j++) {
                    cluster_sum[min_index][j] += data[i][j];
                }

                // クラスタの割り当て
                cluster_index[i] = min_index;
            }
            for (int i = 0; i < k; i++) {
                for (int j = 0; j < dim; j++) {
                    cluster[i][j] = cluster_sum[i][j] / cluster_count[i];
                }
            }

            // クラスタの変化がなければ終了
            boolean flag = true;
            for (int i = 0; i < k; i++) {
                for (int j = 0; j < dim; j++) {
                    if (cluster[i][j] != cluster_sum[i][j] / cluster_count[i]) {
                        flag = false;
                    }
                }
            }
            if (flag) {
                break;
            }
        }
        return cluster_index;
    }
}