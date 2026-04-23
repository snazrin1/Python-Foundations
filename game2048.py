"""
╔══════════════════════════════════════════╗
║            2048 PUZZLE GAME              ║
║   Arrow Keys to move | U to Undo        ║
║   R to Restart | ESC to Quit             ║
╚══════════════════════════════════════════╝

Requirements: pip install pygame
"""

import pygame
import sys
import random
import copy
import math

# ─── INIT ────────────────────────────────────────────────
pygame.init()

# ─── CONSTANTS ───────────────────────────────────────────
GRID_SIZE = 4
CELL_SIZE = 120
CELL_PAD = 12
HEADER_HEIGHT = 140
BORDER_RADIUS = 12

BOARD_ORIGIN_X = CELL_PAD
BOARD_ORIGIN_Y = HEADER_HEIGHT
BOARD_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PAD
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PAD

WIN_WIDTH = BOARD_WIDTH
WIN_HEIGHT = HEADER_HEIGHT + BOARD_HEIGHT + CELL_PAD

FPS = 60
ANIM_SPEED = 18          # tiles per frame (slide)
ANIM_SPAWN_FRAMES = 8    # pop-in frames
ANIM_MERGE_FRAMES = 8    # bounce frames

# ─── COLORS ──────────────────────────────────────────────
BG_COLOR        = (250, 248, 239)
BOARD_BG        = (187, 173, 160)
EMPTY_CELL      = (205, 193, 180)
DARK_TEXT        = (119, 110, 101)
LIGHT_TEXT       = (249, 246, 242)
HEADER_BTN      = (143, 122, 102)
HEADER_BTN_HOVER = (170, 148, 128)

TILE_COLORS = {
    2:    ((238, 228, 218), DARK_TEXT),
    4:    ((237, 224, 200), DARK_TEXT),
    8:    ((242, 177, 121), LIGHT_TEXT),
    16:   ((245, 149, 99),  LIGHT_TEXT),
    32:   ((246, 124, 95),  LIGHT_TEXT),
    64:   ((246, 94,  59),  LIGHT_TEXT),
    128:  ((237, 207, 114), LIGHT_TEXT),
    256:  ((237, 204, 97),  LIGHT_TEXT),
    512:  ((237, 200, 80),  LIGHT_TEXT),
    1024: ((237, 197, 63),  LIGHT_TEXT),
    2048: ((237, 194, 46),  LIGHT_TEXT),
}
TILE_SUPER = ((60, 58, 50), LIGHT_TEXT)

# ─── FONTS ───────────────────────────────────────────────
FONT_TILE_BIG   = pygame.font.SysFont("Arial", 48, bold=True)
FONT_TILE_MED   = pygame.font.SysFont("Arial", 40, bold=True)
FONT_TILE_SM    = pygame.font.SysFont("Arial", 32, bold=True)
FONT_TILE_XS    = pygame.font.SysFont("Arial", 26, bold=True)
FONT_TITLE      = pygame.font.SysFont("Arial", 52, bold=True)
FONT_SCORE_LBL  = pygame.font.SysFont("Arial", 14, bold=True)
FONT_SCORE_VAL  = pygame.font.SysFont("Arial", 26, bold=True)
FONT_BTN        = pygame.font.SysFont("Arial", 16, bold=True)
FONT_MSG        = pygame.font.SysFont("Arial", 54, bold=True)
FONT_SUB        = pygame.font.SysFont("Arial", 20)
FONT_HINT       = pygame.font.SysFont("Arial", 13)

# ─── HELPERS ─────────────────────────────────────────────
def cell_rect(r, c):
    x = CELL_PAD + c * (CELL_SIZE + CELL_PAD)
    y = HEADER_HEIGHT + CELL_PAD + r * (CELL_SIZE + CELL_PAD)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

def get_tile_font(val):
    if val < 100:
        return FONT_TILE_BIG
    elif val < 1000:
        return FONT_TILE_MED
    elif val < 10000:
        return FONT_TILE_SM
    else:
        return FONT_TILE_XS

def draw_rounded_rect(surf, color, rect, radius):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def lerp(a, b, t):
    return a + (b - a) * t

# ─── ANIMATION OBJECTS ───────────────────────────────────
class SlideTile:
    """Animates a tile sliding from one cell to another."""
    def __init__(self, val, from_rc, to_rc):
        self.val = val
        fr = cell_rect(*from_rc)
        tr = cell_rect(*to_rc)
        self.sx, self.sy = fr.x, fr.y
        self.ex, self.ey = tr.x, tr.y
        self.x, self.y = float(self.sx), float(self.sy)
        self.done = False

    def update(self):
        dx = self.ex - self.x
        dy = self.ey - self.y
        dist = math.hypot(dx, dy)
        step = ANIM_SPEED * (CELL_SIZE + CELL_PAD) / FPS * 4
        if dist <= step:
            self.x, self.y = float(self.ex), float(self.ey)
            self.done = True
        else:
            self.x += dx / dist * step
            self.y += dy / dist * step

    def draw(self, surf):
        rect = pygame.Rect(int(self.x), int(self.y), CELL_SIZE, CELL_SIZE)
        bg, fg = TILE_COLORS.get(self.val, TILE_SUPER)
        draw_rounded_rect(surf, bg, rect, BORDER_RADIUS)
        font = get_tile_font(self.val)
        txt = font.render(str(self.val), True, fg)
        surf.blit(txt, txt.get_rect(center=rect.center))


class SpawnTile:
    """Pop-in animation for newly spawned tiles."""
    def __init__(self, val, rc):
        self.val = val
        self.rc = rc
        self.frame = 0
        self.total = ANIM_SPAWN_FRAMES
        self.done = False

    def update(self):
        self.frame += 1
        if self.frame >= self.total:
            self.done = True

    def draw(self, surf):
        t = min(self.frame / self.total, 1.0)
        scale = t
        rect = cell_rect(*self.rc)
        cx, cy = rect.center
        w = int(CELL_SIZE * scale)
        h = int(CELL_SIZE * scale)
        if w < 2:
            return
        r = pygame.Rect(0, 0, w, h)
        r.center = (cx, cy)
        bg, fg = TILE_COLORS.get(self.val, TILE_SUPER)
        draw_rounded_rect(surf, bg, r, max(2, int(BORDER_RADIUS * scale)))
        if scale > 0.5:
            font = get_tile_font(self.val)
            txt = font.render(str(self.val), True, fg)
            txt = pygame.transform.smoothscale(txt, (int(txt.get_width() * scale), int(txt.get_height() * scale)))
            surf.blit(txt, txt.get_rect(center=r.center))


class MergeTile:
    """Bounce animation for merged tiles."""
    def __init__(self, val, rc):
        self.val = val
        self.rc = rc
        self.frame = 0
        self.total = ANIM_MERGE_FRAMES
        self.done = False

    def update(self):
        self.frame += 1
        if self.frame >= self.total:
            self.done = True

    def draw(self, surf):
        t = min(self.frame / self.total, 1.0)
        # bounce: scale up then back to 1
        scale = 1.0 + 0.2 * math.sin(t * math.pi)
        rect = cell_rect(*self.rc)
        cx, cy = rect.center
        w = int(CELL_SIZE * scale)
        h = int(CELL_SIZE * scale)
        r = pygame.Rect(0, 0, w, h)
        r.center = (cx, cy)
        bg, fg = TILE_COLORS.get(self.val, TILE_SUPER)
        draw_rounded_rect(surf, bg, r, BORDER_RADIUS)
        font = get_tile_font(self.val)
        txt = font.render(str(self.val), True, fg)
        surf.blit(txt, txt.get_rect(center=r.center))


# ─── PARTICLE SYSTEM ────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.x, self.y = float(x), float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(15, 35)
        self.max_life = self.life
        self.color = color
        self.size = random.uniform(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def draw(self, surf):
        alpha = max(0, self.life / self.max_life)
        sz = max(1, int(self.size * alpha))
        c = tuple(int(ch * alpha) + int(250 * (1 - alpha)) for ch in self.color[:3])
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), sz)


# ─── GAME CLASS ──────────────────────────────────────────
class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.best = getattr(self, 'best', 0)
        self.history = []
        self.won = False
        self.game_over = False
        self.show_win_msg = False
        self.animations = []
        self.particles = []
        self.animating = False
        self.pending_spawns = []
        self.spawn_tile(count=2)

    def spawn_tile(self, count=1):
        empties = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        for _ in range(min(count, len(empties))):
            rc = random.choice(empties)
            empties.remove(rc)
            val = 4 if random.random() < 0.1 else 2
            self.grid[rc[0]][rc[1]] = val
            self.animations.append(SpawnTile(val, rc))

    def save_state(self):
        self.history.append((copy.deepcopy(self.grid), self.score))
        if len(self.history) > 50:
            self.history.pop(0)

    def undo(self):
        if self.history:
            self.grid, self.score = self.history.pop()
            self.game_over = False
            self.animations.clear()
            self.particles.clear()
            self.pending_spawns.clear()
            self.animating = False

    def compress(self, row):
        """Slide non-zero tiles to the left."""
        new = [v for v in row if v != 0]
        new += [0] * (GRID_SIZE - len(new))
        return new

    def merge(self, row):
        """Merge adjacent equal tiles (left)."""
        pts = 0
        merged_indices = []
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                pts += row[i]
                row[i+1] = 0
                merged_indices.append(i)
        return row, pts, merged_indices

    def move(self, direction):
        """Execute a move. Returns True if board changed."""
        self.save_state()
        old_grid = copy.deepcopy(self.grid)
        slide_anims = []
        merge_anims = []

        if direction == "left":
            for r in range(GRID_SIZE):
                row = list(self.grid[r])
                # track positions
                positions = [(r, c) for c in range(GRID_SIZE)]
                non_zero = [(row[c], positions[c]) for c in range(GRID_SIZE) if row[c] != 0]
                compressed = [v for v, _ in non_zero]
                compressed += [0] * (GRID_SIZE - len(compressed))
                # slide anims
                for idx, (val, orig_pos) in enumerate(non_zero):
                    dest = (r, idx)
                    if orig_pos != dest:
                        slide_anims.append(SlideTile(val, orig_pos, dest))
                self.grid[r] = compressed
                # merge
                merged_row, pts, mi = self.merge(list(self.grid[r]))
                self.score += pts
                for i in mi:
                    merge_anims.append(MergeTile(merged_row[i], (r, i)))
                    bg, _ = TILE_COLORS.get(merged_row[i], TILE_SUPER)
                    rect = cell_rect(r, i)
                    for _ in range(8):
                        self.particles.append(Particle(rect.centerx, rect.centery, bg))
                self.grid[r] = merged_row
                # second compress after merge
                self.grid[r] = self.compress(self.grid[r])

        elif direction == "right":
            for r in range(GRID_SIZE):
                row = list(self.grid[r])
                positions = [(r, c) for c in range(GRID_SIZE)]
                non_zero = [(row[c], positions[c]) for c in range(GRID_SIZE - 1, -1, -1) if row[c] != 0]
                compressed = [v for v, _ in non_zero]
                compressed += [0] * (GRID_SIZE - len(compressed))
                compressed.reverse()
                for idx, (val, orig_pos) in enumerate(non_zero):
                    dest = (r, GRID_SIZE - 1 - idx)
                    if orig_pos != dest:
                        slide_anims.append(SlideTile(val, orig_pos, dest))
                self.grid[r] = compressed
                rev = list(reversed(self.grid[r]))
                merged_row, pts, mi = self.merge(rev)
                self.score += pts
                for i in mi:
                    actual_c = GRID_SIZE - 1 - i
                    merge_anims.append(MergeTile(merged_row[i], (r, actual_c)))
                    bg, _ = TILE_COLORS.get(merged_row[i], TILE_SUPER)
                    rect = cell_rect(r, actual_c)
                    for _ in range(8):
                        self.particles.append(Particle(rect.centerx, rect.centery, bg))
                compressed_rev = self.compress(merged_row)
                self.grid[r] = list(reversed(compressed_rev))

        elif direction == "up":
            for c in range(GRID_SIZE):
                col = [self.grid[r][c] for r in range(GRID_SIZE)]
                positions = [(r, c) for r in range(GRID_SIZE)]
                non_zero = [(col[r], positions[r]) for r in range(GRID_SIZE) if col[r] != 0]
                compressed = [v for v, _ in non_zero]
                compressed += [0] * (GRID_SIZE - len(compressed))
                for idx, (val, orig_pos) in enumerate(non_zero):
                    dest = (idx, c)
                    if orig_pos != dest:
                        slide_anims.append(SlideTile(val, orig_pos, dest))
                for r in range(GRID_SIZE):
                    self.grid[r][c] = compressed[r]
                col2 = [self.grid[r][c] for r in range(GRID_SIZE)]
                merged_col, pts, mi = self.merge(col2)
                self.score += pts
                for i in mi:
                    merge_anims.append(MergeTile(merged_col[i], (i, c)))
                    bg, _ = TILE_COLORS.get(merged_col[i], TILE_SUPER)
                    rect = cell_rect(i, c)
                    for _ in range(8):
                        self.particles.append(Particle(rect.centerx, rect.centery, bg))
                compressed2 = self.compress(merged_col)
                for r in range(GRID_SIZE):
                    self.grid[r][c] = compressed2[r]

        elif direction == "down":
            for c in range(GRID_SIZE):
                col = [self.grid[r][c] for r in range(GRID_SIZE)]
                positions = [(r, c) for r in range(GRID_SIZE)]
                non_zero = [(col[r], positions[r]) for r in range(GRID_SIZE - 1, -1, -1) if col[r] != 0]
                compressed = [v for v, _ in non_zero]
                compressed += [0] * (GRID_SIZE - len(compressed))
                compressed.reverse()
                for idx, (val, orig_pos) in enumerate(non_zero):
                    dest = (GRID_SIZE - 1 - idx, c)
                    if orig_pos != dest:
                        slide_anims.append(SlideTile(val, orig_pos, dest))
                for r in range(GRID_SIZE):
                    self.grid[r][c] = compressed[r]
                rev = [self.grid[GRID_SIZE - 1 - r][c] for r in range(GRID_SIZE)]
                merged_col, pts, mi = self.merge(rev)
                self.score += pts
                for i in mi:
                    actual_r = GRID_SIZE - 1 - i
                    merge_anims.append(MergeTile(merged_col[i], (actual_r, c)))
                    bg, _ = TILE_COLORS.get(merged_col[i], TILE_SUPER)
                    rect = cell_rect(actual_r, c)
                    for _ in range(8):
                        self.particles.append(Particle(rect.centerx, rect.centery, bg))
                compressed_rev = self.compress(merged_col)
                for r in range(GRID_SIZE):
                    self.grid[GRID_SIZE - 1 - r][c] = compressed_rev[r]

        changed = self.grid != old_grid
        if not changed:
            self.history.pop()
            return False

        # queue animations
        self.animations = slide_anims + merge_anims
        self.animating = bool(slide_anims)
        self.pending_spawns = []

        # check win
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 2048 and not self.won:
                    self.won = True
                    self.show_win_msg = True

        # update best
        if self.score > self.best:
            self.best = self.score

        return True

    def check_game_over(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return False
                if c < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r][c+1]:
                    return False
                if r < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r+1][c]:
                    return False
        return True

    # ─── DRAWING ─────────────────────────────────────────
    def draw_header(self):
        # Title
        title = FONT_TITLE.render("2048", True, DARK_TEXT)
        self.screen.blit(title, (CELL_PAD, 12))

        # Score boxes
        for i, (label, val) in enumerate([("SCORE", self.score), ("BEST", self.best)]):
            bx = WIN_WIDTH - (i + 1) * 110 - CELL_PAD + (i * 6)
            by = 10
            box = pygame.Rect(bx, by, 104, 52)
            draw_rounded_rect(self.screen, BOARD_BG, box, 6)
            lbl = FONT_SCORE_LBL.render(label, True, (238, 228, 218))
            self.screen.blit(lbl, lbl.get_rect(centerx=box.centerx, top=box.top + 4))
            vtxt = FONT_SCORE_VAL.render(str(val), True, LIGHT_TEXT)
            self.screen.blit(vtxt, vtxt.get_rect(centerx=box.centerx, top=box.top + 22))

        # Buttons
        mouse = pygame.mouse.get_pos()
        btn_y = 75
        btn_w, btn_h = 100, 36

        # New Game button
        self.btn_new = pygame.Rect(WIN_WIDTH - CELL_PAD - btn_w, btn_y, btn_w, btn_h)
        hover = self.btn_new.collidepoint(mouse)
        draw_rounded_rect(self.screen, HEADER_BTN_HOVER if hover else HEADER_BTN, self.btn_new, 6)
        t = FONT_BTN.render("New Game", True, LIGHT_TEXT)
        self.screen.blit(t, t.get_rect(center=self.btn_new.center))

        # Undo button
        self.btn_undo = pygame.Rect(WIN_WIDTH - CELL_PAD - btn_w * 2 - 8, btn_y, btn_w, btn_h)
        hover = self.btn_undo.collidepoint(mouse)
        draw_rounded_rect(self.screen, HEADER_BTN_HOVER if hover else HEADER_BTN, self.btn_undo, 6)
        t = FONT_BTN.render("Undo", True, LIGHT_TEXT)
        self.screen.blit(t, t.get_rect(center=self.btn_undo.center))

        # Hints
        hint = FONT_HINT.render("Arrow Keys: Move  |  U: Undo  |  R: Restart  |  ESC: Quit", True, (160, 150, 140))
        self.screen.blit(hint, hint.get_rect(centerx=WIN_WIDTH // 2, top=HEADER_HEIGHT - 22))

    def draw_board(self):
        board_rect = pygame.Rect(0, HEADER_HEIGHT, WIN_WIDTH, WIN_HEIGHT - HEADER_HEIGHT)
        draw_rounded_rect(self.screen, BOARD_BG, board_rect, BORDER_RADIUS)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                rect = cell_rect(r, c)
                draw_rounded_rect(self.screen, EMPTY_CELL, rect, BORDER_RADIUS)

    def draw_tiles(self):
        # During slide animation, don't draw static tiles that are moving
        sliding_from = set()
        if self.animating:
            for a in self.animations:
                if isinstance(a, SlideTile) and not a.done:
                    # suppress drawing at destination during slide
                    pass

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                if val == 0:
                    continue
                rect = cell_rect(r, c)
                bg, fg = TILE_COLORS.get(val, TILE_SUPER)
                draw_rounded_rect(self.screen, bg, rect, BORDER_RADIUS)
                font = get_tile_font(val)
                txt = font.render(str(val), True, fg)
                self.screen.blit(txt, txt.get_rect(center=rect.center))

    def draw_overlay(self, text, sub, color, alpha=160):
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT - HEADER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*color, alpha))
        self.screen.blit(overlay, (0, HEADER_HEIGHT))
        msg = FONT_MSG.render(text, True, DARK_TEXT if color == (255, 255, 255) else LIGHT_TEXT)
        self.screen.blit(msg, msg.get_rect(center=(WIN_WIDTH // 2, HEADER_HEIGHT + BOARD_HEIGHT // 2 - 20)))
        sub_txt = FONT_SUB.render(sub, True, DARK_TEXT if color == (255, 255, 255) else (220, 220, 220))
        self.screen.blit(sub_txt, sub_txt.get_rect(center=(WIN_WIDTH // 2, HEADER_HEIGHT + BOARD_HEIGHT // 2 + 25)))

    # ─── MAIN LOOP ───────────────────────────────────────
    def run(self):
        running = True
        spawn_pending = False

        while running:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(self, 'btn_new') and self.btn_new.collidepoint(event.pos):
                        self.reset()
                        continue
                    if hasattr(self, 'btn_undo') and self.btn_undo.collidepoint(event.pos):
                        self.undo()
                        continue
                    if self.show_win_msg:
                        self.show_win_msg = False
                        continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if self.show_win_msg:
                        self.show_win_msg = False
                        continue
                    if self.animating:
                        continue

                    if event.key == pygame.K_r:
                        self.reset()
                        continue
                    if event.key == pygame.K_u:
                        self.undo()
                        continue

                    if self.game_over:
                        continue

                    direction = None
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        direction = "down"

                    if direction:
                        changed = self.move(direction)
                        if changed:
                            spawn_pending = True

            # Update animations
            all_slides_done = True
            for a in self.animations:
                a.update()
                if isinstance(a, SlideTile) and not a.done:
                    all_slides_done = False

            if self.animating and all_slides_done:
                self.animating = False
                if spawn_pending:
                    self.spawn_tile()
                    spawn_pending = False
                    if self.check_game_over():
                        self.game_over = True

            self.animations = [a for a in self.animations if not a.done]

            # Update particles
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.life > 0]

            # ─── DRAW ────────────────────────────────────
            self.screen.fill(BG_COLOR)
            self.draw_header()
            self.draw_board()

            if not self.animating:
                self.draw_tiles()

            # Draw animations on top
            if self.animating:
                # draw static tiles (non-animated)
                self.draw_tiles()
                for a in self.animations:
                    if isinstance(a, SlideTile):
                        a.draw(self.screen)
            else:
                for a in self.animations:
                    a.draw(self.screen)

            # Draw particles
            for p in self.particles:
                p.draw(self.screen)

            # Overlays
            if self.show_win_msg:
                self.draw_overlay("You Win!", "Click or press any key to continue", (237, 194, 46), 180)
            elif self.game_over:
                self.draw_overlay("Game Over!", "Press R to restart", (255, 255, 255), 180)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


# ─── RUN ─────────────────────────────────────────────────
if __name__ == "__main__":
    Game2048().run()
    