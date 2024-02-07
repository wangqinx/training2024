# A parody to classic mini game 特训99

# import essential libs
import pygame
from random import randint, uniform
from math import sin, cos, asin, acos, atan, radians, degrees, sqrt
import pdb

# controllable jet object
class char_sprite(pygame.sprite.Sprite): 
    def __init__(self, current_pos, pic):
        super().__init__()
        self.loadimg = pic
        self.image_shift = 0
        self.image_part = pygame.Rect(self.image_shift*20, 0, 20, 20)
        self.image = (self.loadimg).subsurface(self.image_part) # jet img display
        self.center = current_pos
        self.image.set_colorkey((0,0,0))  # Set black as the transparent color
        self.rect = self.image.get_rect(center = (self.center))  # Position the char
        self.radius = 8 # collide check radius
        self.speed = 3
        self.xfactor = 1
        self.yfactor = 1
    def update(self, direction_type, screen):
        if direction_type == 1: # update the jet's moving direction and img display
            self.xfactor = -1
            self.yfactor = 1
            self.image_shift = 1
        if direction_type == 2:
            self.xfactor = 0
            self.yfactor = 1
            self.image_shift = 0
        if direction_type == 3:
            self.xfactor = 1
            self.yfactor = 1
            self.image_shift = 2
        if direction_type == 4:
            self.xfactor = -1
            self.yfactor = 0
            self.image_shift = 1
        if direction_type == 5:
            self.xfactor = 0
            self.yfactor = 0
            self.image_shift = 0
        if direction_type == 6:
            self.xfactor = 1
            self.yfactor = 0
            self.image_shift = 2
        if direction_type == 7:
            self.xfactor = -1
            self.yfactor = -1
            self.image_shift = 1
        if direction_type == 8:
            self.xfactor = 0
            self.yfactor = -1
            self.image_shift = 0
        if direction_type == 9:
            self.xfactor = 1
            self.yfactor = -1
            self.image_shift = 2
        self.image_part = pygame.Rect(self.image_shift*20, 10, 20, 20)
        self.image = (self.loadimg).subsurface(self.image_part)
        self.image.set_colorkey((0,0,0))
        self.rect.x += self.xfactor*self.speed
        self.rect.y += self.yfactor*self.speed
        if self.rect.x < 0: # restrict jet inside window
            self.rect.x = 0
        if self.rect.x > 780:
            self.rect.x = 780
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 580:
            self.rect.y = 580
        return self.rect.x, self.rect.y # return the coordinates

# fantastic check sprite
class fanta_sprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect(center = position)
        self.radius = 15

# bullet generator
class massbullet(pygame.sprite.Sprite): 
    def __init__(self, current_pos, pic, bullet_type):
        super().__init__()
        self.loadimg = pic
        self.gen = randint(0,359) # bullet generate with following 3 lines
        self.center = 400+600*cos(radians(self.gen)), 300-600*sin(radians(self.gen))
        self.centerx = 400+600*cos(radians(self.gen))
        self.centery = 300-600*sin(radians(self.gen))
        self.radius = 5
        self.homingfactor = 1
        while True: # select bullet bahavior with certain types, fake loop
            if bullet_type == 1:
                self.speedfactor = uniform(1.5, 2)
                self.homing = 0
                self.color = 'red'
                self.image_shift = 1
                break
            if bullet_type == 2:
                self.speedfactor = 1
                self.homing = 0.7
                self.color = 'green'
                self.image_shift = 2
                break
            if bullet_type == 3:
                self.speedfactor = 2
                self.homing = 2
                self.color = 'blue'
                self.image_shift = 3
                break
            if bullet_type == 0:
                self.speedfactor = 1
                self.homing = 0
                self.color = 'yellow'
                self.image_shift = 0
                break
        self.speed = 3.5 * self.speedfactor
        self.counter = 0 # kill check
        self.image_part = pygame.Rect(self.image_shift*10, 0, 10, 10)
        self.image = (self.loadimg).subsurface(self.image_part)
        self.image.set_colorkey((0,0,0))  # Set black as the transparent color
        self.rect = self.image.get_rect(center = (self.center))  # Position the bullet
        if self.centery < current_pos[1]: # determine the shooting angle
            self.angle = degrees(atan((current_pos[0]-self.centerx)/(self.centery-current_pos[1]))) + randint(-15,15)
            self.speedx = -sin(radians(self.angle))*self.speed
            self.speedy = cos(radians(self.angle))*self.speed
        if self.centery >= current_pos[1]:
            self.angle = degrees(atan((current_pos[0]-self.centerx)/(current_pos[1]-self.centery))) + randint(-15,15) 
            self.speedx = -sin(radians(self.angle))*self.speed
            self.speedy = -cos(radians(self.angle))*self.speed
    def update(self, current_pos):
        if self.homing : # homing corrections
            saita = acos(abs((self.rect.x-current_pos[0])/sqrt((self.rect.y-current_pos[1])**2 + (self.rect.x-current_pos[0])**2)))
            if self.rect.x >= current_pos[0]:
                self.speedx -= 0.1*cos(saita) * self.homing
            if self.rect.x < current_pos[0]:
                self.speedx += 0.1*cos(saita) * self.homing
            if self.rect.y >= current_pos[1]:
                self.speedy -= 0.1*sin(saita) * self.homing
            if self.rect.y < current_pos[1]:
                self.speedy += 0.1*sin(saita) * self.homing
            hypotenuse = sqrt(self.speedx**2 + self.speedy**2)
            self.speedx = 3.5 * self.speedfactor * self.speedx / hypotenuse
            self.speedy = 3.5 * self.speedfactor * self.speedy / hypotenuse
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.counter +=1
        if self.counter>120:
            if self.rect.x <-50 or self.rect.x >850 or self.rect.y <-50 or self.rect.y >650:
                self.kill()

# background stars
class shooting_stars(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((2,2))
        self.y = y
        self.rect = self.image.get_rect(center = (randint(0,800),self.y))
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.image.fill(self.color)
        self.speed = uniform(.5,2)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 605:
            self.kill()


# game initials
pygame.init()    # general initial, pygame function
screen = pygame.display.set_mode([800, 600], pygame.RESIZABLE)    # game display window
clock = pygame.time.Clock()
running = True
dt = 1
game_status = 4 # status 4 is game initials
frame_count = 0 # count +1 per in-game flip
frames_per_second = 60 # FPS
game_pause_doubleclick = 10 # double click watcher
back_shootings = pygame.sprite.Group() # background stars
bullets = pygame.sprite.Group() # group for bullets
main_char = pygame.sprite.Group()
sprite_all = pygame.sprite.Group()
font = pygame.font.SysFont('幼圆', 24)
font2 = pygame.font.SysFont('幼圆', 100, bold=True)
event_text = ['高速弹','制导弹','高速制导弹']
summary_text1 = ['嗯？', '清洁工', '派遣工', '科员', '副主任科员', '科长', '处长', '局长', '市长', '厅长', '省长', '部长', '你真厉害！']
summary_text2 = ['发生甚么事了？', '有工作这件事没有看上去那么容易', '"小伙子好好干"', '"坚持下去总有机会的"', '恭喜高升！', '你管着6个人呢', '职工和干部的分界线', '你手下人多得数不清', '风光无限', '怎么爬上来的？', '安全生产', '真正的闲职', '鼓掌！']
summary_text3 = ['', '喂，右边倒数第二个蹲坑里有翔', '工资高于某些编内人员呢', '你头发是不是少了？', '这里是你职业生涯的顶峰和尽头', '没人知道他们的后台都是谁', '使唤不了任何人', '上级更多', '谁都不敢得罪', '目标是安全退休', '夜不能寐', '没人叫得出你的名字', '（此子不可留也']
jet = pygame.image.load('jet.bmp')
jet.set_colorkey((0,0,0))
screen.fill("black")
# pdb.set_trace()

while running:
    event_type = pygame.event.get()
    keys = pygame.key.get_pressed()
    if game_status == 4: # replay initials
        screen.fill("black")
        i = 0
        bullet_type = 0
        bullet_gen_frame = 300
        bullet_trigger = 25
        bullet_trig_count = 0
        back_stars = 60
        while back_stars:
            back_shootings.add(shooting_stars(randint(0,600)))
            back_stars -= 1
        char_direction = 5
        explode_display = 0
        explode_shift = 0
        explode_display = 0
        fanta_count = 0
        fanta_display = 0
        fanta_excla = 0
        fanta_mark = 0
        fanta_sum = 0
        fanta_cumu = 0
        game_pause = 0
        game_pause_doubleclick = 0
        game_status = 0
        game_time = 0
        player_pos = [screen.get_width()/2, screen.get_height()-150]
        player_char = char_sprite(player_pos, jet)
        special_display = 0
        special_event = 0
        sprite_all.add(player_char)
        screen.blit(font2.render('特 训', True, 'white'), (275, 200)) 
        screen.blit(font.render('按下ENTER特训开始', True, 'white'), (300, 500)) 

    # pdb.set_trace()
    # title screen
    if game_status == 0: 
        # pdb.set_trace()
        for i in event_type:
            if i.type == pygame.QUIT:
                running = False
                break
        if  keys[pygame.K_ESCAPE]:
            game_status = 0
            running = False
            break
        if keys[pygame.K_RETURN] and game_pause_doubleclick >= 10:
            game_status = 1
            frame_count = 0
            game_pause_doubleclick = 0

    # game running
    if game_status == 1: 
        # pdb.set_trace()
        while game_status == 1:
            # fill the screen with a color or pic that wipes away anything from last frame
            # keys = pygame.key.get_pressed()
            for i in event_type:
                if i.type == pygame.QUIT:
                    running = False
                    break
            while True:
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    char_direction = 8
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        char_direction = 9
                        break
                    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        char_direction = 7
                        break
                    break
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    char_direction = 2
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        char_direction = 3
                        break
                    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        char_direction = 1
                        break
                    break
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    char_direction = 4
                    break
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    char_direction = 6
                    break
                if keys[pygame.K_ESCAPE]:
                    game_status = 0
                    running = False
                    break
                if keys[pygame.K_RETURN] and game_pause_doubleclick >= 10:
                    if game_pause == 0:
                        game_pause = 1
                        game_pause_doubleclick = 0
                    else:
                        game_pause = 0
                        game_pause_doubleclick = 0
                char_direction = 5
                break

            if bullet_gen_frame >= 150 and game_pause == 0:
                special_event = randint(0,19)
                while True:
                    if special_event == 3: # speed
                        bullet_type = 1
                        special_display = 120
                        bullet_special = 10
                        break
                    elif special_event == 4: # homing
                        bullet_type = 2
                        special_display = 120
                        bullet_special = 5
                        break
                    elif special_event == 5: # speed and homing
                        bullet_type = 3
                        special_display = 120
                        bullet_special = 2
                        break
                    else:
                        bullet_type = 0
                        bullet_special = 0
                        break
                while (bullet_trigger - bullet_special):  # normal
                    bullets.add(massbullet(player_pos, jet, 0))
                    bullet_trigger -= 1
                while bullet_special:  # normal
                    bullets.add(massbullet(player_pos, jet, bullet_type))
                    bullet_special -= 1
                bullet_gen_frame = 0
                bullet_trig_count += 1
                bullet_trigger = 25 + (bullet_trig_count//5)
                # bullet_type = 0
                if bullet_trigger > 150:
                    bullet_trigger = 150

            # refresh background to make you feel moving forward
            if len(back_shootings)<60:
                back_shootings.add(shooting_stars(0))

            # fantastic
            fanta_spr = fanta_sprite(player_pos)
            if pygame.sprite.spritecollide(fanta_spr, bullets, False, collided=pygame.sprite.collide_circle) and game_pause == 0:
                fanta_count += 1
                fanta_sum += 1
            if not pygame.sprite.spritecollide(fanta_spr, bullets, False, collided=pygame.sprite.collide_circle) and game_pause == 0:
                fanta_count = 0
            if fanta_count > 12 and game_pause == 0:
                fanta_display += 1
            if fanta_mark < fanta_display and game_pause == 0:
                fanta_mark = fanta_display
                fanta_excla = fanta_mark // 6
            # if fanta_display and game_pause == 0:
            #     text_surface = font.render('绝妙！', True, 'white')
            #     screen.blit(text_surface, (50, 10)) 
            #     while fanta_excla:
            #         text_excla = font.render('！', True, 'white')
            #         screen.blit(text_excla, (81+5*fanta_excla, 10))
            #         fanta_excla -= 1
            #     fanta_count -= 1
            #     if fanta_count < 0:
            #         fanta_count = 0
            if not fanta_count and game_pause == 0:
                fanta_display -= 1
                if fanta_display < 0:
                    fanta_display = 0
            if not fanta_display and game_pause == 0:
                fanta_mark = 0
                fanta_excla = 0
            fanta_spr.kill()

            # collide monitor
            if pygame.sprite.spritecollide(player_char, bullets, True, collided=pygame.sprite.collide_circle) and game_pause == 0:
                explode_display = 20
                player_char.kill()

            if explode_display < 0:
                game_status = 2

            if game_pause == 0: # none pause actions: variables update and objects blit
                screen.fill("black")
                back_shootings.update()
                back_shootings.draw(screen)
                player_pos = player_char.update(char_direction, screen)
                back_shootings.update()
                sprite_all.draw(screen)
                bullets.update(player_pos)
                bullets.draw(screen)
                frame_count += 1
                bullet_gen_frame += 1
                game_time += clock.get_time()/1000
                if fanta_display:
                    text_surface = font.render('绝妙！', True, 'white')
                    screen.blit(text_surface, (50, 10)) 
                    while fanta_excla:
                        text_excla = font.render('！', True, 'white')
                        screen.blit(text_excla, (81+5*fanta_excla, 10))
                        fanta_excla -= 1
                    fanta_count -= 1
                    if fanta_count < 0:
                        fanta_count = 0
                if explode_display: # end game animation
                    if explode_display == 1:
                        explode_display -= 2
                    else:
                        explode_display -= 1
                    explode_shift = (explode_display//4) - 1
                    explode_rect = pygame.Rect(explode_shift*30, 30, 30, 30)
                    screen.blit(jet, player_pos, explode_rect)
                if explode_display < 0: # print on summary page
                    screen.blit(font2.render('中 弹', True, 'white'), (275, 100)) 
                    screen.blit(font.render('生存时长 {:.2f} 秒'.format(game_time), True, 'white'), (300, 300)) 
                    screen.blit(font.render('弹幕数量 {:.0f} '.format(int(50+bullet_trig_count//2.5)), True, 'white'), (325, 400)) 
                    screen.blit(font.render('绝妙度 {:.0f} %'.format(fanta_sum//15), True, 'white'), (335, 500)) 


            if special_display and game_pause == 0:
                text_event = font.render(event_text[bullet_type-1], True, 'white')
                screen.blit(text_event, (650, 10))
                special_display -= 1


            break

    # summary page
    if game_status == 2: 
        # text_summary = font.render(summary_text1[0], True, 'white')
        # screen.blit(text_summary, (650, 10))
        while True:
            for i in event_type:
                if i.type == pygame.QUIT:
                    running = False
                    break
            if keys[pygame.K_ESCAPE]:
                game_status = 0
                running = False
                break
            if keys[pygame.K_RETURN] and game_pause_doubleclick >= 10: # print on ratings page
                screen.fill("black")
                game_status = 3
                game_pause_doubleclick = 0
                ratings = 0
                if game_time<2.5:
                    ratings = 0
                elif game_time<5:
                    ratings = 1
                elif game_time<10:
                    ratings = 2
                else :
                    ratings = int(game_time//10) + 2
                screen.blit(font2.render(summary_text1[ratings], True, 'white'), (400-len(str(summary_text1[ratings]))*50, 200)) 
                screen.blit(font.render(summary_text2[ratings], True, 'white'), (20, 20)) 
                screen.blit(font.render(summary_text3[ratings], True, 'white'), (750-len(str(summary_text3[ratings]))*25, 550)) 
            break

    # ratings page
    if game_status == 3: 
        while True:
            for i in event_type:
                if i.type == pygame.QUIT:
                    running = False
                    break
            if keys[pygame.K_ESCAPE]:
                game_status = 0
                running = False
                break
            if keys[pygame.K_RETURN] and game_pause_doubleclick >= 10:
                game_status = 4
                game_pause_doubleclick = 0
                bullets.empty()
                screen.fill("black")
            break

    # apply all updates
    pygame.display.flip()

    # limits FPS to 60, dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(frames_per_second) / 1000
    game_pause_doubleclick += 1

pygame.quit()   # pygame.QUIT event means the user clicked X to close your window



