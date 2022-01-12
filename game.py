#Name: Benjamin Chen
#Game: 2D Runner
from cmu_112_graphics import *
from character import *
from platform import *
from powerup import *
from doublejump import *
from speedup import *
from zerogravity import *
from timeslow import *
from coin import *
import random
import math

def appStarted(app):
    app.mode = 'drawStartScreen'
    app.isGameOver = False
    app.score = 0
    app.character = Character(100, 702, 0, 0)
    app.jumpBool = False
    app.jumpBack = False
    app.timerDelay = 50
    app.gravity = 1.25
    app.moveCheck = True
    imageAssets(app)
    coinsPowerUps(app)
    scroll(app)
    app.difficulty = ''

def imageAssets(app):
    app.characterImage = app.loadImage('characterright.png') #https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32?download
    app.characterImage = app.scaleImage(app.characterImage, 2) 
    app.platformImage = app.loadImage('platform.png') #https://www.deviantart.com/mackieftw/art/Simple-2D-Platforms-Ground-for-2D-games-511288073
    app.ground = app.loadImage('ground.png')
    #https://www.pinterest.com/pin/720435271629683682/ All 4 POWERUPS ASSETS
    app.doubleJumpImage1 = app.loadImage('double jump sprite.png')
    app.doubleJumpImage = app.scaleImage(app.doubleJumpImage1, 1/2)
    app.speedUpImage1 = app.loadImage('speed up sprite.png')
    app.speedUpImage = app.scaleImage(app.speedUpImage1, 1/2)
    app.zeroGravityImage1 = app.loadImage('zero gravity sprite.png')
    app.zeroGravityImage = app.scaleImage(app.zeroGravityImage1, 1/2)
    app.timeSlowImage1 = app.loadImage('time slow sprite.png')
    app.timeSlowImage = app.scaleImage(app.timeSlowImage1, 1/2)
    app.coinImage1 = app.loadImage('coin sprite.png') #https://www.pngegg.com/en/png-ertzr
    app.coinImage = app.scaleImage(app.coinImage1, 1/8)
    app.titleScreenImage1 = app.loadImage('title screen.png') #made in photoshop
    app.titleScreenImage = app.scaleImage(app.titleScreenImage1, .8)

def coinsPowerUps(app):
    app.platforms = [] #tracks the number of platforms on screen
    app.coins = [] #tracks coins on screen
    app.powerUps = ['doublejump', 'speedup', 'zerogravity', 'timeslow'] #all possible types of powerups you can get
    app.doubleJumpCounter = 0
    app.powerUpsGenerated = []
    app.doubleJumpTimer = 200
    app.speedUpTimer = 200
    app.speedUpBool = False
    app.zeroGravityTimer = 200
    app.timeSlowTimer = 200
    app.moveDistance = 10
    app.platformGenerated = 0
    app.coinTimer = 0
    app.coinSpawn = 0
    app.coinSpawnGoal = random.randint(2, 5)
    app.platformSpawnGoal = random.randint(2, 8)
    app.spawnDistance = 650
    app.coinGoal = 0

def scroll(app):
    app.timeScroll = 0
    app.scrollX = 3
    app.drawFinalSpeed = False
    app.timeSlow = False
    app.oldScrollX = 0
    app.scrollIncrement = 8
    app.scrollIncrementCounter = 0
    app.finalScrollX = 25
    app.backgroundScroll = 5

def keyPressed(app, event):
    if (app.isGameOver == False):
        if (event.key == 'Right' and app.moveCheck == True):
            app.character.move(app.moveDistance, 0)
        if (event.key == 'Left' and app.moveCheck == True):
            app.character.move(-1 * app.backwardsMoveDistance, 0)
        if (event.key == 'Up' and checkDoubleJump(app) != None and app.doubleJumpCounter < 2): #only activates with doublejump powerup
            if (event.key == 'Right'):
                app.character.xv = app.moveDistance
            elif (event.key == 'Left'):
                app.character.xv = -1 * app.backwardsMoveDistance
                app.jumpBack = True
            app.character.yv = -20
            app.jumpBool = True
            app.jumpBack = False
            app.doubleJumpCounter += 1
        if (event.key == 'Up' and onGround(app)):
            if (event.key == 'Right'):
                app.character.xv = app.moveDistance
            elif (event.key == 'Left'):
                app.character.xv =  -1 * app.backwardsMoveDistance
                app.jumpBack = True
            app.character.yv = -20
            app.jumpBool = True
            app.jumpBack = False
    if (app.isGameOver == True):
        if (event.key == 'r'):
            app.isGameOver = False
            appStarted(app)

def keyReleased(app, event):
    if (app.isGameOver == False):
        if (event.key == 'Right'):
            app.character.xv = 0
        elif (event.key == 'Left'):
            app.character.xv = 0

def timerFired(app):
    jump(app)
    if (legalPositionCharacterSide(app) != None
        and legalPositionCharacterBottom(app)):  
        #checks for platform hitboxes so character doesn't phase through 
        app.jumpBool = False #interrupts the jump
        app.character.xv = 0
        app.moveCheck = False
        app.character.yv = 10
    app.moveCheck = True
    platformGenerator(app) #continously generates platforms with checks and delays
    app.timeScroll += .05 #keeping track of how much time has passed
    if (app.timeScroll >= app.scrollIncrement and app.timeSlow == False): #TIME BASED AD AND POWERUP GENERATION
        app.scrollX += 1
        app.timeScroll = 0
        app.moveDistance += 1
        app.scrollIncrementCounter += 1
        if (app.scrollIncrementCounter >= 8): #every 8 times that scrollX increases, the amount of time needed to increase the speed is lowered
            app.scrollIncrement -= 1
            app.scrollIncrementCounter = 0
    if (app.scrollX >= app.finalScrollX):
        app.drawFinalSpeed = True
    #updating everything based on scroll
    app.character.x -= app.scrollX
    for platform in app.platforms:
        platform.leftBound -= app.scrollX
        platform.rightBound -= app.scrollX
    if (len(app.powerUpsGenerated) != 0):
        app.powerUpsGenerated[0].x -= app.scrollX
    for coin in app.coins:
        coin.x -= app.scrollX
    powerUpObtained(app) #checks when the characater picks up a powerup
    coinObtained(app) #check when character picks up a coin
    timerFiredPowerUps(app) #Checking for powerup time elapsed and removing it from powerups list
    platformRemoval(app) #removes platforms off screen
    powerUpRemoval(app) #removes powerUps off screen
    coinRemoval(app) #removes coins off screen
    if (legalPositionBounds(app) == False):
        app.isGameOver = True

def difficultySelection(app):
    if (app.difficulty == 'easy'):
        app.moveDistance = 10
        app.backwardsMoveDistance = 7
        app.startSpawnDistance = 750
        app.scrollX = 2
        app.maxSpawn = 75
        app.coinGoal = 3
        app.backgroundImage1 = app.loadImage('background1.png') #https://assetstore.unity.com/packages/tools/sprite-management/2d-field-parallax-background-152849
        app.backgroundImage = app.scaleImage(app.backgroundImage1, .7)
    elif (app.difficulty == 'medium'):
        app.moveDistance = 10
        app.backwardsMoveDistance = 3
        app.spawnDistance = 650
        app.scrollX = 4
        app.maxSpawn = 90
        app.coinGoal = 5
        app.backgroundImage1 = app.loadImage('background2.png') #https://itch.io/jam/bigjamgame-i-start
        app.backgroundImage = app.scaleImage(app.backgroundImage1, .7)
    elif (app.difficulty == 'hard'):
        app.moveDistance = 10
        app.backwardsMoveDistance = 0
        app.spawnDistance = 580
        app.scrollX = 7
        app.maxSpawn = 105
        app.coinGoal = 8
        app.backgroundImage1 = app.loadImage('background3.png') #https://superbrutalassets.itch.io/2d-hell-side-scrolling-platformer-pack/devlog/24467/2d-hell-side-scrolling-platformer-pack
        app.backgroundImage = app.scaleImage(app.backgroundImage1, .7)

def jump(app):
    #https://gamedev.stackexchange.com/questions/29617/how-to-make-a-character-jump
    #JUMPING
    if (app.jumpBool == True):
        if (app.jumpBack == True):
            app.character.x -= app.character.xv 
            app.jumpBack = True
        else:
            app.character.x += app.character.xv
        app.character.y += app.character.yv 
        app.character.yv += app.gravity
        if (legalPositionGround(app)): #ground check
            app.character.y = 702
            app.jumpBool = False
            app.character.yv = 0
            app.doubleJumpCounter = 0
        elif (legalPositionPlatform(app) != None): #platform check
            app.character.y = legalPositionPlatform(app) - 68
            app.jumpBool = False
            app.character.yv = 0
            app.doubleJumpCounter = 0
    #GRAVITY
    else:
        if (onGround(app) == False):
            app.character.y += app.character.yv
            app.character.yv += app.gravity
        else:
            if (legalPositionGround(app)): #ground check BIT GLITCHY WHEN LANDING
                app.character.y = 702
                app.character.yv = 0
            if (legalPositionPlatform(app) != None): #platform check
                app.character.y = legalPositionPlatform(app) - 68
                app.character.yv = 0

def timerFiredPowerUps(app):
    if (checkDoubleJump(app) != None):
        app.doubleJumpTimer -= 1
        if (app.doubleJumpTimer <= 0):
            app.character.powerUps.pop(checkDoubleJump(app))
            app.doubleJumpTimer = 200

    if (checkSpeedUp(app) != None):
        app.speedUpTimer -= 1
        if (app.speedUpBool == False):
            app.spawnDistance -= 200
            app.moveDistance += 6
            app.speedUpBool = True
        if (app.speedUpTimer <= 0):
            app.character.powerUps.pop(checkSpeedUp(app))
            app.moveDistance -= 6 #resetting speed after the powerup has been popped
            app.spawnDistance += 200 #resetting the distance between platforms
            app.speedUpTimer = 200
            app.speedUpBool = False

    if (checkZeroGravity(app) != None):
        app.zeroGravityTimer -= 1
        app.gravity = .75
        if (app.zeroGravityTimer <= 0):
            app.character.powerUps.pop(checkZeroGravity(app))
            app.gravity = 1.25
            app.zeroGravityTimer = 200

    if (checkTimeSlow(app) != None):
        app.timeSlowTimer -= 1
        app.timeSlow = True
        if (app.scrollX != 3):
            app.oldScrollX = app.scrollX
        app.scrollX = 3
        if (app.timeSlowTimer <= 0):
            app.character.powerUps.pop(checkTimeSlow(app))
            app.timeSlowTimer = 200
            app.timeSlow = False
            app.scrollX = app.oldScrollX

def legalPositionBounds(app):
    if (app.character.y > 800): #checking for ground collisions
        return False
    elif (app.character.x < 10):
        return False
    elif (app.character.x > 1000):
        return False
    return True

def legalPositionPlatform(app): #setting hitboxes for platforms 
    for platform in app.platforms: 
        if (app.character.x + 90 >= platform.leftBound 
            and app.character.x + 90 <= platform.rightBound
            and app.character.y + 68 >= platform.topBound 
            and app.character.y + 68 <= platform.bottomBound - 40):
                return platform.topBound
    return None

def legalPositionGround(app): #setting hitbox for ground
    if (app.character.y + 68 >= 770):
        return True
    return False

def legalPositionCharacterBottom(app): #setting hitbox for character
    for platform in app.platforms:
        if (app.character.x + 110 >= platform.leftBound 
            and app.character.x + 110 <= platform.rightBound
            and app.character.y >= platform.topBound 
            and app.character.y <= platform.bottomBound):
                return 42
    return None

def legalPositionCharacterSide(app):
    for platform in app.platforms:
        if (app.character.x + 90 >= platform.leftBound
            and app.character.x + 90 <= platform.rightBound
            and app.character.y >= platform.topBound
            and app.character.y <= platform.bottomBound):
            return 42
    return None

def onGround(app): #checking to see if character is on something so they can jump
    if (legalPositionGround(app) or legalPositionPlatform(app) != None):
        return True
    return False

def platformSpawned(app): #forces delay between platform spawning
    for platform in app.platforms:
        if (platform.leftBound >= app.spawnDistance):
            return True
    return False

def platformGenerator(app): #procedurally generating platforms
    if (onGround(app) and platformSpawned(app) == False):
        if (checkDoubleJump(app) == None and checkZeroGravity(app) == None):
            neutralGeneration(app)
        elif (checkDoubleJump(app) != None and app.doubleJumpTimer >= 1): #procedural generation for double jumps
            doubleJumpGeneration(app)
        elif (checkZeroGravity(app) != None and app.zeroGravityTimer >= 1): #procedural generation for zero gravity
            zeroGravityGeneration(app)

def neutralGeneration(app):
    if (legalPositionPlatform(app)): #when character is on platform
        minLevel = int(app.character.y + 200)
        if (minLevel >= 630): #checking to make sure platform doesn't spawn in ground
            minLevel = 630
        maxLevel = int(app.character.y - app.maxSpawn)
        if (maxLevel <= 150): #lowering platforms if the platforms get too high up on the screen
            maxLevel = 200
        if (maxLevel >= minLevel):
            maxLevel = minLevel - 50
        randomYLevel = random.randint(maxLevel, minLevel) #generates a random level for platforms
        platform = Platform(1000, randomYLevel) #VSC Code not recognizing this (still works though)
        app.platforms.append(platform) 
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal): #checks to see if the number of platforms spawned has exceeded the goal and then spawns a powerup
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    elif (legalPositionGround(app)): #when character is on ground
        minLevel = 650
        maxLevel = 590
        randomYLevel = random.randint(maxLevel, minLevel)
        platform = Platform(1000, randomYLevel)
        app.platforms.append(platform)
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal):
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    if (app.coinSpawn >= app.coinSpawnGoal): #checks if number of platforms spawned has exceeded the goal to spawn a coin
        coinGenerator(app)
        app.coinSpawn = 0
        app.coinSpawnGoal = random.randint(2, app.coinGoal)
    app.coinSpawn += 1

def doubleJumpGeneration(app):
    if (legalPositionPlatform(app)): 
        if (app.character.y <= 200):
            minLevel = int(app.character.y + 300)
        else:
            minLevel = int(app.character.y - 100)
        if (minLevel >= 630): 
            minLevel = 630
        maxLevel = int(app.character.y - (app.maxSpawn + 150))
        if (maxLevel <= 200): 
            maxLevel = 300
        if (maxLevel >= minLevel):
            maxLevel = minLevel - 50
        randomYLevel = random.randint(maxLevel, minLevel) 
        platform = Platform(1000, randomYLevel) 
        app.platforms.append(platform) 
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal):
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    elif (legalPositionGround(app)):
        minLevel = 560
        maxLevel = 480
        randomYLevel = random.randint(maxLevel, minLevel)
        platform = Platform(1000, randomYLevel)
        app.platforms.append(platform)
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal):
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    if (app.coinSpawn >= app.coinSpawnGoal):
        coinGenerator(app)
        app.coinSpawn = 0
        app.coinSpawnGoal = random.randint(2, app.coinGoal)
    app.coinSpawn += 1

def zeroGravityGeneration(app):
    if (legalPositionPlatform(app)): 
        if (app.character.y <= 200):
            minLevel = int(app.character.y + 300)
        else:
            minLevel = int(app.character.y - 100)
        if (minLevel >= 630): 
            minLevel = 630
        maxLevel = int(app.character.y - (app.maxSpawn + 170))
        if (maxLevel <= 200): 
            maxLevel = 300
        if (maxLevel >= minLevel):
            maxLevel = minLevel - 50
        randomYLevel = random.randint(maxLevel, minLevel) 
        platform = Platform(1000, randomYLevel)
        app.platforms.append(platform) 
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal):
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    elif (legalPositionGround(app)): 
        minLevel = 600
        maxLevel = 550
        randomYLevel = random.randint(maxLevel, minLevel)
        platform = Platform(1000, randomYLevel)
        app.platforms.append(platform)
        app.platformGenerated += 1
        if (app.platformGenerated >= app.platformSpawnGoal):
            powerUpGenerator(app)
            app.platformGenerated = 0
            app.platformSpawnGoal = random.randint(2, 8)
    if (app.coinSpawn >= app.coinSpawnGoal):
        app.coinSpawn = 0
        app.coinSpawnGoal = random.randint(2, app.coinGoal)
    app.coinSpawn += 1

def platformRemoval(app): #must work with the side scroller
    for platform in app.platforms:
        if (platform.rightBound <= 0):
            app.platforms.remove(platform)

def powerUpGenerator(app):
    platformLocation = app.platforms[-1]
    randomPowerUpIndex = random.randint(0, len(app.powerUps) - 1)
    if (randomPowerUpIndex == 0):
        powerUpGenerated = DoubleJump(platformLocation.leftBound - 40, 
                                      platformLocation.topBound - 60, 10) #time in seconds
    elif (randomPowerUpIndex == 1):
        powerUpGenerated = SpeedUp(platformLocation.leftBound - 40, 
                                   platformLocation.topBound - 60, 10)
    elif (randomPowerUpIndex == 2):
        powerUpGenerated = ZeroGravity(platformLocation.leftBound - 40, 
                                       platformLocation.topBound - 60, 10)
    elif (randomPowerUpIndex == 3):
        powerUpGenerated = TimeSlow(platformLocation.leftBound - 40, 
                                    platformLocation.topBound - 60, 10)      
    app.powerUpsGenerated.append(powerUpGenerated) #adding powerup to the list

def powerUpRemoval(app):
    for powerup in app.powerUpsGenerated:
        if (powerup.x <= 0):
            app.powerUpsGenerated.remove(powerup)

def powerUpObtained(app): #checking when the character collects a powerup
    for powerup in app.powerUpsGenerated:
        if (app.character.x + 30 >= powerup.x 
            and app.character.x + 30 <= powerup.x + 60
            and app.character.y + 30 >= powerup.y 
            and app.character.y + 68 <= powerup.y + 70):
            app.character.powerUps.append(powerup)
            app.powerUpsGenerated.pop()

def checkDoubleJump(app):
    for powerup in app.character.powerUps:
        if (isinstance(powerup, DoubleJump)):
            return app.character.powerUps.index(powerup)
    return None

def checkSpeedUp(app):
    for powerup in app.character.powerUps:
        if (isinstance(powerup, SpeedUp)):
            return app.character.powerUps.index(powerup)
    return None

def checkZeroGravity(app):
    for powerup in app.character.powerUps:
        if (isinstance(powerup, ZeroGravity)):
            return app.character.powerUps.index(powerup)
    return None

def checkTimeSlow(app):
    for powerup in app.character.powerUps:
        if (isinstance(powerup, TimeSlow)):
            return app.character.powerUps.index(powerup)
    return None

def coinGenerator(app):
    choose = random.randint(0, 1)
    if (choose == 0): #spawns on ground
        coin = Coin(910, 710) 
    else:
        platform = app.platforms[-1]
        coin = Coin(platform.leftBound + 40, platform.topBound - 60)
    app.coins.append(coin)

def coinObtained(app):
    for coin in app.coins:
        if (app.character.x + 30 >= coin.x 
            and app.character.x + 30 <= coin.x + 60
            and app.character.y + 30 >= coin.y 
            and app.character.y + 68 <= coin.y + 70):
            app.score += 100
            app.coins.remove(coin)

def coinRemoval(app):
    for coin in app.coins:
        if (coin.x <= 0):
            app.coins.remove(coin)

def redrawAll(app, canvas):
    if (app.isGameOver == False):
        canvas.create_image(670, 360, image = ImageTk.PhotoImage(app.backgroundImage))
        drawGround(app,canvas)
        canvas.create_image(app.character.x - app.scrollX, app.character.y, 
                            image = ImageTk.PhotoImage(app.characterImage))
        drawPlatforms(app, canvas)
        drawPowerUps(app, canvas)
        drawCoin(app, canvas)
        drawScore(app, canvas)
        drawDoubleJumpStatus(app, canvas)
        drawSpeedUpStatus(app, canvas)
        drawZeroGravityStatus(app, canvas)
        drawTimeSlowStatus(app, canvas)
        drawFinalStage(app, canvas)

    if (app.isGameOver):
        canvas.create_text(app.width / 2, app.height / 2, text = "GAME OVER", font = 'Arial 26 bold')
        canvas.create_text(app.width / 2, app.height / 2 + 40, text = 'THE WALL CAUGHT UP WITH YOU', font = 'Impact 15 bold')
        canvas.create_text(app.width / 2 - 20, app.height /2 + 80, text = 'Your final score was ', font = 'Arial 15 bold')
        canvas.create_text(app.width / 2 + 110, app.height / 2 + 80, text = app.score, font = 'Arial 15 bold')
        canvas.create_text(app.width / 2, app.height / 2 + 120, text = 'Press \'r\' to restart', font = 'Arial 15 bold')

def drawGround(app, canvas):
    for i in range(1000//325 + 1):
        canvas.create_image(i * 325 - 10, 770, 
                            image = ImageTk.PhotoImage(app.ground))

def drawPlatforms(app, canvas):
    for platform in app.platforms:
        canvas.create_image(platform.leftBound - app.scrollX, platform.topBound, 
                            image = ImageTk.PhotoImage(app.platformImage))

def drawPowerUps(app, canvas):
    if (len(app.powerUpsGenerated) != 0):
        for powerup in app.powerUpsGenerated:
            if (isinstance(powerup, DoubleJump)):
                canvas.create_image(powerup.x - app.scrollX, powerup.y,
                                    image = ImageTk.PhotoImage(app.doubleJumpImage))
            elif (isinstance(powerup, SpeedUp)):
                canvas.create_image(powerup.x - app.scrollX, powerup.y,
                                    image = ImageTk.PhotoImage(app.speedUpImage))
            elif (isinstance(powerup, ZeroGravity)):
                canvas.create_image(powerup.x - app.scrollX, powerup.y,
                                    image = ImageTk.PhotoImage(app.zeroGravityImage))
            elif (isinstance(powerup, TimeSlow)):
                canvas.create_image(powerup.x - app.scrollX, powerup.y,
                                    image = ImageTk.PhotoImage(app.timeSlowImage))

def drawCoin(app, canvas):
    for coin in app.coins:
        canvas.create_image(coin.x - app.scrollX, coin.y, image = ImageTk.PhotoImage(app.coinImage)) 

def drawScore(app, canvas):
    canvas.create_text(app.width / 2, 20, text = 'Score: ', font = 'Arial 15 bold')
    canvas.create_text(app.width / 2 + 45, 20, text = app.score, font = 'Arial 15 bold')

def drawFinalStage(app, canvas):
    if (app.drawFinalSpeed == True):
        canvas.create_text(app.width / 2, 50, text = 'YOU HAVE REACHED THE FINAL STAGE. STAY ALIVE FOR AS LONG AS POSSIBLE', font = 'Impact 15 bold')

def drawDoubleJumpStatus(app, canvas):
    if (checkDoubleJump(app) != None):
        canvas.create_image(30, 50, image = ImageTk.PhotoImage(app.doubleJumpImage))
        canvas.create_text(80, 50, text = app.doubleJumpTimer, font = 'Arial 15 bold')

def drawSpeedUpStatus(app, canvas):
    if (checkSpeedUp(app) != None):
        canvas.create_image(30, 100, image = ImageTk.PhotoImage(app.speedUpImage))
        canvas.create_text(80, 100, text = app.speedUpTimer, font = 'Arial 15 bold')

def drawZeroGravityStatus(app, canvas):
    if (checkZeroGravity(app) != None):
        canvas.create_image(30, 150, image = ImageTk.PhotoImage(app.zeroGravityImage))
        canvas.create_text(80, 150, text = app.zeroGravityTimer, font = 'Arial 15 bold')

def drawTimeSlowStatus(app, canvas):
    if (checkTimeSlow(app) != None):
        canvas.create_image(30, 200, image = ImageTk.PhotoImage(app.timeSlowImage))
        canvas.create_text(80, 200, text = app.timeSlowTimer, font = 'Arial 15 bold')

def drawStartScreen_keyPressed(app, event):
    if (event.key == 'Space'):
        app.mode = 'drawInstructions'

def drawStartScreen_redrawAll(app, canvas):
    canvas.create_image(500, 400, image = ImageTk.PhotoImage(app.titleScreenImage))
    canvas.create_text(app.width / 2, app.height / 2, text = '2D Runner', font = 'Arial 40 bold')
    canvas.create_text(app.width / 2, app.height / 2 + 60, text = 'Press \'space\' to view the instructions', font = 'Arial 14 bold')

def drawInstructions_mousePressed(app, event):
    if (event.x >= 150 and event.x <= 300 and event.y >= 650 and event.y <= 750):
        app.difficulty = 'easy'
        app.mode = ''
        difficultySelection(app)
    elif (event.x >= 420 and event.x <= 570 and event.y >= 650 and event.y <= 750):
        app.difficulty = 'medium'
        app.mode = ''
        difficultySelection(app)
    elif (event.x >= 690 and event.x <= 840 and event.y >= 650 and event.y <= 750):
        app.difficulty = 'hard'
        app.mode = ''
        difficultySelection(app)

def drawInstructions_redrawAll(app, canvas):
    canvas.create_text(app.width / 2, 40, text = "INSTRUCTIONS", font = 'Arial 26 bold')
    canvas.create_text(app.width / 2, 80, text = 'Welcome to 2D Runner!!!', font = 'Arial 14 bold')
    canvas.create_text(app.width / 2, 120, text = 'The objective of this game is to navigate your way through a series of obstacles and collect coins along the way.')
    canvas.create_text(app.width / 2, 160, text ='As you jump from platform to platform, the game will progessively get harder, making the use of powerups essential to progression.')
    canvas.create_text(app.width / 2, 200, text = 'Each powerup lasts for about 10 seconds. A status bar showing the amount of time you have left on each powerup will appear in the top left corner of the screen.')
    canvas.create_text(app.width / 2, 240, text = 'Be careful to not get too far behind or too far ahead or else the wall will catch up to you!', font = 'Arial 14 bold')
    canvas.create_text(app.width / 3, 300, text = 'Double Jump PowerUp: Allows the player to jump in midair to reach greater heights')
    canvas.create_image((app.width / 3) * 2, 300, image = ImageTk.PhotoImage(app.doubleJumpImage))
    canvas.create_text(app.width / 3, 360, text = 'Speed Up PowerUp : Allows the player to move faster temporarily')
    canvas.create_image((app.width / 3) * 2, 360, image = ImageTk.PhotoImage(app.speedUpImage))
    canvas.create_text(app.width / 3, 420, text = 'Zero Gravity PowerUp: Decreases the gravity so jump heights are increased')
    canvas.create_image((app.width / 3) * 2, 420, image = ImageTk.PhotoImage(app.zeroGravityImage))
    canvas.create_text(app.width / 3, 480, text = 'Time Slow PowerUp: Slows down time')
    canvas.create_image((app.width / 3) * 2, 480, image = ImageTk.PhotoImage(app.timeSlowImage))
    canvas.create_text(app.width / 2, 560, text = 'To move, use the arrow keys.', font = 'Arial 26 bold')
    canvas.create_text(app.width / 2, 600, text = 'When you are ready, select a difficulty level!', font = 'Arial 26 bold')
    canvas.create_rectangle(150, 650, 300, 750, fill = 'light green')
    canvas.create_text(220, 700, text = "EASY", font = 'Impact 18 ')
    canvas.create_rectangle(420, 650, 570, 750, fill = 'yellow')
    canvas.create_text(490, 700, text = "MEDIUM", font = 'Impact 18')
    canvas.create_rectangle(690, 650, 840, 750, fill = 'dark red')
    canvas.create_text(765, 700, text = "HARD", font = 'Impact 18')

runApp(width = 1000, height = 800)
