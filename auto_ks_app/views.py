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
            sys.stderr.write("*** img_up *** aaa ***\n")
            handle_uploaded_img(request.FILES['img'])
            img_obj = request.FILES['img']
            sys.stderr.write(img_obj.name + "\n")
            
            # djangoのform機能から、アップロード画像を取得
            img = form.cleaned_data['img']
            

            #========================================================
            # 入力画像を処理・保存
            #========================================================
            pil_img = Image.open(img)
            cv_img = pil_cv_binary.pil2opencv(pil_img)

            # -----------------------------------------------------------
            # S3へのアップロード
            # -----------------------------------------------------------
            bucket_name = "ks-img-save"
            file_name = "img.png"
            cv2.imwrite(file_name, cv_img)
            original_url = s3_dave.file_boto3(file_name, bucket_name)
            # -----------------------------------------------------------
            
            # 入力画像をセッション変数に保存
            request.session['original_url'] = original_url

            #========================================================


            #========================================================
            # 出力画像を処理・保存
            #========================================================
            # modes_data = UploadImgModel.objects.create(
            #     img=img, success_number=0
            # )
            # modes_data.save()

            # #「model.py」のクラス内の関数を実行し、フィールド「result」に格納
            # cv_calc_img = UploadImgModel.transform(modes_data)


            # アップロードされたimgファイルからPIL画像オブジェクト生成
            pil_img = pil_cv_binary.binar2pil(img)

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
            # -----------------------------------------------------------

            request.session['s3_img_url'] = s3_img_url  # OpenCV処理画像
            request.session['success_number'] = success

            #========================================================
            

            return HttpResponseRedirect(reverse('auto_ks_app:transform'))

    else:
        form = UploadImgForm()
    
    # -----------------------------------------------------------
    # S3へのアップロード
    # -----------------------------------------------------------
    bucket_name = "sample-img-save"
    sample_img_url = []
    sample_img = cv2.imread('./static/sample_img/ks_img1.png')

    file_name = 'sample_img' + '.png'
    cv2.imwrite(file_name, sample_img)
    sample_img_url = s3_dave.file_boto3(file_name, bucket_name)
    # -----------------------------------------------------------

    return render(request, 'auto_ks_app/ks_upload.html', {'form': form , 'sample_img_url': sample_img_url})
#
#
# ------------------------------------------------------------------


def handle_uploaded_img(img_obj):
    sys.stderr.write("*** handle_uploaded_img *** aaa ***\n")
    sys.stderr.write(img_obj.name + "\n")
    file_path = 'media/documents/' + img_obj.name
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in img_obj.chunks():
            sys.stderr.write("*** handle_uploaded_img *** ccc ***\n")
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_img *** eee ***\n")
#
# ------------------------------------------------------------------


def transform(request):
    # セッションから画像URLを取り出す
    original_url = request.session.get('original_url')
    success_number = request.session['success_number']
    s3_img_url = request.session['s3_img_url']  # OpenCV処理画像

    params = {
        'original_url': original_url,
        'result_url': s3_img_url,
        'success_number': success_number,
        }

    return render(request, 'auto_ks_app/ks_transform.html', params)
# ------------------------------------------------------------------