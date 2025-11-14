# Colors
import pygame
import sys
try:
    import vlc  # type: ignore
    _VLC_AVAILABLE = True
except Exception:
    vlc = None
    _VLC_AVAILABLE = False
import time
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
LIGHT_BLUE = (100, 160, 210)
GREEN = (50, 180, 100)
RED = "red"

# Fonts
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_verysmall = pygame.font.SysFont(None, 24)
font_supersmall = pygame.font.SysFont(None, 16)

# Base Screen Class
class Screen:
    def __init__(self, manager):
        self.manager = manager  # Reference to the ScreenManager

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# Title Screen
class TitleScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Title_Card.mp3", volume=80)
        
        # Bouncing squares state array
        self.squares = []

        # Base square variables (for preservation)
        self.squares.append({
            'size': 40,
            'pos': [50.0, 50.0],
            'vel': [2.4, 1.8],
            'color': (200, 60, 60),
        })
        # Add in 14 more random squares for 15 total
        for _ in range(14):
            size = random.randint(24, 68)
            x = random.uniform(0, WIDTH - size)
            y = random.uniform(0, HEIGHT - size)
            vx = random.choice([-1, 1]) * random.uniform(1.2, 3.0)
            vy = random.choice([-1, 1]) * random.uniform(1.0, 2.8)
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.squares.append({
                'size': size,
                'pos': [x, y],
                'vel': [vx, vy],
                'color': color,
            })

    def update(self):
        # Update all squares
        for s in self.squares:
            s['pos'][0] += s['vel'][0]
            s['pos'][1] += s['vel'][1]

            # Bounce off left/right
            if s['pos'][0] <= 0:
                s['pos'][0] = 0
                s['vel'][0] = abs(s['vel'][0])
                # changed color on bounce
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            elif s['pos'][0] + s['size'] >= WIDTH:
                s['pos'][0] = WIDTH - s['size']
                s['vel'][0] = -abs(s['vel'][0])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

            # Bounce off top/bottom
            if s['pos'][1] <= 0:
                s['pos'][1] = 0
                s['vel'][1] = abs(s['vel'][1])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            elif s['pos'][1] + s['size'] >= HEIGHT:
                s['pos'][1] = HEIGHT - s['size']
                s['vel'][1] = -abs(s['vel'][1])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.soundtrack.stop()
                self.soundtrack = play_mp3("royalty_free_music/Palismanto_Stinger.mp3", volume=80)
                time.sleep(2.2)
                self.manager.go_to(MainMenuScreen(self.manager))

    def draw(self, surface):
        surface.fill(WHITE)
        # Draw all bouncing squares
        for s in self.squares:
            pygame.draw.rect(surface, s['color'],
                             (int(s['pos'][0]), int(s['pos'][1]), s['size'], s['size']))
        title_text = font_large.render("Palismanto: The RTS Battling Game", True, BLACK)
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_BLUE if self.button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.button_rect)
        button_text = font_small.render("Start Game", True, WHITE)
        surface.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                   self.button_rect.centery - button_text.get_height() // 2))
    # (squares already drawn behind UI)


# Main Menu Screen
class MainMenuScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Menu.mp3", volume=80)

        # Animated bars at the bottom
        self.bar_count = 8
        self.bar_width = max(8, WIDTH // (self.bar_count * 3))
        self.bar_spacing = self.bar_width // 2
        self.bar_max_height = 120
        # Per-bar attributes (phase, speed, color)
        self.bars = []
        for i in range(self.bar_count):
            phase = i * (2 * math.pi / max(1, self.bar_count))
            speed = 0.8 + (i % 4) * 0.25
            c = pygame.Color(0, 0, 0)
            c.hsva = (i * (360 / max(1, self.bar_count)), 75, 85, 100)
            color = (c.r, c.g, c.b)
            self.bars.append({'phase': phase, 'speed': speed, 'color': color})
        self.bar_time = 0.0

    def update(self):
        # advance animation time for bars
        self.bar_time += 0.06

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(GameScreen(self.manager))  # Go to the game screen
            self.soundtrack.stop()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.manager.go_to(BattleScreen(self.manager))  # Go to the battle screen
            self.soundtrack.stop()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.go_to(TitleScreen(self.manager))  # Go back to title
            self.soundtrack.stop()

    def draw(self, surface):
        surface.fill(GREEN)
        text = font_large.render("Welcome To A New Adventure!", True, WHITE)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 6 - text.get_height() // 6))
        
        info = font_small.render("Make a selection:", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 50))

        info = font_verysmall.render("Press ENTER to start the adventure!", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 100))

        info = font_verysmall.render("Press SPACE to test out the battle feature?", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 150))

        info = font_verysmall.render("Or press ESC to return...", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 200))

        # Draw animated multicolored bars at the bottom
        total_width = self.bar_count * self.bar_width + (self.bar_count - 1) * self.bar_spacing
        start_x = (WIDTH - total_width) // 2
        bottom_margin = 12
        for i, bar in enumerate(self.bars):
            h = (math.sin(self.bar_time * bar['speed'] + bar['phase']) + 1) / 2
            height = int(h * self.bar_max_height)
            x = start_x + i * (self.bar_width + self.bar_spacing)
            y = HEIGHT - bottom_margin - height
            rect = pygame.Rect(x, y, self.bar_width, height)
            pygame.draw.rect(surface, bar['color'], rect)


# Game Screen
class GameScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Adventure.mp3", volume=80)
        
        # Grid setup
        self.grid_size = 40  # Size of each grid cell in pixels
        self.grid_width = WIDTH // self.grid_size
        self.grid_height = HEIGHT // self.grid_size
        
        # Player setup
        self.player_x = self.grid_width // 2  # Start in center (grid coordinates)
        self.player_y = self.grid_height // 2
        self.player_color = (0, 100, 255)
        # Customizable player name
        self.player_name = "The Hero"
        
        # Movement tracking (for smooth grid-based movement)
        self.can_move = True

        # Enemies: three red squares with their own stats
        # Each enemy uses grid coords (x,y) and moves every few frames
        self.enemies = []
        # Example per-enemy stats (health, damage, heal). Tweak as desired.
        enemy_templates = [
            {'name': 'Imp', 'hp': 30, 'damage': 6, 'heal': 6},
            {'name': 'Boss', 'hp': 55, 'damage': 15, 'heal': 10},
            {'name': 'Peon', 'hp': 20, 'damage': 4, 'heal': 6},
            {'name': 'Orc', 'hp': 40, 'damage': 8, 'heal': 8},
        ]
        # Place enemies at distinct positions
        positions = [
            (1, 1),
            (self.grid_width - 2, 2),
            (3, self.grid_height - 3)
        ]
        for i in range(3):
            ex, ey = positions[i]
            # movement direction - grid steps
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            # ensure not (0,0)
            if dx == 0 and dy == 0:
                dx = 1
            tpl = enemy_templates[i]
            self.enemies.append({
                'x': ex,
                'y': ey,
                'dx': dx,
                'dy': dy,
                'name': tpl.get('name', f'Enemy{i+1}'),
                'hp': tpl['hp'],
                'damage': tpl['damage'],
                'heal': tpl['heal'],
                'move_timer': random.randint(6, 18)  # frames until move
            })

        # Keep templates and spawn timing on the screen for dynamic spawning
        self.enemy_templates = enemy_templates
        self.spawn_timer = 0
        self.spawn_interval = 600  # frames between spawn attempts (~10s at 60fps)
        self.max_enemies = 8  # cap total enemies on the map

    def spawn_enemy(self):
        """Attempt to spawn a new enemy at a random free grid tile."""
        if len(self.enemies) >= self.max_enemies:
            return

        # Choose a random template
        tpl = random.choice(self.enemy_templates)

        # Try to find a free position (avoid player and existing enemies)
        attempts = 0
        while attempts < 50:
            rx = random.randint(0, self.grid_width - 1)
            ry = random.randint(0, self.grid_height - 1)
            # avoid spawning on player
            if rx == self.player_x and ry == self.player_y:
                attempts += 1
                continue
            collision = False
            for e in self.enemies:
                if e['x'] == rx and e['y'] == ry:
                    collision = True
                    break
            if collision:
                attempts += 1
                continue

            # Place enemy
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            if dx == 0 and dy == 0:
                dx = 1
            new_enemy = {
                'x': rx,
                'y': ry,
                'dx': dx,
                'dy': dy,
                'name': tpl.get('name', 'Enemy'),
                'hp': tpl['hp'],
                'damage': tpl['damage'],
                'heal': tpl['heal'],
                'move_timer': random.randint(6, 18)
            }
            self.enemies.append(new_enemy)
            return
        # if we exit loop, couldn't find a spot this tick; just skip

    def update(self):
        # Update enemies movement
        for e in self.enemies:
            e['move_timer'] -= 1
            if e['move_timer'] <= 0:
                # attempt move
                new_x = e['x'] + e['dx']
                new_y = e['y'] + e['dy']
                # if out of bounds, pick a new direction
                if new_x < 0 or new_x >= self.grid_width or new_y < 0 or new_y >= self.grid_height:
                    e['dx'] = random.choice([-1, 0, 1])
                    e['dy'] = random.choice([-1, 0, 1])
                    if e['dx'] == 0 and e['dy'] == 0:
                        e['dx'] = 1
                    e['move_timer'] = random.randint(6, 18)
                else:
                    e['x'] = new_x
                    e['y'] = new_y
                    # occasionally change direction
                    if random.random() < 0.25:
                        e['dx'] = random.choice([-1, 0, 1])
                        e['dy'] = random.choice([-1, 0, 1])
                        if e['dx'] == 0 and e['dy'] == 0:
                            e['dx'] = 1
                    e['move_timer'] = random.randint(6, 18)

        # Check for collisions (player steps onto an enemy)
        for e in self.enemies:
            if e['x'] == self.player_x and e['y'] == self.player_y:
                # start battle with this enemy's stats
                self.soundtrack.stop()
                # pass a reference to this GameScreen and the enemy index so BattleScreen
                # can remove the enemy when defeated and return to the map
                enemy_index = self.enemies.index(e)
                self.manager.go_to(BattleScreen(
                    self.manager,
                    player_health=50,
                    player_damage=15,
                    player_heal=10,
                    enemy_health=e['hp'],
                    enemy_damage=e['damage'],
                    enemy_heal=e['heal'],
                    is_boss=(e['hp'] > 50),
                    origin_screen=self,
                    origin_enemy_index=enemy_index,
                    player_name=self.player_name,
                    enemy_name=e['name']
                ))
                return

        # Handle timed spawning of additional enemies
        if self.spawn_timer <= 0:
            # Attempt to spawn and reset timer
            self.spawn_enemy()
            self.spawn_timer = self.spawn_interval
        else:
            self.spawn_timer -= 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.can_move:
            # Arrow key movement
            if event.key == pygame.K_UP:
                if self.player_y > 0:
                    self.player_y -= 1
            elif event.key == pygame.K_DOWN:
                if self.player_y < self.grid_height - 1:
                    self.player_y += 1
            elif event.key == pygame.K_LEFT:
                if self.player_x > 0:
                    self.player_x -= 1
            elif event.key == pygame.K_RIGHT:
                if self.player_x < self.grid_width - 1:
                    self.player_x += 1
            
            # ESC to return to main menu
            if event.key == pygame.K_ESCAPE:
                self.soundtrack.stop()
                self.manager.go_to(MainMenuScreen(self.manager))

    def draw(self, surface):
        surface.fill(BLUE)
        
        # Draw grid
        for x in range(0, WIDTH, self.grid_size):
            pygame.draw.line(surface, BLACK, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, self.grid_size):
            pygame.draw.line(surface, BLACK, (0, y), (WIDTH, y), 1)
        
        # Draw enemy squares (red) on the grid
        for e in self.enemies:
            ex_screen = e['x'] * self.grid_size
            ey_screen = e['y'] * self.grid_size
            er = pygame.Rect(ex_screen + 4, ey_screen + 4, self.grid_size - 8, self.grid_size - 8)
            # small name label
            name_text = font_supersmall.render(str(e['name']), True, WHITE)
            
            # Changes box colours for boss enemies because they are awesome!
            if str(e['name']) is "Boss":
                pygame.draw.rect(surface, (200, 40, 40), er)
            else:
                pygame.draw.rect(surface, (100, 100, 40), er)
            surface.blit(name_text, (ex_screen + 6, ey_screen + 6))

        # Draw player character (as a square)
        player_screen_x = self.player_x * self.grid_size
        player_screen_y = self.player_y * self.grid_size
        player_rect = pygame.Rect(player_screen_x + 2, player_screen_y + 2, 
                                  self.grid_size - 4, self.grid_size - 4)
        pygame.draw.rect(surface, self.player_color, player_rect)
        
        # Draw instructions
        info = font_verysmall.render("Use arrow keys to move - ESC to return to menu", True, WHITE)
        surface.blit(info, (10, 10))


# Button class for UI
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def draw(self, surface, font):
        color = tuple(min(c + 50, 255) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


# Battle Screen
class BattleScreen(Screen):
    def __init__(self, manager, player_health=50, player_damage=15, player_heal=10,
                 enemy_health=50, enemy_damage=6, enemy_heal=12, is_boss=False,
                 origin_screen=None, origin_enemy_index=None, player_name=None, enemy_name=None):
        super().__init__(manager)

        if is_boss:
            self.soundtrack = play_mp3("royalty_free_music/Palismanto_Boss.mp3", volume=80)
        else:
            self.soundtrack = play_mp3("royalty_free_music/Palismanto_Battle.mp3", volume=80)
        
        # Customizable stats
        self.player_max_health = player_health
        self.enemy_max_health = enemy_health
        self.player_damage = player_damage
        self.player_heal_amount = player_heal
        self.enemy_damage = enemy_damage
        self.enemy_heal_amount = enemy_heal
        # Names
        self.player_name = player_name if player_name is not None else "Player"
        self.enemy_name = enemy_name if enemy_name is not None else "Enemy"
        
        # Current health
        self.player_health = player_health
        self.enemy_health = enemy_health
        
        # Battle state
        self.player_turn = True
        self.battle_log = "Battle Start! Choose your action."
        self.action_timer = 0
        self.battle_over = False
        self.winner = None
        # Optional origin info: where to return and which enemy to remove on victory
        self.origin_screen = origin_screen
        self.origin_enemy_index = origin_enemy_index

        # Create buttons for player actions
        button_width = 150
        button_height = 50
        button_y = HEIGHT - 100
        self.attack_button = Button(50, button_y, button_width, button_height, "ATTACK", (200, 50, 50), BLACK)
        self.heal_button = Button(250, button_y, button_width, button_height, "HEAL", (50, 200, 100), BLACK)
        self.plead_button = Button(450, button_y, button_width, button_height, "PLEAD", (200, 50, 200), BLACK)
        self.buttons = [self.attack_button, self.heal_button, self.plead_button]
    
    def enemy_turn(self):
        """Enemy decides to attack or heal"""
        import random
        if self.enemy_health < self.enemy_max_health * 0.4:
            # Heal if low on health
            self.perform_enemy_heal()
        else:
            # Attack by default
            self.perform_enemy_attack()
    
    def perform_player_attack(self):
        """Player attacks enemy"""
        self.enemy_health -= self.player_damage
        self.battle_log = f"You attacked! Enemy took {self.player_damage} damage!"
        self.action_timer = 180  # Display for 3 seconds
        self.check_battle_end()
        self.player_turn = False
    
    def perform_player_heal(self):
        """Player heals themselves"""
        self.player_health = min(self.player_health + self.player_heal_amount, self.player_max_health)
        self.battle_log = f"You healed for {self.player_heal_amount} HP!"
        self.action_timer = 180
        self.player_turn = False

    def perform_player_plead(self):
        """Player begs for mercy (funny)"""
        self.battle_log = f"You begged for mercy! The {self.enemy_name} laughs."
        self.action_timer = 180
        self.player_turn = False
    
    def perform_enemy_attack(self):
        """Enemy attacks player"""
        self.player_health -= self.enemy_damage
        self.battle_log = f"Enemy attacked! You took {self.enemy_damage} damage!"
        self.action_timer = 180
        self.check_battle_end()
        self.player_turn = True
    
    def perform_enemy_heal(self):
        """Enemy heals themselves"""
        self.enemy_health = min(self.enemy_health + self.enemy_heal_amount, self.enemy_max_health)
        self.battle_log = f"Enemy healed for {self.enemy_heal_amount} HP!"
        self.action_timer = 180
        self.player_turn = True
    
    def check_battle_end(self):
        """Check if battle is over"""
        if self.player_health <= 0:
            self.battle_over = True
            self.winner = "Enemy"
            self.battle_log = f"{self.player_name} has been defeated! Press ESC to return."
        elif self.enemy_health <= 0:
            self.battle_over = True
            self.winner = "Player"
            self.battle_log = f"Victory! You defeated {self.enemy_name}! Returning to map..."
            # If we have an origin map and enemy index, remove the enemy and return
            if self.origin_screen is not None and self.origin_enemy_index is not None:
                try:
                    # get the enemy position so we can place the player there
                    enemy_obj = self.origin_screen.enemies[self.origin_enemy_index]
                    enemy_pos_x = enemy_obj['x']
                    enemy_pos_y = enemy_obj['y']
                    # remove the enemy from the map
                    del self.origin_screen.enemies[self.origin_enemy_index]
                    # resume the map soundtrack and return
                    # place the player at the enemy's former position
                    self.origin_screen.player_x = enemy_pos_x
                    self.origin_screen.player_y = enemy_pos_y
                    self.soundtrack.stop()
                    self.origin_screen.soundtrack = play_mp3("royalty_free_music/Palismanto_Adventure.mp3", volume=80)
                    # switch back to the origin screen
                    self.manager.go_to(self.origin_screen)
                except Exception:
                    # If any error occurs, just update the message and let user press ESC
                    self.battle_log = "Victory! Press ESC to return."

    def update(self):
        if self.action_timer > 0:
            self.action_timer -= 1
        
        # Enemy turn after action timer expires
        if self.action_timer == 0 and not self.player_turn and not self.battle_over:
            self.enemy_turn()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.player_turn and not self.battle_over:
                    if self.attack_button.is_clicked(event.pos):
                        self.perform_player_attack()
                    elif self.heal_button.is_clicked(event.pos):
                        self.perform_player_heal()
                    elif self.plead_button.is_clicked(event.pos):
                        self.perform_player_plead()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.go_to(MainMenuScreen(self.manager))
                self.soundtrack.stop()
            
            # Keyboard shortcuts
            if self.player_turn and not self.battle_over:
                if event.key == pygame.K_a:
                    self.perform_player_attack()
                elif event.key == pygame.K_h:
                    self.perform_player_heal()
                elif event.key == pygame.K_p:
                    self.perform_player_plead()

    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw title
        title = font_small.render("BATTLE!", True, WHITE)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        
        # Draw player section
        player_label = font_verysmall.render(self.player_name, True, WHITE)
        surface.blit(player_label, (50, 80))
        
        # Draw player health bar
        health_bar_width = 150
        health_bar_height = 20
        health_bar_x = 50
        health_bar_y = 110
        
        # Background
        pygame.draw.rect(surface, (100, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        # Health
        health_ratio = self.player_health / self.player_max_health
        pygame.draw.rect(surface, (0, 200, 0), (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(surface, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        
        # Health text
        health_text = font_verysmall.render(f"{self.player_health}/{self.player_max_health}", True, WHITE)
        surface.blit(health_text, (health_bar_x + 55, health_bar_y + 2))
        
        # Draw player stats
        player_stats = font_verysmall.render(f"DMG: {self.player_damage} | HEAL: {self.player_heal_amount}", True, WHITE)
        surface.blit(player_stats, (50, 140))
        
        # Draw enemy section
        enemy_label = font_verysmall.render(self.enemy_name, True, WHITE)
        surface.blit(enemy_label, (WIDTH - 200, 80))
        
        # Draw enemy health bar
        health_bar_x = WIDTH - 200
        pygame.draw.rect(surface, (100, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        health_ratio = self.enemy_health / self.enemy_max_health
        pygame.draw.rect(surface, (0, 200, 0), (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(surface, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        
        # Health text
        health_text = font_verysmall.render(f"{self.enemy_health}/{self.enemy_max_health}", True, WHITE)
        surface.blit(health_text, (health_bar_x + 55, health_bar_y + 2))
        
        # Draw enemy stats
        enemy_stats = font_verysmall.render(f"DMG: {self.enemy_damage} | HEAL: {self.enemy_heal_amount}", True, WHITE)
        surface.blit(enemy_stats, (WIDTH - 200, 140))
        
        # Draw battle log
        log_text = font_verysmall.render(self.battle_log, True, WHITE)
        surface.blit(log_text, (WIDTH // 2 - log_text.get_width() // 2, HEIGHT // 2 - 50))
        
        # Draw turn indicator
        if not self.battle_over:
            if self.player_turn:
                turn_text = font_verysmall.render("YOUR TURN", True, (0, 255, 0))
            else:
                turn_text = font_verysmall.render("ENEMY'S TURN", True, (255, 0, 0))
            surface.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT // 2 + 30))
        
        # Draw buttons if it's player's turn
        if self.player_turn and not self.battle_over:
            self.attack_button.draw(surface, font_small)
            self.heal_button.draw(surface, font_small)
            self.plead_button.draw(surface, font_small)
            
            # Draw keyboard shortcuts hint
            hint = font_verysmall.render("(A) Attack | (H) Heal | (P) Plead | Click or Press Keys", True, WHITE)
            surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 30))
        
        # Draw exit hint
        if self.battle_over:
            exit_text = font_verysmall.render("Press ESC to return to menu", True, WHITE)
            surface.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 30))


# Screen Manager
class ScreenManager:
    def __init__(self):
        self.current_screen = TitleScreen(self)

    def go_to(self, screen):
        self.current_screen = screen

    def handle_event(self, event):
        self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def draw(self, surface):
        self.current_screen.draw(surface)

# Function to play mp3 
def play_mp3(file_path, volume=100):
    """
    Plays an MP3 file in a non-blocking infinite loop using VLC.
    The music will automatically restart when it finishes.
    
    - file_path (str): Path to the MP3 file
    - volume (int): Volume (0–100)
    
    Returns player (vlc.MediaPlayer), the VLC player object, so you can stop it later
    """
    # If vlc is not available, return a dummy object with a stop() method
    if not _VLC_AVAILABLE:
        class DummyPlayer:
            def play(self):
                print(f"[INFO] vlc not available - would play: {file_path}")

            def stop(self):
                print(f"[INFO] vlc not available - stop called for: {file_path}")

        dp = DummyPlayer()
        dp.play()
        return dp

    # Create VLC instance with infinite looping enabled
    instance = vlc.Instance("--input-repeat=-1")  # -1 = infinite loop
    try:
        # Some vlc builds don't expose vlc.Instance.vlm_set_loop; guard it
        instance.vlm_set_loop(file_path, True)
    except Exception:
        pass
    player = instance.media_player_new()

    # Load file and set up
    media = instance.media_new(file_path)
    player.set_media(media)
    try:
        player.audio_set_volume(volume)
    except Exception:
        pass

    # Play the music in a non-blocking infinite loop
    player.play()

    return player