"""
使用python撰寫一個簡單的射擊遊戲
不使用pygame.sprite.Sprite，練習物件導向以及事件導向的撰寫
"""
import pygame
from pathlib import Path
from player import Player
from missile import MyMissile
from enemy import Enemy
from explosion import Explosion
# Where your .py file is located
parent_path = Path(__file__).parents[1]     # 自己google查意思
# The resource folder path
image_path = parent_path / 'res'
icon_path = image_path / 'air.png'
icon_path2 = image_path / 'bg.png'
bgm = image_path / 'neko.mp3'

# 初始化pygame系統
pygame.init()
# 建立視窗物件，寬、高
screenHigh = 760
screenWidth = 1000
playground = (screenWidth, screenHigh)
screen = pygame.display.set_mode(playground)

pygame.mouse.set_visible(False)     # 視窗內不顯示滑鼠

pygame.display.set_caption("pygame_wen")     # 視窗標題
icon = pygame.image.load(icon_path)     # 載入圖示
pygame.display.set_icon(icon)
background = pygame.image.load(icon_path2)    # 更換視窗背景
background = background.convert()
#background = pygame.Surface(screen.get_size())      # Surface為圖片
#background = background.convert()       # 改變pixel format，加快顯示速度
#background.fill([0, 200, 250])       # 畫布為鐵黑色(三個參數為RGB)

pygame.mixer.music.load(bgm)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

fps = 120   # 更新頻率，包含畫面更新與事件更新 (每一秒更新120次)
movingScale = 600 / fps  # 把參數和fps作連動，大約 600 pixels / sec

# 把player.py這個物件放進來，playground為寬1000，高760
player = Player(playground=playground, sensitivity=movingScale)

# 建立物件串列
Missiles = []   # 建立一個list來放飛彈的事件
Enemies = []    # 建立一個list來放enemy的事件
Boom = []       # 建立一個list來放爆炸的事件

# 建立事件編號
launchMissile = pygame.USEREVENT + 1    # 自動發設飛彈
createEnemy = pygame.USEREVENT + 2      # 創建enemy的事件

# 建立敵機，每秒一台
pygame.time.set_timer(createEnemy, 500)

keyCountX = 0       # 用來計算按鍵被按下的次數，x軸一組
keyCountY = 0

# 初始化得分為0
Score = 0

running = True
clock = pygame.time.Clock()     # create an object to help track time

# 設定無窮迴圈，讓視窗持續更新與執行
while running:
    # 動態顯示得分
    score = str(Score)
    MyScore = pygame.font.SysFont("arial", 36)
    scoreImage = MyScore.render("My Score: " + score, True, [255, 255, 255], [255, 0, 0])

    # 從pygame事件佇列中，一項一項的檢查
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:     # 按 'Q' 離開視窗
                running = False
            if event.key == pygame.K_LEFT:     # 'a', 'A'
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_RIGHT:
                keyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_DOWN:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_UP:
                keyCountY += 1
                player.to_the_top()

            if event.key == pygame.K_SPACE:
                m_x = player.x + 20
                m_y = player.y
                # 發射第一發飛彈
                # 把MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale)放到append裡面
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                m_x = player.x + 80     # 計算貼圖位置，不是中心位置
                # 發射第二發飛彈
                Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))  # 若未指定參數，須按照宣告順序
                pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1

            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1

            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)  # 停止發射，安排的事件等於0代表清除

        if event.type == launchMissile:
            m_x = player.xy[0] + 20
            m_y = player.xy[1]
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.x + 80
            Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))
            pygame.time.set_timer(launchMissile, 400)  # 之後，每400 ms發射一組

        # createEnemy : 放enemy進來
        if event.type == createEnemy:
            Enemies.append(Enemy(playground=playground, sensitivity=movingScale))

        if player.available == False:
            print("You are died")
            running = False

        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))     # 更新背景圖片
    # ps. 程式碼的先後會影響圖層的上下位置
    # 寫在越前面的程式碼就會在越下面的圖層，寫在越後面的程式碼就會在越上面的圖層
    # 所以目前的圖層順序(下→上) : missile → enemy → player

    # player呼叫碰撞偵測的程式碼，檢查所有與enemy的碰撞
    # 如果有碰撞情形，available會變為false，遭到碰撞的enemy就會消失，剩餘enemy的available會變為true
    player.collision_detect(Enemies)

    # missile呼叫碰撞偵測的程式碼，檢查所有與enemy的碰撞
    for m in Missiles:
        m.collision_detect(Enemies)

    # 偵測enemy的屬性collided是否為true，為true的話加入爆炸效果
    for e in Enemies:
        if e.collided:
            Score += 1
            # 把enemy的中心點位置當成爆炸的參考點
            Boom.append(Explosion(e.center))

    # 重新建立一個Missiles
    Missiles = [item for item in Missiles if item.available]    # available:確定還有效的東西
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    # 把available為true的enemy更新到畫面上
    # 把[]裡的Enemies(舊的)重新定義一個新的list-Enemies，舊的東西會被gobject.py裡的def __del__(self)回收掉
    Enemies = [item for item in Enemies if item.available]
    for e in Enemies:
        e.update()
        screen.blit(e.image, e.xy)

    player.update()     # 更新player的狀態
    # 添加player圖片，player和image繼承到在gobject裡的image來使用，xy繼承到在gobject裡的xy來使用
    screen.blit(player.image, player.xy)

    # 爆炸效果在player之上
    Boom = [item for item in Boom if item.available]
    for e in Boom:
        e.update()
        screen.blit(e.image, e.xy)

    screen.blit(scoreImage, (4, 720))
    pygame.display.update()     # 更新螢幕狀態
    dt = clock.tick(fps)        # 每秒更新fps次 (可當時間延遲)

pygame.quit()   # 關閉繪圖視窗
