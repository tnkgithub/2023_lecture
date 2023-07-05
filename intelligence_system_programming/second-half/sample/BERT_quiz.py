# %%
import torch

from transformers import AutoTokenizer, AutoModelForMaskedLM


# %%
def main():
    ##TokenizerとLanguage modelを用意．日本語BERTを指定．
    tokenizer = AutoTokenizer.from_pretrained(
        "cl-tohoku/bert-base-japanese-whole-word-masking"
    )
    model = AutoModelForMaskedLM.from_pretrained(
        "cl-tohoku/bert-base-japanese-whole-word-masking"
    )
    ## Language modelを評価モードに
    model.eval()

    ##クイズの問題文を用意
    quiz_text_list = [
        "大乱闘スマッシュブラザーズは任天堂の有名なゲーム。中でも人気のキャラクターはソニック、カービィ、???です。",
        "ポケモンは任天堂の有名なゲーム。中でも人気のキャラクターはピカチュウ、イーブイ、???です。",
        "今日はいい天気だな。そうだ、???しよう！",
        "男は大きな斧を持っているのがわかった。男は立ち止まりこちらを振り返ると、「???だ！」と言ってこちらへ向かってきた。",
        "???は激怒した。必ず、かの邪智暴虐の王を除かなければならぬと決意した",
    ]

    ##タイトル＆ルール説明
    print("---BERT Quiz Show---")
    print("問題文の???にBERTが何を入れるか予想しよう！")

    ##合計獲得点数
    total_point = 0

    ##１問ずつ実行
    for quiz_text in quiz_text_list:
        ##問題表示
        print("問題：" + quiz_text)

        ##入力を促して，入力内容を取得
        print("あなたの予想は？↓")
        input_str = input()
        print("あなたの予想：" + input_str)

        ##問題文をBERTへの入力形式に変更，「???」を「[MASK]」に
        quiz_text_f = quiz_text.replace("???", tokenizer.mask_token)

        ##問題文をtoken idの列に変換
        input_ids = tokenizer.encode(quiz_text_f, return_tensors="pt")
        ##問題文中の[MASK]の位置を取得
        masked_index = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]

        # 推論実行
        with torch.no_grad():  # 計算グラフを作らず勾配計算を行わないようにする．
            results = model(input_ids)  ##[MASK]部分を推論
            predictions = results[0][0, masked_index].topk(30)  # 推論結果上位30件を取得
            pred_ids = predictions.indices.tolist()  ##結果をリスト形式に

            # 結果表示＆得点計算
            point = 0

            ##1位から順に表示
            for i, pred_id in zip(range(len(pred_ids)), pred_ids):
                word_ids = [pred_id]
                decoded_word = tokenizer.decode(word_ids)
                print(str(i + 1) + "位:" + decoded_word)
                if input_str == decoded_word:
                    point = 30 - i  ##入力された回答と結果が一致すれば点数を与える，上位のほうが高得点
            ##結果表示
            if point > 0:
                print("正解！ " + str(point) + "点獲得！")
            else:
                print("残念！")
            total_point += point  ##合計得点に加算
    ##最終結果表示
    print("最終結果： " + str(total_point) + "点！")


# %%
if __name__ == "__main__":
    main()

# %%
