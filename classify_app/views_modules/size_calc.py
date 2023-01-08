import cv2
import numpy as np


#==============================================
# 縦横の倍率を保ちながら、画像の辺の長さの最大値を定義
#==============================================
def max_size(cv_img):
    max_img_size = 1500  # 画像の縦または横サイズの最大値を1500に制限

    rows = cv_img.shape[0]
    cols = cv_img.shape[1]
    
    new_row = rows
    new_col = cols
    
    if (rows >= cols)  and (rows > max_img_size) :
        new_row = max_img_size
        new_col = int( cols / (rows/max_img_size) )
    #
    if (cols > rows)  and (cols > max_img_size) :
        new_col = max_img_size
        new_row = int( rows / (cols/max_img_size) )
    #
    
    cv_img = cv2.resize( cv_img , dsize=(new_col, new_row) )
    
    return cv_img
#
