from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import UploadImgForm
# from .models import UploadImgModel

from auto_ks_app.views_modules import cv2_calc
from auto_ks_app.views_modules import pil_cv_binary
from auto_ks_app.views_modules import s3_dave

import sys
import cv2
from PIL import Image

# ------------------------------------------------------------------


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
            bucket_name = "ks-img-save"
            file_name = "img.png"
            cv2.imwrite(file_name, cv_img)
            original_url = s3_dave.file_boto3(file_name, bucket_name)
            # -----------------------------------------------------------


            # アップロードされたimgファイルからPIL画像オブジェクト生成
            pil_img = pil_cv_binary.binar2pil(img_obj)

            # PIL画像をOpenCV画像に変換
            cv_img = pil_cv_binary.pil2opencv(pil_img)

            # OpenCVでの画像処理（台形補正）
            mask_df = 20  # min閾値どうしの差
            mask_number = int(250 / mask_df) + 1  # マスク画像の数(min閾値の数)
            cv_calc_img, success = cv2_calc.auto_keystone(
                cv_img, mask_df, mask_number
            )


            # -----------------------------------------------------------
            # S3へのアップロード
            # -----------------------------------------------------------
            bucket_name = "ks-img-save"
            s3_img_url = []

            for k , c_img in enumerate(cv_calc_img):
                number = str(k)
                file_name = 'ks_img' + number + '.png'
                cv2.imwrite(file_name, c_img)
                s3_img_url.append(s3_dave.file_boto3(file_name, bucket_name))

            params = {
                'original_url': original_url,
                'result_url': s3_img_url,
                'success_number': success,
                'form': form,
            }
            form = UploadImgForm()
            return render(request, 'auto_ks_app/ks_result.html', params)

    else:
        form = UploadImgForm()
    
    # # -----------------------------------------------------------
    # # S3へのアップロード
    # # -----------------------------------------------------------
    # bucket_name = "sample-img-save"

    # file_name = './sample_img.png'
    # file_path = './data/sample_img/ks_img1.png'
    # sample_img = cv2.imread(file_path)
    # cv2.imwrite(file_name, sample_img)

    # sample_img_url = s3_dave.file_boto3(file_name, bucket_name)
    # # -----------------------------------------------------------

    return render(request, 'auto_ks_app/ks_upload.html', {'form': form} )

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

#     return render(request, 'auto_ks_app/ks_transform.html', params)
# ------------------------------------------------------------------