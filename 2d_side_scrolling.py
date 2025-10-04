import pygame

def draw_hitbox(rect, surface, color=(255, 0, 0)):
    pygame.draw.rect(surface, color, rect, 2)  # ขอบหนา 2 px

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    def draw(self, surface):
        pygame.draw.rect(surface, (100, 200, 100), self.rect)  # Draw as a green rectangle
 
        draw_hitbox(self.rect, surface, color=(0, 0, 255))  # วาด hitbox สีฟ้า

class Player:
    def __init__(self, pos, scale=0.1, speed=700):
        self.vel_y = 0
        self.gravity = 1000
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.facing_right = False
        self.facing_up = True
        self.moving = False
        self.current_frame = 0
        self.frame_duration = 0.5
        self.frame_timer = 0
        self.past_move_x_status = 0
        self.past_move_y_status = -1 #make default is original pic(หันหน้า)
        self.jump_pressed = False
        self.double_jump = False
        self.cam_x = 0
        self.cam_y = 0
       
        # Load images
        self.original_image = pygame.image.load("Pic/herta_sama_ver2.1.png").convert_alpha()
        width, height = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(width*scale), int(height*scale)))
        self.width = int(width*scale)*0.85
        self.height = int(height*scale)*0.85
        self.walk_frames = []
        self.walk_frames_up_down = []
        for i in range(1, 3):
            img = pygame.image.load(f"Pic/herta_sama_ver2.{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(width*scale), int(height*scale)))
            self.walk_frames_up_down.append(img)
        for i in range(1, 3):
            img = pygame.image.load(f"Pic/herta_sama_walking_{i}-removebg-preview.png").convert_alpha()
            img = pygame.transform.scale(img, (int(width*scale), int(height*scale)))
            self.walk_frames.append(img)
        self.hitbox = pygame.Rect (
            self.pos.x - self.width,
            self.pos.y - self.height ,
            self.width,
            self.height
        )
        self.jump_cooldown = 0
    def handle_input(self, keys, dt):
        move_dir = pygame.Vector2(0, 0) #x is 1 if pressed d and -1 if pressed a ,y is the same
        # if self.jump_cooldown > 0:
        #     self.jump_cooldown -= dt
        if keys[pygame.K_w] and self.double_jump and  self.jump_pressed :
            self.vel_y = -500
            self.double_jump = False 
        if keys[pygame.K_w]: 
            # move_dir.y -= 1
            # self.past_move_x_status = move_dir.x
            # self.past_move_y_status = move_dir.y
            if self.vel_y == 0 and self.jump_pressed:
                self.vel_y = -500
                self.jump_pressed = False
                self.double_jump = True
            
        else:
            self.jump_pressed = True
        if self.vel_y == 0:
            self.double_jump = False
          
            # print("w",move_dir.y,move_dir.x)
        if keys[pygame.K_s]:
            move_dir.y += 1
            self.past_move_x_status = move_dir.x
            self.past_move_y_status = move_dir.y
            # print("s",move_dir.y,move_dir.x)
        if keys[pygame.K_a]:
            move_dir.x -= 1
            self.past_move_x_status = move_dir.x
           
            # print("a",move_dir.x)
        if keys[pygame.K_d]:
            move_dir.x += 1
            self.past_move_x_status = move_dir.x
         
            # print("d",move_dir.x)
        # print("x past = ",self.past_move_x_status," y past= ",self.past_move_y_status)
        
        if move_dir.length_squared() > 0:
            move_dir = move_dir.normalize()
            self.pos += move_dir * self.speed * dt
            self.moving = True
        else:
            self.moving = False

        if move_dir.x > 0:
            self.facing_right = True
        elif move_dir.x < 0:
            self.facing_right = False
        if move_dir.y > 0:
            self.facing_up = True
        elif move_dir.y < 0:
            self.facing_up = False

    def update(self, dt,platforms,screen_height):
        self.vel_y += self.gravity * dt
        self.pos.y += self.vel_y * dt

        # ตรวจ collision กับ platform
        player_rect = pygame.Rect (
            self.pos.x - self.width//2,
            self.pos.y - self.height//2 ,
            self.width,
            self.height
        )
        on_platform = False
        
        for plat in platforms:
            if player_rect.colliderect(plat.rect):
                # เฉพาะกรณีตกลงมาจากด้านบน
                if self.vel_y > 0 and player_rect.bottom - plat.rect.top < 30:
                    # วางขอบล่าง hitbox player ให้อยู่ห่างขอบบน platform 2 px
                    self.pos.y = plat.rect.top - self.height // 2 + 2
                    self.vel_y = 0
                    on_platform = True
                    # อัปเดต player_rect ใหม่หลังเซ็ต pos.y กันไม่ให้มันเอาอันเก่ามาแล้วตกทะลุ
                    player_rect = pygame.Rect(
                        self.pos.x - self.width // 2,
                        self.pos.y - self.height // 2,
                        self.width,
                        self.height
                    )
        if not on_platform:
            # ยังตกต่อไป
            pass
       
        player_bottom = self.pos.y + self.height // 2
        if player_bottom > screen_height:
            self.pos.y = (screen_height// 2)
            self.pos.x = 1280-((1280*3)//4)
            self.vel_y = 0
            
        if self.moving:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        else:
            self.current_frame = 0
        


    def draw(self, surface,cx,cy):
        if self.moving:
            if  self.past_move_y_status <= 0 and self.past_move_x_status == 0:
                frame_image = self.walk_frames_up_down[1]
            elif self.past_move_y_status >=1 and self.past_move_x_status == 0:
                frame_image = self.image
            else:
                frame_image = self.walk_frames[self.current_frame]
        else:
            frame_image = self.image
        if self.facing_right:
            frame_image = pygame.transform.flip(frame_image, True, False)
        
        frame_rect = frame_image.get_rect(center=(self.pos.x-cx, self.pos.y-cy))
        surface.blit(frame_image, frame_rect)
        
        draw_hitbox(pygame.Rect(
        self.pos.x - self.width // 2 - cx,
        self.pos.y - self.height // 2 - cy,
        self.width,
        self.height
    ), surface, color=(255, 0, 0))
    # def set_start_position(self):
    #      player = Player((screen.get_width() / 4, screen.get_height() / 2), scale=0.1, speed=300) #set start
        
class Map:
    def __init__(self,pic):
        if pic == None:
            self.pic = []
        else:
            self.pic = pic
    def get_current(self,position):
        return self.pic[position//1280]
        pass
background_display = (135, 206, 235)
def main():
    
    pygame.init()
    screen_height = 720
    screen = pygame.display.set_mode((1280, screen_height))
    pygame.display.set_caption("GuruGuru Walking")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    running = True
    dt = 0

    player = Player((screen.get_width() / 4, screen.get_height() / 2), scale=0.1, speed=300) #set start
    platforms = [
                    Platform(0, 680, 1280, 40),      # Ground platform
                    Platform(300, 500, 200, 20),     # Floating platform
                    Platform(600, 400, 200, 20),     # Another platform
                ]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        camera_x = player.pos.x - screen.get_width() // 2
        camera_y = player.pos.y - screen.get_height() // 2

       
        
        
        
        # Handle collision: e.g., stop falling, set player on top of platform  
        
        screen.fill(background_display)
        radian = 40
        top = 30
        player.hitbox = pygame.Rect(
                        player.pos.x - player.width//2 ,
                        player.pos.y - player.height//2 ,
                        player.width,
                        player.height
                    )
        for plat in platforms:
            pygame.draw.rect(screen, (0, 200, 0),
                         (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height))

    # วาด player (ให้อยู่กลางจอ)
    
        
            # player.hitbox = pygame.Rect(
            #             player.pos.x - player.width//2 ,
            #             player.pos.y - player.height//2 ,
            #             player.width,
            #             player.height
            #         )
            # if player.hitbox.colliderect(plat.rect):
            # # ตรวจว่าผู้เล่นมาจากด้านบน platform
            #     if player.past_move_y_status > 0:  # กำลังตกลงมา
            #         player.pos.y = plat.rect.top - player.height // 2 + 2
            #         player.past_move_y_status = 0  # หยุดการตก
                    
                

        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt)
        player.update(dt,platforms,screen_height)
        player.draw(screen,camera_x,camera_y)
        # pygame.draw.rect(screen, (200, 50, 50),
        #              (player.pos.x - camera_x, player.pos.y - camera_y, player.width, player.height))

        if keys[pygame.K_SPACE]:
            text_surface = font.render("Nahh I would win", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(player.pos.x-camera_x, player.pos.y - radian - top-camera_y))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()