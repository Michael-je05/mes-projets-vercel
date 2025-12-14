# main.py - Version SIMPLIFIÉE qui fonctionne
import pygame
import random
import os
import sys

# Initialisation
pygame.init()
pygame.mixer.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ANIMATION_SPEED = 100

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Variables globales
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
mummies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player = None

class Button:
    def __init__(self, x, y, text, width=200, height=50):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.is_hovered = False
        self.color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        text_color = (255, 255, 200) if self.is_hovered else WHITE
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.load_player_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 7
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.score = 0
        self.invincible = False
        self.invincible_time = 1500
        self.last_hit = 0
        self.power_level = 1
    
    def load_player_image(self):
        # Chercher une image du joueur
        if os.path.exists("player"):
            for file in os.listdir("player"):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = pygame.image.load(os.path.join("player", file)).convert_alpha()
                        return pygame.transform.scale(img, (50, 50))
                    except:
                        pass
        # Image par défaut
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(surf, BLUE, [(25, 0), (0, 50), (50, 50)])
        pygame.draw.circle(surf, WHITE, (25, 15), 5)
        return surf
    
    def update(self):
        # Clignotement si invincible
        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.last_hit > self.invincible_time:
                self.invincible = False
            elif (now // 100) % 2 == 0:
                alpha = 128
                self.image.set_alpha(alpha)
        
        # Mouvement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # Garder dans l'écran
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            
            try:
                pygame.mixer.Sound("sounds/shoot.wav").play()
            except:
                pass
    
    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.last_hit = pygame.time.get_ticks()
            return True
        return False
    
    def add_score(self, points):
        self.score += points
        if self.score // 500 + 1 > self.power_level:
            self.power_level = min(3, self.score // 500 + 1)

class Alien(pygame.sprite.Sprite):
    def __init__(self, difficulty=1):
        super().__init__()
        self.image = self.load_alien_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -100)
        self.difficulty = difficulty
        self.speedx = random.choice([-2, -1, 1, 2]) * (1 + difficulty * 0.2)
        self.speedy = random.randrange(1, 3) * (1 + difficulty * 0.2)
        self.health = 20
        self.value = 10
        self.can_shoot = difficulty >= 2
        self.shoot_delay = 3000
        self.last_shot = pygame.time.get_ticks()
    
    def load_alien_image(self):
        if os.path.exists("aliens"):
            files = os.listdir("aliens")
            if files:
                try:
                    img = pygame.image.load(os.path.join("aliens", random.choice(files))).convert_alpha()
                    return pygame.transform.scale(img, (45, 45))
                except:
                    pass
        surf = pygame.Surface((45, 45), pygame.SRCALPHA)
        pygame.draw.circle(surf, GREEN, (22, 22), 20)
        pygame.draw.circle(surf, RED, (22, 22), 10)
        return surf
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speedx = -self.speedx
        
        if self.can_shoot:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
        
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -100)
    
    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, "alien")
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

class Mummy(pygame.sprite.Sprite):
    def __init__(self, difficulty=1):
        super().__init__()
        self.image = self.load_mummy_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -150)
        self.difficulty = difficulty
        self.speedx = random.choice([-1, 0, 1])
        self.speedy = random.randrange(1, 2)
        self.health = 40
        self.value = 25
        self.shoot_delay = max(1000, 3000 - difficulty * 500)
        self.last_shot = pygame.time.get_ticks()
    
    def load_mummy_image(self):
        if os.path.exists("mummy"):
            files = os.listdir("mummy")
            if files:
                try:
                    img = pygame.image.load(os.path.join("mummy", random.choice(files))).convert_alpha()
                    return pygame.transform.scale(img, (55, 55))
                except:
                    pass
        surf = pygame.Surface((55, 55), pygame.SRCALPHA)
        pygame.draw.rect(surf, PURPLE, (0, 0, 55, 55))
        pygame.draw.rect(surf, (200, 100, 200), (5, 5, 45, 45))
        return surf
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
        
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()
    
    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, "mummy")
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, YELLOW, (0, 0, 8, 20))
        pygame.draw.rect(self.image, (255, 200, 0), (0, 0, 8, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -12
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.image = pygame.Surface((6, 15), pygame.SRCALPHA)
        color = GREEN if enemy_type == "alien" else PURPLE
        pygame.draw.rect(self.image, color, (0, 0, 6, 15))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Defender")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"
        self.score = 0
        self.level = 1
        self.wave = 1
        self.difficulty = 1
        
        # Polices
        self.font_title = pygame.font.SysFont('arial', 64, bold=True)
        self.font_large = pygame.font.SysFont('arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 32)
        self.font_small = pygame.font.SysFont('arial', 24)
        
        # Background
        self.background = self.create_background()
        
        # Boutons
        self.start_button = Button(SCREEN_WIDTH // 2, 350, "COMMENCER")
        self.quit_button = Button(SCREEN_WIDTH // 2, 420, "QUITTER")
        
        # Initialiser le jeu
        self.init_game()
    
    def create_background(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill((10, 10, 40))
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(surf, WHITE, (x, y), 1)
        return surf
    
    def init_game(self):
        global all_sprites, aliens, mummies, bullets, enemy_bullets, player
        
        all_sprites.empty()
        aliens.empty()
        mummies.empty()
        bullets.empty()
        enemy_bullets.empty()
        
        player = Player()
        all_sprites.add(player)
        
        for _ in range(6):
            alien = Alien(self.difficulty)
            all_sprites.add(alien)
            aliens.add(alien)
    
    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        
        # Titre centré
        title1 = self.font_title.render("SPACE", True, WHITE)
        title2 = self.font_title.render("DEFENDER", True, (0, 200, 255))
        title1_rect = title1.get_rect(center=(SCREEN_WIDTH // 2, 150))
        title2_rect = title2.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(title1, title1_rect)
        self.screen.blit(title2, title2_rect)
        
        # Boutons
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        # Contrôles à droite
        controls_x = SCREEN_WIDTH - 250
        controls_title = self.font_medium.render("CONTROLES", True, (0, 255, 255))
        self.screen.blit(controls_title, (controls_x, 300))
        
        controls = ["ZQSD/FLECHES: Déplacer", "ESPACE: Tirer", "ECHAP: Menu"]
        for i, text in enumerate(controls):
            y = 350 + i * 40
            self.draw_text(text, self.font_small, WHITE, controls_x, y)
    
    def draw_playing(self):
        self.screen.blit(self.background, (0, 0))
        all_sprites.draw(self.screen)
        self.draw_hud()
    
    def draw_game_over(self):
        self.screen.blit(self.background, (0, 0))
        
        game_over = self.font_large.render("GAME OVER", True, RED)
        score_text = self.font_medium.render(f"Score: {self.score}", True, YELLOW)
        
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 200))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_medium.render("Cliquez pour revenir au menu", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_hud(self):
        # Score
        score_text = f"Score: {player.score}"
        self.draw_text(score_text, self.font_medium, WHITE, 20, 10)
        
        # Vies
        lives_text = f"Vies: {player.lives}"
        self.draw_text(lives_text, self.font_medium, WHITE, 20, 50)
        
        # Niveau
        level_text = f"Niveau: {self.level}"
        self.draw_text(level_text, self.font_medium, YELLOW, SCREEN_WIDTH - 150, 10)
        
        # Difficulté
        diff_text = f"Difficulté: {self.difficulty}"
        self.draw_text(diff_text, self.font_small, WHITE, SCREEN_WIDTH - 150, 50)
    
    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    elif self.game_state == "menu":
                        self.running = False
                
                if self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        player.shoot()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if self.game_state == "menu":
                    if self.start_button.is_clicked(pos):
                        self.start_new_game()
                    elif self.quit_button.is_clicked(pos):
                        self.running = False
                
                elif self.game_state == "game_over":
                    self.game_state = "menu"
    
    def update_game(self):
        if self.game_state != "playing":
            return
        
        all_sprites.update()
        
        # Collisions balles -> ennemis
        for enemy in list(aliens) + list(mummies):
            hits = pygame.sprite.spritecollide(enemy, bullets, True)
            for bullet in hits:
                enemy.health -= 10
                if enemy.health <= 0:
                    enemy.kill()
                    player.add_score(enemy.value)
                    self.score = player.score
        
        # Collisions balles ennemies -> joueur
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            if player.take_damage():
                if player.lives <= 0:
                    self.game_state = "game_over"
        
        # Collisions joueur -> ennemis (contact direct) - PERDRE UNE VIE
        hits = pygame.sprite.spritecollide(player, aliens, False)
        hits += pygame.sprite.spritecollide(player, mummies, False)
        
        for enemy in hits:
            if player.take_damage():
                enemy.kill()  # L'ennemi est détruit au contact
                
                if player.lives <= 0:
                    self.game_state = "game_over"
        
        # Augmenter la difficulté avec le score
        self.difficulty = min(5, 1 + self.score // 500)
        self.level = 1 + self.score // 1000
        
        # Spawn de nouveaux ennemis
        if len(aliens) < 4 + self.difficulty:
            alien = Alien(self.difficulty)
            all_sprites.add(alien)
            aliens.add(alien)
        
        if random.random() < 0.01 and len(mummies) < 1 + self.difficulty // 2:
            mummy = Mummy(self.difficulty)
            all_sprites.add(mummy)
            mummies.add(mummy)
    
    def start_new_game(self):
        self.score = 0
        self.level = 1
        self.wave = 1
        self.difficulty = 1
        self.game_state = "playing"
        self.init_game()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update_game()
            
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "playing":
                self.draw_playing()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()