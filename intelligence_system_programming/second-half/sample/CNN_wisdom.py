# %%
# 必要なライブラリをインポート

import torch
from torchvision import models, transforms

from PIL import Image
import json

from tkinter import filedialog


# %%
def main():
    ## torchvision.modelsからImageNet学習済みモデルを複数ロード
    model_vgg16 = models.vgg16(pretrained=True)
    model_alexnet = models.alexnet(pretrained=True)
    model_resnet152 = models.resnet152(pretrained=True)

    ##学習済みモデルとその名前をリスト化
    model_list = [model_vgg16, model_alexnet, model_resnet152]
    name_list = ["VGG16", "AlexNet", "ResNet"]

    ##すべてのモデルを評価モードに
    for model in model_list:
        model.eval()

    ##ImageNetの画像に合わせて入力画像を変形させる
    image_converter = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    ##ファイルダイアログで読み込むファイルタイプを指定．JPG画像のみ
    file_type = [("画像", "*.jpg")]
    ##ファイルダイアログで画像ファイルを指定．ファイルパスを得る．
    filepath = filedialog.askopenfilename(filetypes=file_type)

    ##入力画像を指定されたフォーマットに変形，バッチデータ化
    target_image = Image.open(filepath)
    converted_image = image_converter(target_image)
    batch = converted_image[None]

    ##ImageNetの推論カテゴリ番号と対応する名前のデータをロード
    with open("./imagenet_class_index.json") as file:
        labels = json.load(file)

        ##各モデルごとに画像データを推論
        for model, name in zip(model_list, name_list):
            result = model(batch)

            possibility_result = result[0].softmax(dim=0)  ##結果をソフトマックス関数で確率に変換

            confidence = torch.max(possibility_result).item()  ##最も高い確率を取得
            result_index = torch.argmax(possibility_result)  ##最も高い確率のインデックスを取得
            answer = labels[str(result_index.item())]  ##カテゴリの名前を取得

            ##確率にあわせて語尾を選ぶ
            confidence_word = ""
            if confidence > 0.75:
                confidence_word = "だね．"
            elif confidence > 0.5:
                confidence_word = "かなあ？"
            else:
                confidence_word = "...知らんけど..."

            ##結果を表示
            print(name + "> " + answer[1] + confidence_word)


# %%
if __name__ == "__main__":
    main()

# %%
