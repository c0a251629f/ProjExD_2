import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0 , -5),  # 上
    pg.K_DOWN: (0 , +5),  # 下
    pg.K_LEFT: (-5, 0),  # 左
    pg.K_RIGHT: (+5, 0),  # 右
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()  # リストを取得
    bb_img = bb_imgs[0]
    #bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurfaceを作る
    #pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の黒い部分を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得する
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾の初期横座標を設定する
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾の初期縦座標を設定する
    vx, vy = +5, +5  # 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾の衝突判定
            gameover(screen)
            return  # ゲームオーバーの意味でmain関数から出る

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]   
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        idx = min(tmr // 500, 9)  # 時間に応じてインデックスを取得
        avx = vx * bb_accs[idx]  # 加速度を反映
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]  # サイズの異なる画像を再設
        # Surfaceの大きさが変わったのでRectのサイズを更新
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)  # vx, vy ではなく avx, avy を渡す
        #bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向の判定
            vx *= -1
        if not tate:  # 縦方向の判定
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

def gameover(screen: pg.Surface) -> None:
    bg_img = pg.Surface((WIDTH, HEIGHT))
    bg_img.set_alpha(150)
    screen.blit(bg_img, [0, 0])

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    kk_img = pg.image.load("fig/8.png")
    kk_rct1 = kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    kk_rct2 = kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))

    screen.blit(txt, txt_rct)
    screen.blit(kk_img, kk_rct1)
    screen.blit(kk_img, kk_rct2)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
