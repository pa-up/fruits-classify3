from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import UploadImgForm
from .models import UploadImgModel
from auto_ks_app.views_modules import s3_dave
import sys
import cv2

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

            # formから得たデータを、データベースに保存
            modes_data = UploadImgModel.objects.create(
                img=img, success_number=0
            )
            modes_data.save()
            
            #「model.py」のクラス内の関数を実行し、フィールド「result」に格納
            cv_calc_img = UploadImgModel.transform(modes_data)

            # データベースに保存された入力画像のURLをセッションに保存
            request.session['original_url'] = modes_data.img.url

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

            request.session['s3_img_url'] = s3_img_url
            request.session['success_number'] = modes_data.success_number
            
            return HttpResponseRedirect(reverse('auto_ks_app:transform'))

    else:
        form = UploadImgForm()
    return render(request, 'auto_ks_app/ks_upload.html', {'form': form})
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
    s3_img_url = request.session['s3_img_url']

    params = {
        'original_url': original_url,
        'result_url': s3_img_url,
        'success_number': success_number,
        }

    return render(request, 'auto_ks_app/ks_transform.html', params)
# ------------------------------------------------------------------