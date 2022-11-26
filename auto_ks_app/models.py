from django.db import models
from PIL import Image
import io
from auto_ks_app.views_modules import pil2cv
from auto_ks_app.views_modules import cv2_calc


# マスク画像の数 ＝ min閾値の数 = resultの数
mask_df = 20  # min閾値どうしの差
mask_number = int(250 / mask_df) + 1  # マスク画像の数(min閾値の数)


class UploadImgModel(models.Model):
    img = models.ImageField(upload_to='documents/')
    success_number = models.IntegerField(default=0)


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

        # 補正成功画像のリストを戻り値（Herokuデプロイの際には、DBから画像を取り出すことはできない）
        return cv_calc_img
    #

    def __str__(self):
        return self.img.url
#
