from django.db import models
from PIL import Image
import io
from auto_ks_app.views_modules import pil2cv
from auto_ks_app.views_modules import cv2_calc


# マスク画像の数 ＝ min閾値の数 = resultの数
mask_df = 20  # min閾値どうしの差
mask_number = int(250 / mask_df) + 1  # マスク画像の数(min閾値の数)


class UploadImgModel(models.Model):
    title = models.CharField(max_length=50, default='title')
    img = models.ImageField(upload_to='documents/')
    success_number = models.IntegerField(default=0)
    result1 = models.ImageField(upload_to='results/', default=img)
    result2 = models.ImageField(upload_to='results/', default=img)
    result3 = models.ImageField(upload_to='results/', default=img)
    result4 = models.ImageField(upload_to='results/', default=img)
    result5 = models.ImageField(upload_to='results/', default=img)
    result6 = models.ImageField(upload_to='results/', default=img)
    result7 = models.ImageField(upload_to='results/', default=img)
    result8 = models.ImageField(upload_to='results/', default=img)
    result9 = models.ImageField(upload_to='results/', default=img)
    result10 = models.ImageField(upload_to='results/', default=img)
    result11 = models.ImageField(upload_to='results/', default=img)
    result12 = models.ImageField(upload_to='results/', default=img)
    result13 = models.ImageField(upload_to='results/', default=img)

    #def transform(self, angle, gray):    #リクエスト値によってパラメータや処理オプションを選択させる機能

    def transform(self):   # self == UploadImgModel
        #==========================================================
        # アップロードされたimgファイルからPIL画像オブジェクト生成
        #==========================================================
        pil_img = Image.open(self.img)

        #==========================================================
        # PIL画像をOpenCV画像に変換
        #==========================================================
        cv_img = pil2cv.pil2opencv(pil_img)

        #==========================================================
        # OpenCVでの画像処理（台形補正）
        #==========================================================
        cv_calc_img, success = cv2_calc.auto_keystone(
            cv_img, mask_df, mask_number)
        self.success_number = success   # 補正に成功したマスク画像の数

        # 以下は、自作モジュールの関数「auto_keystone」で補正に成功した場合のみ実行
        # success の数だけループ
        # 2値化時のmin閾値でループ(現在は13個)
        for i, ks_img in enumerate(cv_calc_img):
            if success >= i + 1:
                #==========================================================
                # OpenCV画像をPIL画像に変換
                #==========================================================
                pil_calc_img = pil2cv.opencv2pil(ks_img)

                #==========================================================
                # 画像処理後の画像のデータをbufferに保存
                #==========================================================
                buffer = io.BytesIO()   # メモリ上のバイナリデータをファイルのように扱うためのクラス
                pil_calc_img.save(fp=buffer, format=pil_img.format)

                #======================================================
                # bufferのデータをファイルとして保存（レコードの更新も行われる）
                #======================================================
                if i == 0:
                    # 以前保存した画像処理後の画像ファイルを削除
                    self.result1.delete()
                    # imgと同じファイル名 & MEDIA_ROOTからの相対パスで 保存
                    self.result1.save(name=self.img.name, content=buffer)
                #
                if i == 1:
                    self.result2.delete()
                    self.result2.save(name=self.img.name, content=buffer)
                #
                if i == 2:
                    self.result3.delete()
                    self.result3.save(name=self.img.name, content=buffer)
                #
                if i == 3:
                    self.result4.delete()
                    self.result4.save(name=self.img.name, content=buffer)
                #
                if i == 4:
                    self.result5.delete()
                    self.result5.save(name=self.img.name, content=buffer)
                #
                if i == 5:
                    self.result6.delete()
                    self.result6.save(name=self.img.name, content=buffer)
                #
                if i == 6:
                    self.result7.delete()
                    self.result7.save(name=self.img.name, content=buffer)
                #
                if i == 7:
                    self.result8.delete()
                    self.result8.save(name=self.img.name, content=buffer)
               #
                if i == 8:
                    self.result9.delete()
                    self.result9.save(name=self.img.name, content=buffer)
                #
                if i == 9:
                    self.result10.delete()
                    self.result10.save(name=self.img.name, content=buffer)
                #
                if i == 10:
                    self.result11.delete()
                    self.result11.save(name=self.img.name, content=buffer)
                #
                if i == 11:
                    self.result12.delete()
                    self.result12.save(name=self.img.name, content=buffer)
                #
                if i == 12:
                    self.result13.delete()
                    self.result13.save(name=self.img.name, content=buffer)
                #
            #
    # ①〜③を実行するモデルの関数が終了

    def __str__(self):
        return self.img.url
#
