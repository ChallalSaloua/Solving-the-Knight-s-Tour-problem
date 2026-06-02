import pygame
import sys
import math
import random
import time
from pygame import gfxdraw
from enum import Enum

# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
CELL_SIZE = 70
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 150
FPS = 60

# États du jeu
class GameState(Enum):
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    SOLUTION_COMPLETE = "SOLUTION_COMPLETE"
    GAME_OVER = "GAME_OVER"
    SETTINGS = "SETTINGS"

class Colors:
    # Couleurs principales
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Palette améliorée
    PRIMARY_BLUE = (41, 128, 185)
    PRIMARY_GREEN = (46, 204, 113)
    PRIMARY_PURPLE = (155, 89, 182)
    PRIMARY_ORANGE = (230, 126, 34)
    PRIMARY_RED = (231, 76, 60)
    ACCENT_CYAN = (52, 152, 219)
    ACCENT_TEAL = (26, 188, 156)
    
    # Nouvelles couleurs d'échiquier - Plus modernes
    CHESS_LIGHT = (240, 217, 181)  # Beige clair élégant
    CHESS_DARK = (181, 136, 99)    # Marron doux
    
    # Alternative 2 - Style bois naturel
    WOOD_LIGHT = (245, 222, 179)
    WOOD_DARK = (139, 90, 43)
    
    MODERN_LIGHT = (234, 240, 246)  
    MODERN_DARK = (96, 125, 139)    
    
    # Couleurs du ciel
    SKY_BLUE = (135, 206, 235)
    DEEP_BLUE = (25, 25, 112)
    
    # Couleurs UI
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (200, 200, 200)
    
    # Couleurs de transparence
    TRANSPARENT_BLACK = (0, 0, 0, 128)
    TRANSPARENT_WHITE = (255, 255, 255, 128)

class Particle:
    """Système de particules amélioré"""
    def __init__(self, x, y, color, velocity=None, size=None, lifetime=30):
        self.x = x
        self.y = y
        self.vx = velocity[0] if velocity else random.uniform(-3, 3)
        self.vy = velocity[1] if velocity else random.uniform(-3, 3)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size if size else random.randint(2, 6)
        self.gravity = 0.1
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        self.size = max(1, self.size * (self.lifetime / self.max_lifetime))
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color[:3], alpha) if len(self.color) == 4 else self.color
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))
            
            if self.lifetime > self.max_lifetime * 0.5:
                glow_surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color[:3], alpha // 4), 
                                 (self.size * 2, self.size * 2), self.size * 2)
                screen.blit(glow_surf, (self.x - self.size * 2, self.y - self.size * 2))

class Star:
    """Étoile animée pour le fond"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        
    def update(self):
        self.brightness = 0.5 + 0.5 * math.sin(time.time() * self.twinkle_speed)
        
    def draw(self, screen):
        color = int(255 * self.brightness)
        pygame.draw.circle(screen, (color, color, color), (self.x, self.y), self.size)

class Button:
    """Bouton amélioré avec meilleur affichage"""
    def __init__(self, x, y, width, height, text, action, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        if color is None:
            if "JOUER" in text or "play" in action:
                color = Colors.PRIMARY_GREEN
            elif "SOLUTIONS" in text or "solution" in action:
                color = Colors.PRIMARY_BLUE
            elif "RESTART" in text or "restart" in action:
                color = Colors.PRIMARY_ORANGE
            elif "QUITTER" in text or "quit" in action:
                color = Colors.PRIMARY_RED
            elif "ROTATION" in text or "rotation" in action:
                color = Colors.PRIMARY_PURPLE
            else:
                color = Colors.ACCENT_TEAL
        
        self.color = color
        self.hover_color = self.lighten_color(color, 30)
        self.pressed_color = self.darken_color(color, 20)
        self.is_hovered = False
        self.is_pressed = False
        self.animation_offset = 0
        self.particles = []
        self.glow_intensity = 0
        
    def lighten_color(self, color, amount):
        return tuple(min(255, c + amount) for c in color)
    
    def darken_color(self, color, amount):
        return tuple(max(0, c - amount) for c in color)
        
    def update(self, mouse_pos, mouse_clicked):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered:
            self.animation_offset = min(4, self.animation_offset + 0.4)
            self.glow_intensity = min(1.0, self.glow_intensity + 0.08)
            if random.random() < 0.05:
                self.particles.append(
                    Particle(random.randint(self.rect.left, self.rect.right),
                           random.randint(self.rect.top, self.rect.bottom),
                           self.color, lifetime=15))
        else:
            self.animation_offset = max(0, self.animation_offset - 0.4)
            self.glow_intensity = max(0, self.glow_intensity - 0.08)
            
        if self.is_hovered and mouse_clicked:
            self.is_pressed = True
        else:
            self.is_pressed = False
            
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen, font):
        # Dessiner les particules
        for particle in self.particles:
            particle.draw(screen)
            
        # Position du bouton avec animation
        button_rect = self.rect.copy()
        button_rect.y -= self.animation_offset
        
        # Effet de glow pour le survol
        if self.glow_intensity > 0:
            glow_size = int(8 + self.glow_intensity * 8)
            glow_surf = pygame.Surface((button_rect.width + glow_size*2, 
                                       button_rect.height + glow_size*2), pygame.SRCALPHA)
            glow_alpha = int(60 + self.glow_intensity * 40)
            pygame.draw.rect(glow_surf, (*self.hover_color, glow_alpha), 
                           glow_surf.get_rect(), border_radius=12)
            screen.blit(glow_surf, (button_rect.x - glow_size, button_rect.y - glow_size))
        
        # Ombre portée plus subtile
        shadow_rect = button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 60), shadow_surf.get_rect(), border_radius=10)
        screen.blit(shadow_surf, shadow_rect)
        
        # Couleur du bouton
        color = self.pressed_color if self.is_pressed else (self.hover_color if self.is_hovered else self.color)
        
        # Fond du bouton avec dégradé simulé
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        
        # Bordure plus visible
        border_color = self.lighten_color(color, 50) if self.is_hovered else self.darken_color(color, 30)
        pygame.draw.rect(screen, border_color, button_rect, 3, border_radius=10)
        
        # Effet de brillance sur le haut
        if not self.is_pressed:
            highlight_rect = pygame.Rect(button_rect.x + 6, button_rect.y + 4, 
                                        button_rect.width - 12, button_rect.height // 4)
            highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            for i in range(highlight_rect.height):
                alpha = int(40 * (1 - i / highlight_rect.height))
                pygame.draw.line(highlight_surf, (255, 255, 255, alpha), 
                               (0, i), (highlight_rect.width, i))
            screen.blit(highlight_surf, highlight_rect)
        
        # Texte avec ombre plus marquée
        offset_y = 2 if self.is_pressed else 0
        
        # Ombre du texte
        shadow_text = font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(button_rect.centerx + 2, 
                                                   button_rect.centery + 2 + offset_y))
        shadow_surf = pygame.Surface(shadow_text.get_size(), pygame.SRCALPHA)
        shadow_surf.blit(shadow_text, (0, 0))
        shadow_surf.set_alpha(100)
        screen.blit(shadow_surf, shadow_rect)
        
        # Texte principal
        text_surface = font.render(self.text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=(button_rect.centerx, 
                                                  button_rect.centery + offset_y))
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked

class KnightTourGame:
    def __init__(self, best_solution=None, all_solutions=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Knight's Tour - Genetic Algorithm Game")
        self.clock = pygame.time.Clock()
        
        # Polices
        try:
            self.font_title = pygame.font.Font(None, 72)
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font_title = pygame.font.SysFont('arial', 72, bold=True)
            self.font_large = pygame.font.SysFont('arial', 48, bold=True)
            self.font_medium = pygame.font.SysFont('arial', 36, bold=True)
            self.font_small = pygame.font.SysFont('arial', 24)
        
        # Solutions
        self.best_solution = best_solution
        self.all_solutions = all_solutions or []
        self.current_solution_index = 0
        self.current_solution = self.best_solution or (self.all_solutions[0][0] if self.all_solutions else None)
        
        # Choix du style d'échiquier (changez ici pour tester différents styles)
        self.chess_style = "modern"  # Options: "classic", "wood", "modern"
        
        # État du jeu
        self.state = GameState.MENU
        self.running = True
        self.current_move_index = 0
        self.animation_speed = 300
        self.last_move_time = 0
        
        # Systèmes d'effets
        self.particles = []
        self.stars = [Star() for _ in range(100)]
        
        # Animation et UI
        self.menu_selection = 0
        self.show_grid = True
        self.auto_rotate = False
        self.rotation_angle = 0
        self.screen_shake = 0
        
        # Score et statistiques
        self.score = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.best_score = 0
        self.combo = 0
        self.moves_count = 0
        
        # Créer les boutons
        self.create_buttons()
        
        # Charger les ressources
        self.load_assets()
        
        # Animation du menu
        self.menu_time = 0
        self.background_offset = 0
        
    def get_chess_colors(self):
        """Retourne les couleurs d'échiquier selon le style choisi"""
        if self.chess_style == "wood":
            return Colors.WOOD_LIGHT, Colors.WOOD_DARK
        elif self.chess_style == "modern":
            return Colors.MODERN_LIGHT, Colors.MODERN_DARK
        else:  # classic
            return Colors.CHESS_LIGHT, Colors.CHESS_DARK
        
    def create_buttons(self):
        """Crée tous les boutons avec meilleur espacement et taille"""
        # Boutons du menu - redessinés
        button_width = 380
        button_height = 65
        start_y = 260
        spacing = 85
        
        self.menu_buttons = [
            Button(SCREEN_WIDTH//2 - button_width//2, start_y, button_width, button_height, 
                   "JOUER", "play", Colors.PRIMARY_GREEN),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + spacing, button_width, button_height, 
                   "SOLUTIONS", "solutions", Colors.PRIMARY_BLUE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + spacing*2, button_width, button_height, 
                   "OPTIONS", "options", Colors.PRIMARY_PURPLE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + spacing*3, button_width, button_height, 
                   "QUITTER", "quit", Colors.PRIMARY_RED)
        ]
        
        # Boutons du jeu - repositionnés
        game_btn_x = SCREEN_WIDTH - 220
        game_btn_width = 190
        game_btn_height = 48
        
        self.game_buttons = [
            Button(game_btn_x, 120, game_btn_width, game_btn_height, "MENU", "menu", Colors.ACCENT_TEAL),
            Button(game_btn_x, 178, game_btn_width, game_btn_height, "PAUSE", "pause", Colors.PRIMARY_ORANGE),
            Button(game_btn_x, 236, game_btn_width, game_btn_height, "RESTART", "restart", Colors.PRIMARY_BLUE),
            Button(game_btn_x, 294, 88, game_btn_height, "-", "speed_down", Colors.LIGHT_GRAY),
            Button(game_btn_x + 102, 294, 88, game_btn_height, "+", "speed_up", Colors.PRIMARY_GREEN),
            Button(game_btn_x, 352, game_btn_width, game_btn_height, "GRILLE", "toggle_grid", Colors.PRIMARY_PURPLE),
            Button(game_btn_x, 410, game_btn_width, game_btn_height, "ROTATION", "toggle_rotation", Colors.ACCENT_CYAN)
        ]
        
        # Boutons de navigation
        nav_btn_width = 88
        self.nav_buttons = [
            Button(game_btn_x, 490, nav_btn_width, game_btn_height, "PREC", "prev_solution", Colors.ACCENT_TEAL),
            Button(game_btn_x + 102, 490, nav_btn_width, game_btn_height, "SUIV", "next_solution", Colors.ACCENT_TEAL)
        ]
        
    def load_assets(self):
        """Charge les ressources du jeu"""
        self.knight_surface = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10), pygame.SRCALPHA)
        self.draw_realistic_knight(self.knight_surface, CELL_SIZE//2-5, CELL_SIZE//2-5, 25)
        
        try:
            self.move_sound = pygame.mixer.Sound("move.wav")
            self.complete_sound = pygame.mixer.Sound("complete.wav")
            self.menu_sound = pygame.mixer.Sound("menu.wav")
        except:
            self.move_sound = None
            self.complete_sound = None
            self.menu_sound = None
            
    def draw_realistic_knight(self, surface, x, y, size):
        """Dessine un cavalier réaliste"""
        body_points = [
            (x - size//2, y - size//4),
            (x - size//3, y - size//2),
            (x + size//4, y - size//2),
            (x + size//2, y - size//4),
            (x + size//2, y + size//4),
            (x - size//2, y + size//4)
        ]
        pygame.draw.polygon(surface, Colors.WHITE, body_points)
        pygame.draw.polygon(surface, Colors.BLACK, body_points, 2)
        
        head_points = [
            (x + size//4, y - size//2),
            (x + size//2, y - size//3),
            (x + size//2, y - size//6),
            (x + size//3, y - size//4)
        ]
        pygame.draw.polygon(surface, Colors.WHITE, head_points)
        pygame.draw.polygon(surface, Colors.BLACK, head_points, 2)
        
        ear1_points = [
            (x + size//3, y - size//2),
            (x + size//3 + 3, y - size//2 - 8),
            (x + size//3 + 6, y - size//2)
        ]
        pygame.draw.polygon(surface, Colors.WHITE, ear1_points)
        pygame.draw.polygon(surface, Colors.BLACK, ear1_points, 1)
        
        ear2_points = [
            (x + size//3 + 10, y - size//2),
            (x + size//3 + 13, y - size//2 - 8),
            (x + size//3 + 16, y - size//2)
        ]
        pygame.draw.polygon(surface, Colors.WHITE, ear2_points)
        pygame.draw.polygon(surface, Colors.BLACK, ear2_points, 1)
        
        pygame.draw.circle(surface, Colors.BLACK, (x + size//3 + 8, y - size//3), 2)
        
        leg_width = 3
        legs = [
            [(x - size//3, y + size//4), (x - size//3, y + size//2)],
            [(x - size//6, y + size//4), (x - size//6, y + size//2)],
            [(x + size//6, y + size//4), (x + size//6, y + size//2)],
            [(x + size//3, y + size//4), (x + size//3, y + size//2)]
        ]
        
        for leg in legs:
            pygame.draw.line(surface, Colors.BLACK, leg[0], leg[1], leg_width)
            pygame.draw.circle(surface, Colors.BLACK, leg[1], 3)
            
        tail_points = [
            (x - size//2, y),
            (x - size//2 - 10, y - size//6),
            (x - size//2 - 8, y + size//6)
        ]
        pygame.draw.polygon(surface, Colors.WHITE, tail_points)
        pygame.draw.polygon(surface, Colors.BLACK, tail_points, 2)
        
        mane_points = [
            (x, y - size//2),
            (x - size//6, y - size//3),
            (x - size//6, y),
            (x, y - size//4)
        ]
        pygame.draw.polygon(surface, Colors.BLACK, mane_points)
        
    def create_explosion(self, x, y, color, count=30):
        """Crée une explosion de particules"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            self.particles.append(Particle(x, y, color, velocity, random.randint(2, 8), random.randint(20, 40)))
            
    def draw_background(self):
        """Dessine un fond animé"""
        for i in range(SCREEN_HEIGHT):
            progress = i / SCREEN_HEIGHT
            r = int(Colors.DEEP_BLUE[0] * (1 - progress) + Colors.SKY_BLUE[0] * progress)
            g = int(Colors.DEEP_BLUE[1] * (1 - progress) + Colors.SKY_BLUE[1] * progress)
            b = int(Colors.DEEP_BLUE[2] * (1 - progress) + Colors.SKY_BLUE[2] * progress)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        for star in self.stars:
            star.update()
            star.draw(self.screen)
        
        self.background_offset += 0.5
        mountain_offset = self.background_offset % 100
        
        mountain_points = [
            (0, SCREEN_HEIGHT // 2),
            (150, SCREEN_HEIGHT // 3),
            (300, SCREEN_HEIGHT // 2.5),
            (450, SCREEN_HEIGHT // 3.5),
            (600, SCREEN_HEIGHT // 2.8),
            (750, SCREEN_HEIGHT // 3.2),
            (900, SCREEN_HEIGHT // 2.6),
            (SCREEN_WIDTH, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, SCREEN_HEIGHT)
        ]
        pygame.draw.polygon(self.screen, (100, 100, 150), mountain_points)
        
        for i in range(3):
            x = (i * 400 + mountain_offset) % (SCREEN_WIDTH + 200) - 100
            y = 80 + i * 40
            self.draw_cloud(x, y)
            
    def draw_cloud(self, x, y):
        """Dessine un nuage"""
        cloud_color = (255, 255, 255, 180)
        cloud_surf = pygame.Surface((120, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(cloud_surf, cloud_color, (0, 20, 40, 40))
        pygame.draw.ellipse(cloud_surf, cloud_color, (20, 10, 40, 40))
        pygame.draw.ellipse(cloud_surf, cloud_color, (40, 15, 40, 40))
        pygame.draw.ellipse(cloud_surf, cloud_color, (60, 20, 40, 40))
        pygame.draw.ellipse(cloud_surf, cloud_color, (80, 25, 40, 35))
        self.screen.blit(cloud_surf, (x, y))
        
    def draw_menu(self):
        """Dessine le menu principal"""
        self.draw_background()
        
        vignette_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for i in range(0, SCREEN_WIDTH // 2, 5):
            alpha = int(255 * (i / (SCREEN_WIDTH // 2)))
            pygame.draw.circle(vignette_surf, (0, 0, 0, alpha // 4), 
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                             SCREEN_WIDTH // 2 - i)
        self.screen.blit(vignette_surf, (0, 0))
        
        title_offset = math.sin(self.menu_time * 2) * 3
        title_y = 120 + title_offset
        
        title_text = self.font_title.render("KNIGHT'S TOUR", True, Colors.PRIMARY_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        
        # Ombre du titre
        shadow_text = self.font_title.render("KNIGHT'S TOUR", True, Colors.BLACK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, title_y + 3))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        subtitle = self.font_medium.render("Genetic Algorithm Adventure", True, Colors.ACCENT_TEAL)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, title_y + 55))
        self.screen.blit(subtitle, subtitle_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.menu_buttons:
            button.update(mouse_pos, mouse_clicked)
            button.draw(self.screen, self.font_large)
            
        instructions = [
            "Utilisez la souris ou les fleches pour naviguer",
            "CLIC GAUCHE ou ENTREE pour selectionner",
            "ESC pour quitter"
        ]
        y_offset = SCREEN_HEIGHT - 110
        for instruction in instructions:
            text = self.font_small.render(instruction, True, Colors.LIGHT_GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 28
            
    def draw_board(self):
        """Dessine l'échiquier avec les nouvelles couleurs"""
        shake_x = math.sin(self.screen_shake) * 2 if self.screen_shake > 0 else 0
        shake_y = math.cos(self.screen_shake * 1.5) * 2 if self.screen_shake > 0 else 0
        
        board_surf = pygame.Surface((BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE))
        light_color, dark_color = self.get_chess_colors()
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                color = light_color if (row + col) % 2 == 0 else dark_color
                    
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(board_surf, color, rect)
                
                # Dégradé subtil pour donner de la profondeur
                gradient_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                for i in range(CELL_SIZE // 2):
                    alpha = int(15 * (1 - i / (CELL_SIZE // 2)))
                    pygame.draw.line(gradient_surf, (0, 0, 0, alpha), (i, i), (CELL_SIZE - i, i))
                board_surf.blit(gradient_surf, (x, y))
                
                if self.current_solution and self.current_solution.path:
                    for i, pos in enumerate(self.current_solution.path[:self.current_move_index + 1]):
                        if pos == (col, row):
                            pulse = abs(math.sin(time.time() * 3 + i * 0.1)) * 0.4 + 0.6
                            highlight_color = (
                                int(Colors.PRIMARY_GREEN[0] * pulse),
                                int(Colors.PRIMARY_GREEN[1] * pulse),
                                int(Colors.PRIMARY_GREEN[2] * pulse)
                            )
                            pygame.draw.rect(board_surf, highlight_color, rect, 4)
                            
                            if i == self.current_move_index:
                                glow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                                pygame.draw.rect(glow_surf, (*highlight_color, 80), glow_surf.get_rect())
                                board_surf.blit(glow_surf, (x, y))
                
                if self.show_grid:
                    pygame.draw.rect(board_surf, Colors.BLACK, rect, 1)
                    
        board_rect = board_surf.get_rect()
        board_rect.topleft = (BOARD_OFFSET_X + shake_x, BOARD_OFFSET_Y + shake_y)
        self.screen.blit(board_surf, board_rect)
        
        for i in range(BOARD_SIZE):
            letter = self.font_small.render(chr(ord('a') + i), True, Colors.LIGHT_GRAY)
            letter_rect = letter.get_rect(
                center=(BOARD_OFFSET_X + i * CELL_SIZE + CELL_SIZE // 2 + shake_x, 
                       BOARD_OFFSET_Y - 20 + shake_y)
            )
            self.screen.blit(letter, letter_rect)
            
            number = self.font_small.render(str(BOARD_SIZE - i), True, Colors.LIGHT_GRAY)
            number_rect = number.get_rect(
                center=(BOARD_OFFSET_X - 20 + shake_x, 
                       BOARD_OFFSET_Y + i * CELL_SIZE + CELL_SIZE // 2 + shake_y)
            )
            self.screen.blit(number, number_rect)
            
    def draw_knight(self):
        """Dessin du cavalier"""
        if not self.current_solution or self.current_move_index >= len(self.current_solution.path):
            return
            
        pos = self.current_solution.path[self.current_move_index]
        x = BOARD_OFFSET_X + pos[0] * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_OFFSET_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
        
        self.rotation_angle += 1.5
        
        knight_rotated = pygame.transform.rotate(self.knight_surface, self.rotation_angle)
        knight_rect = knight_rotated.get_rect(center=(x, y))
        
        for i in range(3):
            trail_surf = pygame.Surface((CELL_SIZE + 10, CELL_SIZE + 10), pygame.SRCALPHA)
            alpha = 80 - i * 25
            pygame.draw.circle(trail_surf, (*Colors.PRIMARY_BLUE[:3], alpha), 
                             (CELL_SIZE // 2 + 5, CELL_SIZE // 2 + 5), CELL_SIZE // 2 - i * 2)
            self.screen.blit(trail_surf, (x - CELL_SIZE // 2 - 5, y - CELL_SIZE // 2 - 5))
            
        self.screen.blit(knight_rotated, knight_rect)
        
        num_text = self.font_medium.render(str(self.current_move_index + 1), True, Colors.WHITE)
        num_rect = num_text.get_rect(center=(x, y))
        
        pygame.draw.circle(self.screen, Colors.PRIMARY_BLUE, num_rect.center, num_rect.width // 2 + 8)
        pygame.draw.circle(self.screen, Colors.WHITE, num_rect.center, num_rect.width // 2 + 6, 2)
        self.screen.blit(num_text, num_rect)
        
    def draw_path(self):
        """Dessine le chemin avec numéros"""
        if not self.current_solution or len(self.current_solution.path) < 2:
            return
            
        for i in range(min(self.current_move_index + 1, len(self.current_solution.path) - 1)):
            start_pos = self.current_solution.path[i]
            end_pos = self.current_solution.path[i + 1]
            
            start_x = BOARD_OFFSET_X + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
            start_y = BOARD_OFFSET_Y + start_pos[1] * CELL_SIZE + CELL_SIZE // 2
            
            end_x = BOARD_OFFSET_X + end_pos[0] * CELL_SIZE + CELL_SIZE // 2
            end_y = BOARD_OFFSET_Y + end_pos[1] * CELL_SIZE + CELL_SIZE // 2
            
            pygame.draw.line(self.screen, Colors.ACCENT_TEAL, (start_x, start_y), (end_x, end_y), 3)
                
        for i in range(min(self.current_move_index + 1, len(self.current_solution.path))):
            pos = self.current_solution.path[i]
            x = BOARD_OFFSET_X + pos[0] * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_OFFSET_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
            
            if i == 0:
                pulse = abs(math.sin(time.time() * 2)) * 3 + 8
                pygame.draw.circle(self.screen, Colors.PRIMARY_GREEN, (x, y), int(pulse))
                pygame.draw.circle(self.screen, Colors.WHITE, (x, y), int(pulse - 2), 1)
                
                num_text = self.font_small.render(str(i + 1), True, Colors.WHITE)
                num_rect = num_text.get_rect(center=(x, y))
                pygame.draw.circle(self.screen, Colors.PRIMARY_GREEN, num_rect.center, num_rect.width // 2 + 4)
                pygame.draw.circle(self.screen, Colors.WHITE, num_rect.center, num_rect.width // 2 + 2, 1)
                self.screen.blit(num_text, num_rect)
                
            elif i == len(self.current_solution.path) - 1 and self.state == GameState.SOLUTION_COMPLETE:
                pulse = abs(math.sin(time.time() * 3)) * 6 + 10
                pygame.draw.circle(self.screen, Colors.PRIMARY_RED, (x, y), int(pulse))
                pygame.draw.circle(self.screen, Colors.WHITE, (x, y), int(pulse - 3), 1)
                
                num_text = self.font_small.render(str(i + 1), True, Colors.WHITE)
                num_rect = num_text.get_rect(center=(x, y))
                pygame.draw.circle(self.screen, Colors.PRIMARY_RED, num_rect.center, num_rect.width // 2 + 4)
                pygame.draw.circle(self.screen, Colors.WHITE, num_rect.center, num_rect.width // 2 + 2, 1)
                self.screen.blit(num_text, num_rect)
                
                if random.random() < 0.15:
                    self.create_explosion(x, y, Colors.GOLD, 8)
                    
            else:
                pulse = abs(math.sin(time.time() * 2 + i * 0.2)) * 2 + 4
                pygame.draw.circle(self.screen, Colors.PRIMARY_BLUE, (x, y), int(pulse))
                pygame.draw.circle(self.screen, Colors.WHITE, (x, y), int(pulse - 1), 1)
                
                num_text = self.font_small.render(str(i + 1), True, Colors.WHITE)
                num_rect = num_text.get_rect(center=(x, y))
                pygame.draw.circle(self.screen, Colors.PRIMARY_BLUE, num_rect.center, num_rect.width // 2 + 4)
                pygame.draw.circle(self.screen, Colors.WHITE, num_rect.center, num_rect.width // 2 + 2, 1)
                self.screen.blit(num_text, num_rect)
                
    def draw_ui(self):
        """Interface utilisateur améliorée"""
        top_bar = pygame.Surface((SCREEN_WIDTH, 110), pygame.SRCALPHA)
        pygame.draw.rect(top_bar, (*Colors.BLACK[:3], 180), top_bar.get_rect(), border_radius=8)
        self.screen.blit(top_bar, (0, 0))
        
        pygame.draw.rect(self.screen, Colors.ACCENT_TEAL, (0, 0, SCREEN_WIDTH, 110), 2)
        
        self.score = self.current_move_index * 100 + self.combo * 50
        
        score_text = self.font_large.render(f"SCORE {self.score:06d}", True, Colors.GOLD)
        score_rect = score_text.get_rect(topleft=(20, 30))
        self.screen.blit(score_text, score_rect)
        
        if self.combo > 0:
            combo_text = self.font_small.render(f"COMBO x{self.combo}", True, Colors.PRIMARY_ORANGE)
            combo_rect = combo_text.get_rect(topleft=(20, 75))
            self.screen.blit(combo_text, combo_rect)
        
        # Affichage du mouvement actuel
        if self.current_solution:
            move_text = self.font_medium.render(f"Mouvement: {self.current_move_index + 1}/{len(self.current_solution.path)}", 
                                               True, Colors.WHITE)
            move_rect = move_text.get_rect(topleft=(SCREEN_WIDTH // 2 - 120, 35))
            self.screen.blit(move_text, move_rect)
            
        side_panel = pygame.Surface((250, SCREEN_HEIGHT - 130), pygame.SRCALPHA)
        pygame.draw.rect(side_panel, (*Colors.BLACK[:3], 190), side_panel.get_rect(), border_radius=8)
        self.screen.blit(side_panel, (SCREEN_WIDTH - 260, 105))
        
        pygame.draw.rect(self.screen, Colors.PRIMARY_BLUE, 
                        (SCREEN_WIDTH - 260, 105, 250, SCREEN_HEIGHT - 130), 2)
        
        title = self.font_medium.render("STATUS", True, Colors.PRIMARY_BLUE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH - 135, y=560)
        self.screen.blit(title, title_rect)
        
        if self.current_solution:
            info_y = 610
            line_height = 35
            
            if len(self.all_solutions) > 1:
                sol_text = self.font_small.render(f"Solution: {self.current_solution_index + 1}/{len(self.all_solutions)}", 
                                                 True, Colors.LIGHT_GRAY)
                self.screen.blit(sol_text, (SCREEN_WIDTH - 245, info_y))
                info_y += line_height
                
            visited = len(self.current_solution.path)
            visited_text = self.font_small.render(f"Cases: {visited}/64", True, Colors.PRIMARY_GREEN)
            self.screen.blit(visited_text, (SCREEN_WIDTH - 245, info_y))
            info_y += line_height
            
            progress = (visited / 64) * 100
            progress_text = self.font_small.render(f"Progress: {progress:.0f}%", True, Colors.ACCENT_TEAL)
            self.screen.blit(progress_text, (SCREEN_WIDTH - 245, info_y))
            info_y += line_height
            
            bar_rect = pygame.Rect(SCREEN_WIDTH - 245, info_y, 230, 20)
            pygame.draw.rect(self.screen, Colors.DARK_GRAY, bar_rect, border_radius=3)
            fill_width = int(230 * progress / 100)
            fill_rect = pygame.Rect(SCREEN_WIDTH - 245, info_y, fill_width, 20)
            pygame.draw.rect(self.screen, Colors.PRIMARY_GREEN, fill_rect, border_radius=3)
            pygame.draw.rect(self.screen, Colors.PRIMARY_GREEN, bar_rect, 1, border_radius=3)
            
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.game_buttons:
            button.update(mouse_pos, mouse_clicked)
            button.draw(self.screen, self.font_small)
            
        if len(self.all_solutions) > 1:
            for button in self.nav_buttons:
                button.update(mouse_pos, mouse_clicked)
                button.draw(self.screen, self.font_small)
                
        if self.state == GameState.SOLUTION_COMPLETE:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*Colors.BLACK[:3], 140))
            self.screen.blit(overlay, (0, 0))
            
            complete_text = self.font_title.render("SOLUTION COMPLETE!", True, Colors.PRIMARY_GREEN)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(complete_text, complete_rect)
            
            final_score = self.font_large.render(f"Final Score: {self.score:06d}", True, Colors.GOLD)
            final_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(final_score, final_rect)
            
    def update_particles(self):
        """Met à jour toutes les particules"""
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
            else:
                particle.draw(self.screen)
                
    def handle_menu_input(self, event):
        """Gère les entrées du menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % len(self.menu_buttons)
                if self.menu_sound:
                    self.menu_sound.play()
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % len(self.menu_buttons)
                if self.menu_sound:
                    self.menu_sound.play()
            elif event.key == pygame.K_RETURN:
                action = self.menu_buttons[self.menu_selection].action
                self.execute_menu_action(action)
            elif event.key == pygame.K_ESCAPE:
                self.running = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu_buttons:
                if button.is_clicked(mouse_pos, event.button == 1):
                    self.execute_menu_action(button.action)
                    
    def execute_menu_action(self, action):
        """Exécute une action du menu"""
        if action == "play":
            self.state = GameState.PLAYING
            self.reset_game()
        elif action == "solutions":
            if self.all_solutions:
                self.state = GameState.PLAYING
                self.current_solution_index = 0
                self.current_solution = self.all_solutions[0][0]
                self.reset_game()
        elif action == "options":
            self.state = GameState.SETTINGS
        elif action == "quit":
            self.running = False
            
    def handle_game_input(self, event):
        """Gère les entrées du jeu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            elif event.key == pygame.K_SPACE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for button in self.game_buttons:
                if button.is_clicked(mouse_pos, event.button == 1):
                    self.execute_game_action(button.action)
                    
            if len(self.all_solutions) > 1:
                for button in self.nav_buttons:
                    if button.is_clicked(mouse_pos, event.button == 1):
                        self.execute_nav_action(button.action)
                        
    def execute_game_action(self, action):
        """Exécute une action du jeu"""
        if action == "menu":
            self.state = GameState.MENU
        elif action == "pause":
            self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING
        elif action == "restart":
            self.reset_game()
        elif action == "speed_up":
            self.animation_speed = max(50, self.animation_speed - 50)
        elif action == "speed_down":
            self.animation_speed = min(2000, self.animation_speed + 50)
        elif action == "toggle_grid":
            self.show_grid = not self.show_grid
        elif action == "toggle_rotation":
            self.auto_rotate = not self.auto_rotate
            
    def execute_nav_action(self, action):
        """Exécute une action de navigation"""
        if action == "prev_solution":
            self.current_solution_index = (self.current_solution_index - 1) % len(self.all_solutions)
            self.current_solution = self.all_solutions[self.current_solution_index][0]
            self.reset_game()
        elif action == "next_solution":
            self.current_solution_index = (self.current_solution_index + 1) % len(self.all_solutions)
            self.current_solution = self.all_solutions[self.current_solution_index][0]
            self.reset_game()
            
    def reset_game(self):
        """Réinitialise le jeu"""
        self.current_move_index = 0
        self.last_move_time = 0
        self.state = GameState.PLAYING
        self.particles.clear()
        self.screen_shake = 0
        self.start_time = time.time()
        self.combo = 0
        self.moves_count = 0
        
    def update(self):
        """Met à jour l'état du jeu"""
        self.menu_time += 0.02
        
        if self.screen_shake > 0:
            self.screen_shake -= 0.3
            
        if self.state == GameState.PLAYING and self.current_solution:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_move_time > self.animation_speed:
                if self.current_move_index < len(self.current_solution.path) - 1:
                    self.current_move_index += 1
                    self.last_move_time = current_time
                    self.moves_count += 1
                    
                    pos = self.current_solution.path[self.current_move_index]
                    x = BOARD_OFFSET_X + pos[0] * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_OFFSET_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
                    self.create_explosion(x, y, Colors.PRIMARY_BLUE, 12)
                    self.screen_shake = 3
                    
                    if self.move_sound:
                        self.move_sound.play()
                        
                    self.combo += 1
                else:
                    self.state = GameState.SOLUTION_COMPLETE
                    if self.complete_sound:
                        self.complete_sound.play()
                    self.create_explosion(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                                        Colors.GOLD, 80)
                    
    def draw(self):
        """Dessine tout"""
        if self.state == GameState.MENU:
            self.draw_menu()
        else:
            self.draw_background()
            self.draw_board()
            self.draw_path()
            self.draw_knight()
            self.draw_ui()
            
        self.update_particles()
        
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if self.state == GameState.MENU:
                    self.handle_menu_input(event)
                else:
                    self.handle_game_input(event)
                    
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = KnightTourGame()
    game.run()