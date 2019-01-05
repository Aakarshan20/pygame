import pygame
import sys
import traceback
import math
from pygame.locals import *
from random import * #引入隨機模塊


class Ball(pygame.sprite.Sprite):
    def __init__(self, white_ball_image, red_ball_image, position, speed, bg_size, target):#bg_size為背景尺寸
        pygame.sprite.Sprite.__init__(self)

        self.white_ball_image = pygame.image.load(white_ball_image).convert_alpha()#白球
        self.red_ball_image = pygame.image.load(red_ball_image).convert_alpha()#紅球
        
        self.rect = self.white_ball_image.get_rect()
        self.rect.left, self.rect.top = position
        self.side = [choice([-1,1]), choice([-1,1])]#choice(list) : 隨機從list中取出一個值
        self.speed = speed
        self.collide = False#預設無碰撞
        #self.control = True#預設為無法控制 隨機移動
        self.control = False#預設為無法控制 隨機移動
        self.target = target
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius =  self.rect.width/2
        self.in_hole = False
        self.sound_played = False

    def move(self):#讓球移動
        #如果是玩家控制的話
        
        
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:            
            #方向乘以速度
            self.rect = self.rect.move((self.side[0]* self.speed[0], \
                                        self.side[1]*self.speed[1]))
        
        if self.rect.left > 30 and self.rect.left < 45 and self.rect.top >30 and self.rect.top < 45 :#左上洞
                self.rect.left = 14
                self.rect.top = 12
                self.in_hole = 1
        if (self.rect.left > 208 and self.rect.left < 232) and (self.rect.top >30 and self.rect.top < 42):#中上洞
                self.rect.left = 212
                self.rect.top = 14
                self.in_hole = 2

        if self.rect.left > 385 and self.rect.top < 40:#右上洞
                self.rect.left = 408
                self.rect.top = 12
                self.in_hole = 3

        if self.rect.left <45  and self.rect.top > 190:#左下洞
                self.rect.left = 14
                self.rect.top = 215
                self.in_hole = 4

        if (self.rect.left > 208 and self.rect.left < 232) and (self.rect.top >190):#中下洞
                self.rect.left = 211
                self.rect.top = 215
                self.in_hole = 5

        if self.rect.left > 385 and self.rect.top > 190:#右上洞
                self.rect.left = 408
                self.rect.top = 215
                self.in_hole = 6

        
        if self.in_hole == False:
            if self.rect.left <= 28:
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]
                self.rect.left = 28
            elif self.rect.right >= self.width-28:
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]
                self.rect.right = self.width-28
            elif self.rect.bottom >= self.height-28:
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]
                self.rect.bottom = self.height-28
            elif self.rect.top <= 28:
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]
                self.rect.top = 28
        elif self.in_hole ==1:
            self.rect.left = 14
            self.rect.top = 14
        elif self.in_hole ==2:
            self.rect.left = 212
            self.rect.top = 14
        elif self.in_hole ==3:
            self.rect.left = 408
            self.rect.top = 14
        elif self.in_hole ==4:
            self.rect.left = 14
            self.rect.top = 215
        elif self.in_hole ==5:
            self.rect.left = 211
            self.rect.top = 214
        elif self.in_hole ==6:
            self.rect.left = 408
            self.rect.top = 215

    def check(self, motion):#將motion參數與自身target比較
        if self.target < motion < self.target +10:#誤差範圍+5
            return True
        else:
            return False
        
            
class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image,mouse_image, bg_size):#bg_size為背景尺寸
    #def __init__(self, glass_image, bg_size):#bg_size為背景尺寸
        #初始化動畫精靈
        pygame.sprite.Sprite.__init__(self)

        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
                              (bg_size[0]-self.glass_rect.width)//2,\
                              (bg_size[1]-self.glass_rect.height)//2

        #畫鼠標
        
        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = self.glass_rect.top, \
                                                    self.glass_rect.left

        pygame.mouse.set_visible(False)#預設不可見
        

def main():
    pygame.init()
    white_ball_image = "images/whiteBall_12x12_2.png"
    red_ball_image = "images/redBall_12x12_2.png"
    bg_image = "images/table.png"
    mouse_image = "images/hand3.png"
    glass_image = "images/glass2.png"

    running = True

    #添加背景音樂
    pygame.mixer.music.load('sounds/bgm.ogg')
    bgm_volume = 0.01
    pygame.mixer.music.set_volume(bgm_volume)#音量0.01
    pygame.mixer.music.play()

    #添加音效''''''20190103
    sound_volume = 0.01
    hole_sound = pygame.mixer.Sound('sounds/sword.ogg')#進洞音效
    hole_sound.set_volume(sound_volume)
    
    loser_sound = pygame.mixer.Sound('sounds/whistling.ogg')#失敗音效
    loser_sound.set_volume(sound_volume)
    
    winner_sound = pygame.mixer.Sound('sounds/clapping_bravo.ogg')#成功音效(1)
    banzai_sound = pygame.mixer.Sound('sounds/banzai.ogg')#成功音效(2)
    winner_sound.set_volume(sound_volume)
    banzai_sound.set_volume(sound_volume)
    
    #音樂播放完時遊戲結束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)
    


    bg_size = width, height = 435, 235
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("play Billiard")

    #載入背景
    background = pygame.image.load(bg_image).convert_alpha()
    
    #存放所有球的列表
    balls = []
    group = pygame.sprite.Group()

    #此處創建一堆球
    BALL_NUM =10
    
    
    for i in range(BALL_NUM):
        #12: 球的直徑, 22:桌子的邊框寬度
        position = randint(34, width-12-22), randint(34, height-12-22)

        #隨機給一個速度(向量)
        speed = [randint(1,10), randint(1,10)]

        ball = Ball(white_ball_image, red_ball_image, position, speed, bg_size, 2*(i+1))#最後的參數是該球的觸發條件(每秒左右次數)
        #生成時 使用自帶的碰撞檢測方法檢測
        while pygame.sprite.spritecollide(ball, group,False, pygame.sprite.collide_circle):
            #如果發生碰撞 則重新給定初速度
            ball.rect.left, ball.rect.top = randint(34, width-12-22), randint(34, height-12-22)
        
        #加入列表
        balls.append(ball)
        group.add(ball)

    #glass = Glass(glass_image, mouse_image, bg_size)
    glass = Glass(glass_image,mouse_image, bg_size)

    #記錄每秒鐘鼠標移動的次數
    motion = 0

    #添加自定義事件監聽小球與motion的狀態
    MYTIMER = USEREVENT+1 #設為下一個自定義事件

    pygame.time.set_timer(MYTIMER, 1000)#1秒


    pygame.key.set_repeat(100,100)#延遲100毫秒 每100毫秒取得該事件

    clock = pygame.time.Clock()

    holes = []#各種洞
    messages = []#各種訊息
    
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type ==GAMEOVER:
                loser_sound.play()
                msg = pygame.image.load('images/fail.png').convert_alpha()
                msg_pos = (width-msg.get_width())//2, (height-msg.get_height())//2

                messages.append((msg, msg_pos))#用元組的型式加進去
                running = False
            elif event.type == MYTIMER:
                #一但motion計數不為空
                if motion:
                    #取出每個小球
                    for each in group:
                        if each.check(motion):#使用該球的方法
                            each.speed = [0,0]
                            each.control = True
                    motion = 0#motion歸零

            elif event.type == MOUSEMOTION:#捕獲所有鼠標事件
                motion +=1

            elif event.type == KEYDOWN:
                #調整背景音量
                if event.key == K_KP_MINUS:
                    if sound_volume > 0:
                        sound_volume -=0.01
                        winner_sound.set_volume(sound_volume)
                        banzai_sound.set_volume(sound_volume)
                        loser_sound.set_volume(sound_volume)
                        hole_sound.set_volume(sound_volume)
                    if bgm_volume >0:
                        bgm_volume -=0.01
                        pygame.mixer.music.set_volume(bgm_volume)#設置bgm

                if event.key == K_KP_PLUS:
                    if sound_volume < 0.2:
                        sound_volume +=0.01
                        winner_sound.set_volume(sound_volume)
                        banzai_sound.set_volume(sound_volume)
                        loser_sound.set_volume(sound_volume)
                        hole_sound.set_volume(sound_volume)
                    if bgm_volume < 0.2:
                        bgm_volume +=0.01
                        pygame.mixer.music.set_volume(bgm_volume)#設置bgm
                        
                if event.key == K_w:
                    for each in group:#遍歷出可控的小球
                        if each.control:#等效於 if each.control == Ttue
                            each.speed[1] -=1#向上移動
                if event.key == K_s:
                    for each in group:#遍歷出可控的小球
                        if each.control:#等效於 if each.control == Ttue
                            each.speed[1] +=1#向下移動
                if event.key == K_a:
                    for each in group:#遍歷出可控的小球
                        if each.control:#等效於 if each.control == Ttue
                            each.speed[0] -=1#向左移動

                if event.key == K_d:
                    for each in group:#遍歷出可控的小球
                        if each.control:#等效於 if each.control == Ttue
                            each.speed[0] +=1#向右移動
                            
        screen.blit(background, (0,0))#繪製背景
        #screen.blit(glass.glass_image, mouse_image, glass.glass_rect)#繪製玻璃板
        

        
        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()#畫鼠標
        #限制客製化鼠標圖像只在玻璃面板內可見
        
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
            
        if glass.mouse_rect.right > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
            
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
            
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height

        screen.blit(glass.mouse_image, glass.mouse_rect)
        
        for each in balls:
            each.move()#修改座標讓他移動
            if each.collide:
                each.speed = [randint(1,10), randint(1,10)]
                each.collide = False
                
            if each.control or each.in_hole:
                #畫一個紅色的球
                screen.blit(each.red_ball_image, each.rect)
            else:
                screen.blit(each.white_ball_image, each.rect)

        
        
        for each in group:
            group.remove(each)#把要檢測的球拿出來
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                #如果發生碰撞 則重新給定初速度
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    #下面兩行反正就是反向移動
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False#和別的球碰撞時 失去控制

            if each.in_hole is not False and each.sound_played is False:#如果小球進洞
                hole_sound.play()
                each.sound_played = True

                if each.in_hole not in holes:
                    holes.append(each.in_hole)
                if len(holes) == 6:#六洞全滿 遊戲結束
                    pygame.mixer.music.stop()
                    winner_sound.play()
                    pygame.time.delay(3000)
                    banzai_sound.play()
                    msg = pygame.image.load('images/message.png').convert_alpha()
                    msg_pos = (width-msg.get_width())//2, \
                              (height-msg.get_height())//2

                    messages.append((msg, msg_pos))#用元組的型式加進去
                    pygame.time.delay(7000)
                    loser_sound.play()
                    
            
            #加回去
            group.add(each)


        for message in messages:
            screen.blit(message[0], message[1])
        if len(messages) == 0:
            screen.blit(glass.glass_image, glass.glass_rect)#繪製玻璃板
        pygame.display.flip()
        clock.tick(30)
            
        
    
if __name__ =="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()














    
