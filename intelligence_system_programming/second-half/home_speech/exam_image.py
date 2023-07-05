# %%
import random
import torch
from torchvision import models, transforms
from PIL import Image
import json
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from tkinter import filedialog

# %%
# torchvision.modelsからImageNet学習済みモデルを複数ロード
cnn_model = models.resnet152(pretrained=True)

# 翻訳モデルをロード
translator = pipeline("translation", model="staka/fugumt-en-ja")

# モデルを評価モードに
cnn_model.eval()

# %%
##ImageNetの画像に合わせて入力画像を変形させる
image_converter = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# 画像を褒めてもらう場合
print("あなたの褒めてほしい画像を選択してください")
# ファイルダイアログで読み込むファイルタイプを指定．JPG画像のみ
file_type = [("画像", "*.jpg")]
# ファイルダイアログで画像ファイルを指定．ファイルパスを得る．
filepath = filedialog.askopenfilename(filetypes=file_type)

# ImageNetの画像に合わせて入力画像を変形させる
target_image = Image.open(filepath)
converted_image = image_converter(target_image)
batch = converted_image[None]

##ImageNetの推論カテゴリ番号と対応する名前のデータをロード
with open("../sample/imagenet_class_index.json") as file:
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
    translated_answer = translator(replase_answer, max_length=40)[0]["translation_text"]

    # 結果を表示
    print(f"あなたの画像は{translated_answer}ですね！")

# %%
text = "sports_car"

text = text.replace("_", " ")

translated_answer = translator(text, max_length=40)[0]["translation_text"]

# 結果を表示
print(f"あなたの画像は{translated_answer}ですね！")
# %%
