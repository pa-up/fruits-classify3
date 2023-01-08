from PIL import Image
import numpy as np
import cv2

# バイナリ画像(DjangoのformからのUP画像)を PIL画像 に変換
def binar2pil(binary_img):
    pil_img = Image.open(binary_img)
    return pil_img
#


# PIL画像をOpenCV画像に変換
def pil2opencv(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)

    if cv_img.ndim == 2:  # モノクロ
        pass
    elif cv_img.shape[2] == 3:  # カラー
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    elif cv_img.shape[2] == 4:  # 透過
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
    return cv_img
#


# OpenCV画像をPIL画像に変換
def opencv2pil(cv_calc_img):
    pil_img = cv_calc_img.copy()
    
    if pil_img.ndim == 2:  # モノクロ
        pass
    elif pil_img.shape[2] == 3:  # カラー
        pil_img = cv2.cvtColor(pil_img, cv2.COLOR_BGR2RGB)
    elif pil_img.shape[2] == 4:  # 透過
        pil_img = cv2.cvtColor(pil_img, cv2.COLOR_BGRA2RGBA)
    pil_img = Image.fromarray(pil_img)
    return pil_img
#