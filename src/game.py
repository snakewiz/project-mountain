from os import path

from PPlay.window import *
from PPlay.sprite import *

from player import Player
from notplatform import Platform
from mapmanager import MapManager

class Game:

  WINDOW_WIDTH = 1280
  WINDOW_HEIGHT = 720
  TITLE = 'Project Mountain v1.0.0'
  DEBUG = 0

  SAVE_PATH = 'save.txt'
  
  BACKGROUND_PATH = 'assets/bg.png'
  LOGO_PATH = 'assets/logo.png'
  FADE_PATH = 'assets/fade.png'
  ACTION_PATH = 'assets/action.png'

  GROUND_X = -10
  GROUND_Y = 710

  DEFAULT_DESCENT_SPEED = 100
  DESCENT_FACTOR = 2
  MAX_DESCENT_SPEED = 180

  def __init__(self):
    self.window = Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
    self.window.set_title(Game.TITLE)

    self.keyboard = self.window.get_keyboard()
    self.mouse = self.window.get_mouse()

    self.dir = path.dirname(__file__)

    self.background = Sprite(Game.BACKGROUND_PATH)
    self.logo = Sprite(Game.LOGO_PATH)
    self.fade = Sprite(Game.FADE_PATH)
    self.action = Sprite(Game.ACTION_PATH)

    self.logo.x = self.window.width / 2 - self.logo.width / 2
    self.logo.y = 100

    self.action.x = self.window.width / 2 - self.action.width / 2
    self.action.y = self.window.height / 2 + self.action.height

    self.isGameStarted = False

    self.descentSpeed = DEFAULT_DESCENT_SPEED = 80

    self.highScore = self.readHighScore()
    self.score = 0

    self.mapManager = MapManager(self)
    self.mapManager.init()

    self.player = Player(self)

  def readHighScore(self):
    data = None

    try:
      file = open(path.join(self.dir, Game.SAVE_PATH), 'r')
      data = int(file.read())
      file.close()
    except:
      data = 0

    return data

  def writeHighScore(self):
    try:
      file = open(path.join(self.dir, Game.SAVE_PATH), 'w')
      file.write(str(self.highScore))
      file.close()
    except:
      return

  def stop(self):
    self.isGameStarted = False

    self.descentSpeed = DEFAULT_DESCENT_SPEED = 80

    if (self.score > self.highScore):
      self.highScore = self.score
      self.writeHighScore()

    self.score = 0

    self.player = Player(self)
    self.mapManager = MapManager(self)
    self.mapManager.init()

  def tick(self):
    self.background.draw()
    
    self.mapManager.tick()
    self.player.tick()

    if (self.isGameStarted):

      if (self.score > 0):
        self.player.descend(self.descentSpeed)
        self.mapManager.descend(self.descentSpeed)

      if (self.keyboard.key_pressed('ESC')):
        self.stop()

      self.window.draw_text("PONTUAÇÃO: {}".format(self.score), 0, 0, 16, (251, 242, 54), "Arial", True)

    else:
      self.fade.draw()
      self.logo.draw()
      self.action.draw()

      self.window.draw_text("PONTUAÇÃO MÁXIMA: {}".format(self.highScore), Game.WINDOW_WIDTH / 2 - 160, Game.WINDOW_HEIGHT / 2, 24, (251, 242, 54), "Arial", True)

      if (self.keyboard.key_pressed('SPACE')):
        self.isGameStarted = True

    self.window.update()