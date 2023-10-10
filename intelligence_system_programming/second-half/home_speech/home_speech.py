"""
    ある単語を入力すると
    テンプレートに沿ったほめる文章を出力する
"""
# %%
import random
import torch
from torchvision import models, transforms
from PIL import Image
import json
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from tkinter import filedialog

# %%
# テンプレート
template_list = [
    "{}はとても{}です",
    "あなたの{}は{}です",
    "あなたの{}はとても{}ですね",
    "あなたの{}がとても{}なので好きです",
]

# 画像用テンプレート
template_image_list = [
    "この{}は{}です",
    "この{}はとても{}ですね",
    "{}がとても{}なので好きです",
]

# 褒められない場合のテンプレート
template_no_praise_list = [
    "あなたの{}は褒められるようなものではありません",
    "あなたの{}はとてもじゃないですが褒められるようなものではありません",
    "あなたの{}はお世辞にも褒められるようなものではありません",
]

# 画像用褒められない場合のテンプレート
template_no_praise_image_list = [
    "この{}は褒められるようなものではありません",
    "この{}はとてもじゃないですが褒められるようなものではありません",
    "この{}はお世辞にも褒められるようなものではありません",
]

# 褒め言葉のリスト
praise_list = [
    "かわいい",
    "美しい",
    "素敵",
    "優しい",
    "頭がいい",
    "かっこいい",
    "面白い",
    "すごい",
    "優れている",
    "すばらしい",
    "最高",
    "最強",
    "頼もしい",
    "尊敬",
    "才能ある",
    "センスがいい",
    "センスが抜群",
    "センスが最高",
    "センスが最強",
    "センスがすごい",
    "センスがすばらしい",
    "魅力的",
    "一流",
    "天才的",
    "優雅",
    "気品がある",
    "多才",
    "うまい",
    "完璧",
    "きれい",
    "速い",
    "強い",
    "賢い",
    "優秀",
    "優勝",
    "太い",
    "大きい",
    "細い",
    "小さい",
    "軽い",
    "長い",
    "高い",
]


# %%
def home_speech(tokenizer, model):
    # 入力を促して，入力内容を取得
    print("あなたの褒めてほしいワードは？単語で入力して↓")
    input_str = input()

    # テンプレートをランダムに選択
    template = random.choice(template_list)
    template_no_praise = random.choice(template_no_praise_list)

    # テンプレートに入力を埋め込み
    input_text = template.format(input_str, tokenizer.mask_token)

    # テンプレートをtoken idの列に変換
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # [MASK]の位置を取得
    masked_index = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]

    # 推論実行

    with torch.no_grad():  # 計算グラフを作らず勾配計算を行わないようにする．
        results = model(input_ids)  ##[MASK]部分を推論
        predictions = results[0][0, masked_index].topk(50)  # 推論結果上位30件を取得
        pred_ids = predictions.indices.tolist()  ##結果をリスト形式に
        # 推論結果の上位50件の単語内に褒め言葉リストと似た単語があるか確認
        # あれば一番上の単語を出力
        # 無ければ褒められない文章を出力
        for pred_id in pred_ids:
            flag = False
            pred_str = tokenizer.convert_ids_to_tokens([pred_id])[0]
            if pred_str in praise_list:
                print(template.format(input_str, pred_str))
                break
            else:
                flag = True
                continue
        if flag:
            print(template_no_praise.format(input_str))

    return


def home_image(tokenizer, bert_model):
    # torchvision.modelsからImageNet学習済みモデルを複数ロード
    cnn_model = models.resnet152(pretrained=True)

    # 翻訳モデルをロード
    translator = pipeline("translation", model="staka/fugumt-en-ja")

    # モデルを評価モードに
    cnn_model.eval()

    # 画像を褒めてもらう場合
    print("あなたの褒めてほしい画像を選択してください")
    # ファイルダイアログで読み込むファイルタイプを指定．JPG画像のみ
    file_type = [("画像", "*.jpg")]
    # ファイルダイアログで画像ファイルを指定．ファイルパスを得る．
    filepath = filedialog.askopenfilename(filetypes=file_type)

    ##ImageNetの画像に合わせて入力画像を変形させる
    image_converter = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    # ImageNetの画像に合わせて入力画像を変形させる
    target_image = Image.open(filepath)
    converted_image = image_converter(target_image)
    batch = converted_image[None]

    ##ImageNetの推論カテゴリ番号と対応する名前のデータをロード
    with open(
        "/home/sumthen/2023/2023_lecture/intelligence_system_programming/second-half/sample/imagenet_class_index.json"
    ) as file:
        labels = json.load(file)

        # 画像を推論
        result = cnn_model(batch)

        # 結果をソフトマックス関数で確率に変換
        possibility_result = result[0].softmax(dim=0)

        # 最も高い確率を取得
        confidence = torch.max(possibility_result).item()

        # 最も高い確率のインデックスを取得
        result_index = torch.argmax(possibility_result)

        # カテゴリの名前を取得
        answer = labels[str(result_index.item())]

        # カテゴリ名を単語に分割
        replase_answer = answer[1].replace("_", " ")

        # 翻訳
        translated_answer = translator(replase_answer, max_length=40)[0][
            "translation_text"
        ]

        # テンプレートをランダムに選択
        template = random.choice(template_image_list)
        template_no_praise = random.choice(template_no_praise_image_list)

        # テンプレートに入力を埋め込み
        input_text = template.format(translated_answer, tokenizer.mask_token)

        # テンプレートをtoken idの列に変換
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # [MASK]の位置を取得
        masked_index = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]

        # 推論実行
        with torch.no_grad():  # 計算グラフを作らず勾配計算を行わないようにする．
            results = bert_model(input_ids)  ##[MASK]部分を推論
            predictions = results[0][0, masked_index].topk(50)  # 推論結果上位30件を取得
            pred_ids = predictions.indices.tolist()  ##結果をリスト形式に
            # 推論結果の上位50件の単語内に褒め言葉リストと似た単語があるか確認
            # あれば一番上の単語を出力
            # 無ければ褒められない文章を出力
            for pred_id in pred_ids:
                flag = False
                pred_str = tokenizer.convert_ids_to_tokens([pred_id])[0]
                if pred_str in praise_list:
                    print(template.format(translated_answer, pred_str))
                    break
                else:
                    flag = True
                    continue
            if flag:
                print(template_no_praise.format(translated_answer))

    return


def main():
    tokenizer = AutoTokenizer.from_pretrained(
        "cl-tohoku/bert-base-japanese-whole-word-masking"
    )
    bert_model = AutoModelForMaskedLM.from_pretrained(
        "cl-tohoku/bert-base-japanese-whole-word-masking"
    )
    # Language modelを評価モードに
    bert_model.eval()

    # %%
    # 使用方法の説明
    print("画像か単語を褒めてもらおう！")
    print("あなたが褒めて欲しいのは画像ですか？それとも単語ですか？")

    # 画像か単語を選択させる
    print("画像なら1を，単語なら2を入力してください")
    input_num = input()

    if input_num == "1" or input_num == "１":
        home_image(tokenizer, bert_model)
    elif input_num == "2" or input_num == "２":
        home_speech(tokenizer, bert_model)


# %%
# if __name__ == "__main__":
main()

# %%
