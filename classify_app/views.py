from django.shortcuts import render
from .forms import UploadImgForm

from classify_app.views_modules import pil_cv_binary
from classify_app.views_modules import s3_dave

import cv2
import numpy as np
from PIL import Image
from tensorflow.python.keras.models import load_model
import requests


def img_up(request):
    if request.method == 'POST':
        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img_obj = request.FILES['img']

            #========================================================
            # 入力画像を処理・保存
            #========================================================
            pil_img = Image.open(img_obj)
            cv_img = pil_cv_binary.pil2opencv(pil_img)

            # -----------------------------------------------------------
            # S3へのアップロード
            # -----------------------------------------------------------
            bucket_name = "fruits-classify"
            file_name = "img.png"
            cv2.imwrite(file_name, cv_img)
            original_url = s3_dave.file_boto3(file_name, bucket_name)
            # -----------------------------------------------------------


            # アップロードされたimgファイルからPIL画像オブジェクト生成
            pil_img = pil_cv_binary.binar2pil(img_obj)

            # PIL画像をOpenCV画像に変換
            cv_img = pil_cv_binary.pil2opencv(pil_img)

            # 前処理
            cv_img = cv2.cvtColor( cv_img , cv2.COLOR_BGR2RGB )
            resize_settings = (50,50)  # リサイズ設定
            cv_img = cv2.resize(cv_img, dsize=resize_settings)  # リサイズ実行
            x_01 = cv_img.astype("float") / cv_img.max()  # 0~255の整数 → 0~1の数値
            x_up_model = x_01[np.newaxis , : , : , :]  # TensorFlow に適合するデータ型に変更

            # モデルの読み込み
            s3_static_url='https://fruits-classify.s3.ap-northeast-1.amazonaws.com/fruits_classify.h5'
            filename='fruits_classify_url.h5'
            urlData = requests.get(s3_static_url).content
            with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
                f.write(urlData)
            ai_model = load_model(filename)
            print(ai_model)
            
            # モデルの実行
            y = ai_model.predict(x_up_model)
            labels = ["grape" , "apple" , "orange"]  
            classify_result = str( labels[np.argmax(y[0 , :])] )

            # HTMLに渡す変数
            params = {
                'original_url': original_url,
                'classify_result': classify_result,
            }
            # 再入力フォーム
            form = UploadImgForm()
            return render(request, 'classify_app/classify.html', params)

    else:
        form = UploadImgForm()
    
    # HTMLに渡す変数
    params = {
        'form': form,
    }
    return render(request, 'classify_app/fruits_upload.html', params)

# ------------------------------------------------------------------



# def transform(request):
#     # セッションから画像URLを取り出す
#     original_url = request.session.get('original_url')
#     success_number = request.session['success_number']
#     s3_img_url = request.session['s3_img_url']  # OpenCV処理画像

#     params = {
#         'original_url': original_url,
#         'result_url': s3_img_url,
#         'success_number': success_number,
#         }

#     return render(request, 'classify_app/ks_transform.html', params)
# ------------------------------------------------------------------