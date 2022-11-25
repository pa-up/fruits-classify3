import cv2
import numpy as np


#==================================
# グレースケール化
#==================================
def gray(cv_img):
    cv_calc_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    return cv_calc_img
#




#==========================================
# 台形領域を自動検出し、台形補正
#==========================================
def auto_keystone(cv_img, mask_df, mask_number):

    row = cv_img.shape[0]  # 入力画像の行数（縦サイズ）
    col = cv_img.shape[1]   # 入力画像の列数（横サイズ）

    #----------------------------------------
    #グレースケール化
    #----------------------------------------
    img_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    #----------------------------------------
    # マスク画像のmin閾値ループに必要な変数と準備
    #----------------------------------------
    img_mask = np.empty((mask_number),  dtype='object')
    mask_count = 0   #「点の数が4つの近似輪郭」を含む マスク画像の数
    edge_4_mask = []    # 各マスク画像の「点の数が4つの近似輪郭」で「面積最大」


    # min閾値ごとに条件分岐   ()() マスク画像で頂点4つ画像が得られなかったら、入力画像を入れる
    for m in range( 0, mask_number ):

        #----------------------------------------
        # 2値化処理で マスク画像生成
        #----------------------------------------
        # 2値化のmin閾値
        mask_min  =  10  +  m * mask_df   # 例. 1回：10 , 2回：30 , ... , 13回：250

        # 2値化処理の実行
        ret, img_mask = cv2.threshold(img_gray, mask_min, 255, cv2.THRESH_BINARY)

        #----------------------------------------
        # 輪郭の検出 （contours： 輪郭の頂点の座標）
        #----------------------------------------
        contours, hierarchy = cv2.findContours(img_mask.astype("uint8"), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


        #----------------------------------------
        # 大きいor小さい輪郭を誤検出として、削除
        #----------------------------------------
        # 小さすぎる輪郭（ノイズなど）を削除 → 利用者に指示「台形領域 が入力画像の半分以上」
        contours = list(filter(lambda x: cv2.contourArea(x) > (40*40/100/100 * row * col), contours))
        # 大きすぎる輪郭（周辺減光や枠線など）を削除
        contours = list(filter(lambda x: cv2.contourArea(x) < (99*99/100/100 * row * col), contours))


        #----------------------------------------
        # 大きいor小さい輪郭を誤検出として、削除
        #----------------------------------------
        # 頂点の数を減らす
        edge_easy = np.empty( (len(contours)) ,  dtype = 'object' )  # 近似輪郭の配列
        edge_4_easy = []

        count = 0   # 頂点数が4の輪郭をカウント （0個の場合は、補正処理を禁止＆エラー文言を表示）
        for k in range(0, len(contours), 1):
            # 点の数を減らして輪郭を近似
            edge_long = cv2.arcLength(contours[k], True)
            ratio = 0.02
            edge_easy[k] = cv2.approxPolyDP(contours[k], epsilon=ratio * edge_long, closed=True)

            # 点の数が4つの輪郭の配列のみを保存
            if (len(edge_easy[k]) == 4):
                edge_4_easy.append(edge_easy[k])
                count = count + 1
            #
        # 1つのマスク画像内で、最大の「点の数4つ輪郭」を リスト edge_4_mask に格納
        ## （画像内でおかしな箇所を四角形と認識させないため）
        if count >= 1:
            edge_4_mask.append(max(edge_4_easy, key=lambda x: cv2.contourArea(x)))
            mask_count = mask_count + 1
        #

        # 頂点4つ画像がなかった場合 → 入力画像を入力 （本当はこんなことせずに失敗にしたい）
        # これにより、13種類のマスク画像すべてで、補正画像を出力できるようにしてる（modelのresult1~13全てを出力）
        #if count == 0:
            #edge_4_mask.append(cv_img)#### ここに間違いあるのでは？？？
            #mask_count = mask_count + 1
        #


        # 再利用する変数を初期化
        del mask_min
        del img_mask
        del contours
        del hierarchy
        del edge_easy
        del edge_4_easy
    # 1つのマスク画像におけるループ終了



    #--------------------------------------------------
    # 全てのマスク画像の中に四角形が存在しない場合を「失敗」
    #--------------------------------------------------
    if mask_count == 0:
        success = 0
        square_image = []
        return square_image, success
    #



    #--------------------------------------------------
    # 全てのマスク画像の中で四角形が存在する場合は台形補正実行
    #--------------------------------------------------
    # 台形補正後の画像データ （マスク画像毎に、補正後の画像を格納）
    square_image = []

    # 補正開始
    if mask_count >= 1:    # 便宜上これまでで、mask_count が1になるようにしている（→ len(edge_4_maskがマスク画像の数にしてる）
        for p in range( 0 , len(edge_4_mask) ):
            # 台形の頂点座標配列の次元を美化 (edge_4_easy_max の次元は(4, 1, 2))
            edge_4_mask_p = edge_4_mask[p]
            edge_square = np.squeeze(edge_4_mask[p])

            #----------------------------------------
            # 歪んだ台形の4つの頂点の座標を命名
            #----------------------------------------
            # 座標①　座標④
            # 座標②  座標③
            #----------------------------------------
            # x座標が1番小さいの座標とその番号を取得
            x_min = edge_square[0][0]
            x_min_number = 0

            for k in range(1, 4, 1):
                if (edge_square[k][0] <= x_min):
                    x_min = edge_square[k][0]
                    x_min_number = k
                #
            #

            # x座標が2番目に小さいの座標とその番号を取得
            x_pre_min = 10000000
            for k in range(0, 4, 1):
                if (k != x_min_number):
                    if (edge_square[k][0] <= x_pre_min):
                        x_pre_min = edge_square[k][0]
                        x_pre_min_number = k
            #

            #　座標①と座標②を決定
            if ( edge_square[x_min_number][1]    >=    edge_square[x_pre_min_number][1]):
                vertex_order1_x = edge_square[x_pre_min_number][0]
                vertex_order1_y = edge_square[x_pre_min_number][1]
                vertex_order2_x = edge_square[x_min_number][0]
                vertex_order2_y = edge_square[x_min_number][1]
            #
            if ( edge_square[x_min_number][1]    <=    edge_square[x_pre_min_number][1]):
                vertex_order1_x = edge_square[x_min_number][0]
                vertex_order1_y = edge_square[x_min_number][1]
                vertex_order2_x = edge_square[x_pre_min_number][0]
                vertex_order2_y = edge_square[x_pre_min_number][1]
            #

            # 座標③と座標④の候補を取得
            x_number3 = -1
            for k in range(0, 4, 1):
                if (   (k != x_min_number)   and   (k != x_pre_min_number)   and    (x_number3 == -1)   ):
                    x_number3 = k
                #
                if (   (k != x_min_number)   and   (k != x_pre_min_number)   and    (x_number3 != -1)   ):
                    x_number4 = k
                #
            #

            #　座標③と座標④を決定
            if (edge_square[x_number3][1] >= edge_square[x_number4][1]):
                vertex_order3_x = edge_square[x_number3][0]
                vertex_order3_y = edge_square[x_number3][1]
                vertex_order4_x = edge_square[x_number4][0]
                vertex_order4_y = edge_square[x_number4][1]
            #
            if ( edge_square[x_number3][1]    <=    edge_square[x_number4][1]):
                vertex_order3_x = edge_square[x_number4][0]
                vertex_order3_y = edge_square[x_number4][1]
                vertex_order4_x = edge_square[x_number3][0]
                vertex_order4_y = edge_square[x_number3][1]
            #

            #----------------------------------------
            # 補正後の長方形の4つの頂点座標を算出
            #----------------------------------------
            width = vertex_order4_x - vertex_order1_x
            height = vertex_order2_y - vertex_order1_y


            #----------------------------------------
            # アフィン変換
            #----------------------------------------
            # 変換に利用する座標
            keystone_dots = np.array([ [vertex_order1_x , vertex_order1_y] , [vertex_order2_x, vertex_order2_y], [vertex_order3_x, vertex_order3_y], [vertex_order4_x, vertex_order4_y] ], dtype=np.float32)
            square_dots = np.array([[vertex_order1_x , vertex_order1_y], [vertex_order1_x, vertex_order1_y + height], [vertex_order1_x + width , vertex_order1_y + height], [vertex_order1_x + width , vertex_order1_y]], dtype=np.float32)

            # 変換行列
            trans_array = cv2.getPerspectiveTransform(keystone_dots, square_dots)
            
            # 射影変換
            square_image.append( cv2.warpPerspective(cv_img, trans_array, (col, row)) )
        #

        success = mask_count
        return square_image, success
    #
#
