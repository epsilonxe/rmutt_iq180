import pygame
import pygame.freetype
import numpy as np
import sys


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
FONT_SIZE = 40
BLINK = True
BLINK_SPEED = 600
RAND_INTERVAL = 200

COLOR_PRIME_1 = [220, 0, 0]
COLOR_PRIME_2 = [255, 255, 0]
COLOR_BG = [0, 0, 0]
COLOR_FG = [255, 255, 255]


class GameIQ180():
	def __init__(self, size=None, scene='start'):
		pygame.init()
		pygame.display.set_caption('RMUTT IQ180')
		self.run = True
		self.num_digit = None
		self.surface = None
		self.scene = scene
		self.select = 0
		if size == 'semifull':
			fscr = pygame.display.Info()
			global SCREEN_WIDTH
			global SCREEN_HEIGHT
			SCREEN_WIDTH = 0.99*fscr.current_w
			SCREEN_HEIGHT = 0.92*fscr.current_h
			screensize = (SCREEN_WIDTH, SCREEN_HEIGHT)
			self.surface = pygame.display.set_mode(screensize)

		elif size == 'full':
			fscr = pygame.display.Info()
			SCREEN_WIDTH = fscr.current_w
			SCREEN_HEIGHT = fscr.current_h
			screensize = (SCREEN_WIDTH, SCREEN_HEIGHT)
			self.surface = pygame.display.set_mode(
					(0, 0), 
					pygame.FULLSCREEN)

		self.bgcolor = COLOR_BG
		self.clock = pygame.time.Clock()
		self.key_timer = 0
		self.game_state = -1
		self.game_tick = 0
		self.game_recent_clock = 0
		self.slots = [0] * 5
		self.target = 0

		self.BLINK_EVENT = pygame.USEREVENT + 1
		pygame.time.set_timer(self.BLINK_EVENT, BLINK_SPEED)

		self.beep_sound = [pygame.mixer.Sound('./assets/sounds/enter_game.wav'), False]
		self.hit_sound = [pygame.mixer.Sound('./assets/sounds/hit.wav'), False]
		self.bell_sound = [pygame.mixer.Sound('./assets/sounds/bell.wav'), False]
		self.slot_music = [pygame.mixer.Sound('./assets/sounds/slot.wav'), False]
		self.game_music = [pygame.mixer.Sound('./assets/sounds/game_level.wav'), False]
		self.menu_music = [pygame.mixer.Sound('./assets/sounds/get_ready.mp3'), False]
		


	def launch(self):


		self.slots = None
		self.target = None
		self.counter = None

		while self.run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run = False
				elif event.type == self.BLINK_EVENT:
					global BLINK
					BLINK = not BLINK
				elif event.type == pygame.KEYDOWN:
					if self.scene == 'start':
						pygame.mixer.Sound.play(self.beep_sound[0])
						self.scene = 'mode_selection'
					elif self.scene == 'mode_selection':
						kbinput = pygame.key.get_pressed()
						if kbinput[pygame.K_RETURN] or kbinput[pygame.K_KP_ENTER]:
							self.scene = 'game'
							pygame.mixer.Sound.play(game.beep_sound[0])

				else:
					pass

			self.surface.fill(self.bgcolor)		
			self.run_scence()
			pygame.display.update()
			self.clock.tick(FPS)

	def play_sound(self, sound, loops=0):
		if not sound[1]:
			pygame.mixer.Sound.play(sound[0], loops=loops)
			sound[1] = True
  
	def game_key_pressed(self):
		kbinput = pygame.key.get_pressed()
		if kbinput[pygame.K_RETURN] or kbinput[pygame.K_KP_ENTER]:
			now_time = pygame.time.get_ticks()
			if now_time - game.key_timer >= 200:
				if self.scene == 'game':
					self.game_state = (self.game_state + 1) % 4
					self.bell_sound[1] = False
				self.key_timer = now_time

		elif kbinput[pygame.K_ESCAPE]:
			now_time = pygame.time.get_ticks()
			if now_time - game.key_timer >= 200:
				if game.scene == 'game': 
					game.scene = 'mode_selection'
					game.game_state = -1
				elif game.scene == 'mode_selection':
					game.scene = 'start'
				game.bell_sound[1] = False
				game.slot_music[1] = False
				game.game_music[1] = False
				pygame.mixer.Sound.stop(game.slot_music[0])
				pygame.mixer.Sound.stop(game.game_music[0])
				game.key_timer = now_time

		
	def str_clock(x):
		ms = x % 1000
		s = int((x - ms)/1000)
		m = int(s // 60)
		s = s - m*60
		return f'{m:02d}:{s:02d}:{ms:03d}'

	def quit(self):
		pygame.quit()
		sys.exit()

	def run_scence(self):
		scene = self.scene

		if scene == 'start':

			self.play_sound(self.menu_music, loops=-1)
			
			logo_loc = './assets/figures/rmutt_iq180_logo.png'
			logo = pygame.image.load(logo_loc)
			logo = pygame.transform.scale_by(logo, SCREEN_HEIGHT/880 )
			logo_rect = logo.get_rect()
			logo_rect.center = np.array([SCREEN_WIDTH/2, 0.8*SCREEN_HEIGHT/2])
			self.surface.blit(logo, logo_rect)


			text = GameText(font='EXEPixelPerfect', size=1)
			text.pos = np.array([SCREEN_WIDTH/2, 1.4*SCREEN_HEIGHT/2])
			text.str = 'Press any key to start'
			text.blink()
			text.draw(self.surface, fg=COLOR_PRIME_2)

			credit = GameText(font='EXEPixelPerfect', size=0.8)
			credit.pos = np.array([SCREEN_WIDTH/2, 0.97*SCREEN_HEIGHT])
			credit.str = 'Copyright 2023. All right reserved. Department of Mathematics, RMUTT.'
			credit.draw(self.surface)

		elif scene == 'mode_selection':

			if not self.menu_music[1]:
				self.play_sound(self.menu_music)
				self.menu_music[1] = True
			
			logo_loc = './assets/figures/rmutt_iq180_logo_blur.png'
			logo = pygame.image.load(logo_loc)
			logo = pygame.transform.scale_by(logo, SCREEN_HEIGHT/880 )
			logo_rect = logo.get_rect()
			logo_rect.center = np.array([SCREEN_WIDTH/2, 0.8*SCREEN_HEIGHT/2])
			self.surface.blit(logo, logo_rect)

			text = GameText(font='EXEPixelPerfect', size=1)
			text.pos = np.array([SCREEN_WIDTH/2, 1.4*SCREEN_HEIGHT/2])
			text.str = 'Select game difficulity'
			text.draw(self.surface)

			modes = ['easy', 'normal', 'advance']
			digits = [3, 4, 5]
			self.num_digit = digits[self.select]
			num_modes = len(modes)
			text_modes = [None] * num_modes
			ext_y = 1.4
			for k in range(num_modes):
				ext_y += 0.1 
				text_modes[k] = GameText(font='EXEPixelPerfect', size=1.2)
				text_modes[k].pos = np.array([SCREEN_WIDTH/2, ext_y*SCREEN_HEIGHT/2])
				text_modes[k].str = modes[k].title()
				if self.select == k:
					text_modes[k].draw(self.surface, fg=COLOR_PRIME_2, bgalpha=0)
				else:
					text_modes[k].draw(self.surface)
			kbinput = pygame.key.get_pressed()
			kblist = [pygame.K_DOWN, pygame.K_UP]
			kbval = [1, -1]
			for k,v in zip(kblist, kbval):
				if kbinput[k]:
					now_time = pygame.time.get_ticks()
					if now_time - self.key_timer >= 200:
						self.select = (self.select + v) % num_modes
						self.num_digit = digits[self.select]
						self.key_timer = now_time
						pygame.mixer.Sound.play(self.hit_sound[0])


			self.slots = [None] * self.num_digit
			for k in range(self.num_digit):
				self.slots[k] = SlotNumber(size=7)
				self.slots[k].pos = ((k+1)*SCREEN_WIDTH/(game.num_digit+1), 0.5*SCREEN_HEIGHT/2)

			self.target = SlotNumber(size=10)
			self.target.pos = (SCREEN_WIDTH/2, 1.5*SCREEN_HEIGHT/2)
			self.target.str = '0' * max(2, self.num_digit-2)

			self.counter = SlotNumber(ini='READY', size=1)
			self.counter.pos = (SCREEN_WIDTH/2, 0.05*SCREEN_HEIGHT)
			
			self.game_key_pressed()

		elif scene == 'game':

			self.menu_music[0].stop()
			self.menu_music[1] = False

			if self.game_state == 0: # Initialization
				self.game_music[0].set_volume(0.4)
				self.play_sound(self.game_music, loops=-1)
				self.counter.str = 'READY'
				for k in range(self.num_digit):
					self.slots[k].str = '0'
				self.target.str = '0' * max(2, self.num_digit-2)
			
			elif self.game_state == 1: # Random
				self.game_music[0].set_volume(0.4)
				if not self.slot_music[1]:
					pygame.mixer.Sound.play(self.slot_music[0], loops=-1)
					self.slot_music[1] = True
				for k in range(self.num_digit):
					self.slots[k].roll(0, 10)
				if self.num_digit == 5:
					self.target.roll(100, 1000)
				else:
					self.target.roll(10, 100)
				self.counter.str = 'SET'
			
			elif self.game_state == 2: # Freeze/ Clock run
				self.game_music[0].set_volume(1)
				if self.slot_music[1]:
					pygame.mixer.Sound.stop(self.slot_music[0])
					self.slot_music[1] = False
				self.play_sound(self.bell_sound)
				if self.game_tick == 0:
					now = pygame.time.get_ticks()
					self.game_tick = now
				counter_time = pygame.time.get_ticks() - self.game_tick
				self.counter.str = 'START ' + GameIQ180.str_clock(counter_time)
				self.game_recent_clock = counter_time
			
			elif self.game_state == 3: # Clock stop
				self.game_music[0].set_volume(0.25)
				self.play_sound(self.bell_sound, loops=2)
				self.game_tick = 0
				self.counter.str = 'STOP  ' + GameIQ180.str_clock(self.game_recent_clock)
			
			else: # Default of game state
				pass

			for k in range(self.num_digit):
				self.slots[k].draw(self.surface, fg=COLOR_PRIME_1)
			self.target.draw(self.surface, fg=COLOR_PRIME_1)
			self.counter.draw(self.surface)
			self.game_key_pressed()

		else: # Default of scene
			pass


class GameText(pygame.freetype.Font):
	def __init__(self, size=1, font=None, visible=True):
		size = size*FONT_SIZE*(SCREEN_HEIGHT/600)
		font_path = './assets/fonts/' + font + '.ttf'
		super().__init__(font_path, size)
		self.str = None
		self.pos = None
		self.visible = visible

	def blink(self):
		self.visible = BLINK

			
	def draw(self, surface, fg=COLOR_FG, bg=COLOR_BG, bgalpha=0):
		bgalpha = min(255, bgalpha)
		if len(bg) == 4:
			bg[3] = bgalpha
		else:
			bg = bg + [bgalpha]
		text_surf, _ = self.render(self.str, fg, bg)
		if self.visible:
			surface.blit(text_surf, text_surf.get_rect(center=self.pos))


class SlotNumber(GameText):
	def __init__(self, ini='0', **kwargs):
		super().__init__(font='digital-7_mono', **kwargs)
		self.str = ini
		self.next_roll = SlotNumber.next_roll()

	def roll(self, x=0, y=9):
		if pygame.time.get_ticks() > self.next_roll:
			self.str = str(np.random.randint(x, y))
			self.next_roll = SlotNumber.next_roll()

	def next_roll():
		return pygame.time.get_ticks() + np.random.rand()*RAND_INTERVAL

	

if __name__ == '__main__':
	game = GameIQ180(size='semifull')
	game.launch()
	game.quit()