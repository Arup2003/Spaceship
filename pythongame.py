import pygame, random, math, time
from pygame import mixer


#Initialize Pygame
switch = True
while switch:
	clock = pygame.time.Clock()
	pygame.init()

	#The window
	screen = pygame.display.set_mode((800, 600))

	#Title of the window and icon
	pygame.display.set_caption("Spaceship")
	icon = pygame.image.load("player.png")
	pygame.display.set_icon(icon)

	background = pygame.image.load("bg.jpeg")

	#Points
	score = 0 
	POINT = pygame.font.Font("freesansbold.ttf", 32)
	textX = 10
	textY = 10

	#Score Text
	def showscore(x,y):
		score1 = POINT.render("SCORE: " + str(score), True, (255, 255, 255))
		screen.blit(score1, (x, y))

	#GAME OVER TEXT
	over = pygame.font.Font("pencil.ttf", 64)
	text = pygame.font.Font("lead.ttf", 37)
	def game_over_text():
		gameover = over.render("GAME OVER" , True, (255, 255, 255))
		pt = text.render("SCORE: " + str(score), True, (255,255,255))
		screen.blit(gameover, (210, 270))
		screen.blit(pt, (350, 375))

	#Game Start Text
	start = pygame.font.Font("pencil.ttf", 50)
	def starting():
		diff= start.render("*Set Difficulty*" , True, (255, 255, 255))
		Start = start.render("Press 1 for EASY" , True, (200, 200, 255))
		Start1 = start.render("Press 2 to MEDIUM" , True, (200, 200, 255))
		Start2 = start.render("Press 3 to DIFFICULT" , True, (200, 200, 255))
		Start3 = start.render("Press 4 to INSANE" , True, (200, 200, 255))

		screen.blit(diff, (230, 100))
		screen.blit(Start, (165, 200))
		screen.blit(Start1, (165, 275))
		screen.blit(Start2, (165, 350))
		screen.blit(Start3, (165, 425))

	def wait():
		hola = pygame.font.Font("lead.ttf", 70)
		Wait = hola.render("Press SPACE to start!", True, (255, 255, 255))
		screen.blit(Wait, (115, 275))


	#Game End Text
	end = pygame.font.Font("lead.ttf", 60)
	end1 = pygame.font.Font("lead.ttf", 40)
	def ending():
		End = end1.render("Press SPACE to restart", True, (250, 250, 250))
		screen.blit(End, (225, 375))
		End1 = end1.render("Press ESCAPE to quit", True, (250, 250, 250))
		screen.blit(End1, (245, 325))
		End2 = end.render("Thanks for playing Arup's game!", True, (250, 250, 250))
		screen.blit(End2, (37, 225))

	#MUSIC! 
	mixer.music.load("start.mp3")
	mixer.music.play(-1)

	#Player and placing the player
	playerImg = pygame.image.load("main.png")
	playerX = 370
	playerY = 480
	playerX_change = 0 #Later this variable will help move the player 

	#Enemy Empty lists
	enemyImg = []
	enemyX = []
	enemyY = []
	enemyX_change = []
	enemyY_change = []
	num_of_enemies = 6

	#Missile
	missileImg = pygame.image.load("missile.png")
	missileX = playerX
	missileY = playerY
	missileX_change = 0
	missileY_change = 3
	#"ready" state means its not fired and "fire" state means it is moving
	missile_state = "ready"


	def player(x, y):
		screen.blit(playerImg, (x, y)) #Blit means to draw

	def enemy(x, y, i):
		screen.blit(enemyImg[i], (x, y))

	def fire_missile(x,y):
		global missile_state
		missile_state = "fire"
		screen.blit(missileImg, (x + 16, y + 10))

	def collide(enemyX, enemyY, missileX, missileY):
		distance = math.sqrt(math.pow(enemyX-missileX, 2) + math.pow(enemyY - missileY, 2))
		if distance < 30:
			return True
		else:
			return False

	#This will be the starting screen LOOP
	x = True
	while x:
		screen.blit(background, (0,0))

		starting()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				switch = False
				x = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					num_of_enemies = 1
					x = False
				if event.key == pygame.K_2:
					num_of_enemies = 3
					x = False
				if event.key == pygame.K_3:
					num_of_enemies = 5
					x = False
				if event.key == pygame.K_4:
					num_of_enemies = 8
					x = False

		pygame.display.update()

	#ENEMY!
	for i in range(num_of_enemies):
		enemyImg.append(pygame.image.load("enemy.png"))
		enemyX.append(random.randint(0, 800))
		enemyY.append(random.randint(0, 150))
		enemyX_change.append(1)
		enemyY_change.append(0) 

	waitt = True
	while waitt:
		screen.blit(background, (0,0))

		wait()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				switch = False
				wait = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					mixer.music.stop()
					waitt = False

		pygame.display.update()


	#Game Loop
	mixer.music.load("background.mp3")
	mixer.music.play()
	running = True
	while running:
		screen.blit(background, (0,0))

		#An event is something that a user does... (Presses close, presses a key, clicks etc...)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			#KEYDOWN is pressing a key and KEYUP is releasing a key...
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					playerX_change = -2.5
				if event.key == pygame.K_RIGHT:
					playerX_change = 2.5
				if event.key == pygame.K_SPACE:
					if missile_state == "ready":
						missile_sound = mixer.Sound("fire.wav")
						missile_sound.play()
						missileX = playerX
						fire_missile(missileX, missileY)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					playerX_change = 0
		
		#This will change the co-ordinates and make the player move
		playerX += playerX_change

		#This if else statement will create the boundar
		if playerX <= 0:
			playerX_change = 0 
		elif playerX >= 736:
			playerX_change = 0 

		#This will make the boundary for the enemy and when it will come down the y-axis
		for i in range(num_of_enemies):
			if enemyX[i] <= 0 or enemyX[i] >= 730:
				enemyX_change[i] = -enemyX_change[i]
				enemyY_change[i] = 80

			#This will change the position of the enemy in X axis and Y axis
			enemyX[i] += enemyX_change[i]
			enemyY[i] += enemyY_change[i]
			enemyY_change[i] = 0

			#This defines what will happen if the bullet collides with the enemy
			collision = collide(enemyX[i], enemyY[i], missileX, missileY)
			if collision:
				explosion_sound = mixer.Sound("destroy.wav")
				explosion_sound.play()
				missileX = playerX
				missileY = playerY
				missile_state = "ready"
				score += 1 
				enemyX_change[i] = random.randint(1, 7)
				enemyX[i] = random.randint(1, 700)
				enemyY[i] = random.randint(1, 150)

		#To move the missile after pressing the spacebar
		if missile_state == "fire":
			fire_missile(missileX, missileY)
			missileY -= missileY_change
			if missileY == 0:
				missile_state = "ready"
				missileY = playerY

		#GAME OVER
		for i in range(num_of_enemies):
			boom = math.sqrt(math.pow(enemyX[i] - playerX, 2) + math.pow(enemyY[i] - playerY, 2))
			if boom < 45:
				explosion_sound = mixer.Sound("destroy.wav")
				explosion_sound.play()
		
			if boom < 45 or enemyY[i] >= 2000:
				enemyY[i] = 2000
				playerY = 2000
				mixer.music.stop()
				mixer.music.load("End.mp3")
				mixer.music.play()
				running = False

		showscore(textX, textY )
		player(playerX, playerY)

		for i in range(num_of_enemies):
			enemy(enemyX[i], enemyY[i], i)
		clock.tick(160)
		pygame.display.update()

	lol = 0
	while lol < 500:
		screen.blit(background, (0, 0))
		game_over_text()
		lol+= 2
		pygame.display.update()

	endgame = True
	while endgame:
		screen.blit(background, (0,0))
		ending()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				switch = False
				endgame = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					endgame = False
				if event.key == pygame.K_ESCAPE:
					switch = False
					endgame = False

		pygame.display.update()




