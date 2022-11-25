from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import UploadImgForm
from .models import UploadImgModel
import sys

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
            title = form.cleaned_data['title']
            img = form.cleaned_data['img']

            # formから得たデータを、データベースに保存
            modes_data = UploadImgModel.objects.create(
                title=title, img=img, success_number=0, result1=img, 
                result2=img, result3=img, result4=img, result5=img, 
                result6=img, result7=img, result8=img, result9=img, 
                result10=img, result11=img, result12=img, result13=img)
            modes_data.save()
            
            #「model.py」のクラス内の関数を実行し、フィールド「result」に格納
            UploadImgModel.transform(modes_data)

            # データベースに保存された画像のURLをセッションに保存
            request.session['title'] = modes_data.title
            request.session['original_url'] = modes_data.img.url

            # 補正に成功した画像の数だけ、補正画像へのURLを格納
            count = 0
            if modes_data.success_number >= count + 1:
                request.session['result1_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result1_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result2_url'] = modes_data.result2.url
                count = count + 1
            else:
                request.session['result2_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result3_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result3_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result4_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result4_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result5_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result5_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result6_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result6_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result7_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result7_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result8_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result8_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result9_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result9_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result10_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result10_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result11_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result11_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result12_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result12_url'] = modes_data.img.url
            #
            if modes_data.success_number >= count + 1:
                request.session['result13_url'] = modes_data.result1.url
                count = count + 1
            else:
                request.session['result13_url'] = modes_data.img.url
            #
            

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
    title = request.session.get('title')
    original_url = request.session.get('original_url')

    success_number = request.session['success_number']

    # result1 〜 result13   # マスク画像の個数に応じて出力
    result_cv = []
    result_cv.append(request.session.get('result1_url'))
    result_cv.append(request.session.get('result2_url'))
    result_cv.append(request.session.get('result3_url'))
    result_cv.append(request.session.get('result4_url'))
    result_cv.append(request.session.get('result5_url'))
    result_cv.append(request.session.get('result6_url'))
    result_cv.append(request.session.get('result7_url'))
    result_cv.append(request.session.get('result8_url'))
    result_cv.append(request.session.get('result9_url'))
    result_cv.append(request.session.get('result10_url'))
    result_cv.append(request.session.get('result11_url'))
    result_cv.append(request.session.get('result12_url'))
    result_cv.append(request.session.get('result13_url'))

    params = {
        'title': title,
        'original_url': original_url,
        'result_url': result_cv,
        'success_number': success_number,
        }

    return render(request, 'auto_ks_app/ks_transform.html', params)
# ------------------------------------------------------------------