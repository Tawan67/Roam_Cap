import pygame

class Player:
    def __init__(self, pos, scale=0.1, speed=300):
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
        # Load images
        self.original_image = pygame.image.load("Pic/herta_sama_ver2.1.png").convert_alpha()
        width, height = self.original_image.get_size()
        self.image = pygame.transform.scale(self.original_image, (int(width*scale), int(height*scale)))
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

    def handle_input(self, keys, dt):
        move_dir = pygame.Vector2(0, 0) #x is 1 if pressed d and -1 if pressed a ,y is the same
        if keys[pygame.K_w]: 
            move_dir.y -= 1
            self.past_move_x_status = move_dir.x
            self.past_move_y_status = move_dir.y
            print("w",move_dir.y,move_dir.x)
        if keys[pygame.K_s]:
            move_dir.y += 1
            self.past_move_x_status = move_dir.x
            self.past_move_y_status = move_dir.y
            print("s",move_dir.y,move_dir.x)
        if keys[pygame.K_a]:
            move_dir.x -= 1
            self.past_move_x_status = move_dir.x
           
            print("a",move_dir.x)
        if keys[pygame.K_d]:
            move_dir.x += 1
            self.past_move_x_status = move_dir.x
         
            print("d",move_dir.x)
        print("x past = ",self.past_move_x_status," y past= ",self.past_move_y_status)
        
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

    def update(self, dt):
        if self.moving:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        else:
            self.current_frame = 0

    def draw(self, surface):
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

        frame_rect = frame_image.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(frame_image, frame_rect)
        
class Map:
    def __init__(self,pic):
        if pic == None:
            self.pic = []
        else:
            self.pic = pic
    def get_current(self,position):
        return self.pic[position//1280]
        pass
background_display = "purple"
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("GuruGuru Walking")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    running = True
    dt = 0

    player = Player((screen.get_width() / 4, screen.get_height() / 1.5), scale=0.1, speed=300) #set start

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_display)
        radian = 40
        top = 30

        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt)
        player.update(dt)
        player.draw(screen)

        if keys[pygame.K_SPACE]:
            text_surface = font.render("Nahh I would win", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(player.pos.x, player.pos.y - radian - top))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()