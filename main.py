import arcade
import math
import random

SPRITE_SCALING = 0.25 #Játékos méret
BULLET_SCALING=0.01 #Rakéta méret
#METEOR_SCALING=0.15 Meteor méret

SCREEN_WIDTH = 1600 #Ablak szélessége
SCREEN_HEIGHT = 800 #Ablak magassága
SCREEN_TITLE = "Gem Game" #Ablak neve

ANGLE_SPEED = 5 #Forgás sebessége
BULLET_SPEED = 4 #Rakéta sebessége
METEOR_SPEED = 1 #Meteor sebessége

SPAWN_RATE = 120 #Framenként hány meteor spawn-nol

class Player(arcade.Sprite): #Játékos osztály

    def __init__(self, image, scale):
        super().__init__(image, scale)

    def update(self):
        
        self.angle += self.change_angle #Játékos forgatása

class MyGame(arcade.Window):#Játék osztály 

    def __init__(self, width, height, title):
        
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK) #Háttér sima fekete szín

        self.frame_count = 0 #Frame számláló
        
        self.bullet_sound = None #Rakéta kilövésének hangja
        
        self.score =0 #Pontszám
        self.score_text=None #Pontszám megjelenítésére szolgáló felirat

        self.meteor_list = None #Meteorok (ebben tároljuk a meteorokat, amik közelítenek majd a játékoshoz)
        self.bullet_list = None #Kilőtt rakéták (ebben tároljuk a rakétákat, amiket a játékos kilőtt)
        self.player_list = None #Játékos (ebben tároljuk a játékost)

    def setup(self): #Kezdőértékek átadása

        #Sprite lists
        self.meteor_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        #Játékos
        self.player_sprite = Player("player.png",SPRITE_SCALING)#Játékos osztályból létrehozunk egyet és kap egy sprite-ot
        self.player_sprite.center_x = SCREEN_WIDTH / 2 #Játékos x koordinátája
        self.player_sprite.center_y = SCREEN_HEIGHT / 2 #Játékos y koordinátája
        self.player_list.append(self.player_sprite) #A létrehozott játékost hozzáadjuk a listájához
        
        self.score = 0
        self.bullet_sound = arcade.Sound("raketa.wav")

    def on_draw(self):#Képernyőre rajzolás

        self.clear() #Képernyőt tisztít

        # Kirajzolja a sprite-okat
        self.meteor_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        pontok = "Score: "+str(self.score) #Pontszám
        arcade.draw_text(pontok,SCREEN_WIDTH / 2 - 30 ,SCREEN_HEIGHT-30,arcade.color.WHITE,14) #Pontszám felirat pozícionálása

    def on_update(self, delta_time):#Framenként megnézi az eseményeket
        
        self.frame_count += 1 #Eddigi framek száma
        
        if self.frame_count % SPAWN_RATE == 0: #Ha eltelik x db frame lefut
            METEOR_SCALING = random.randrange(2,5)*0.1 #Random méretű meteor
            meteor=arcade.Sprite("meteor.png",METEOR_SCALING) #Meteor létrehozása
            poz=int(random.randint(0,3)) #Random pozíció, hogy honnan induljon a meteor
            if poz == 0: #Képernyő bal széle
                meteor.center_x = 0
                meteor.center_y = random.randrange(SCREEN_HEIGHT)
            elif poz == 1: #Képernyő teteje
                meteor.center_x = random.randrange(SCREEN_WIDTH)
                meteor.center_y = SCREEN_HEIGHT
            elif poz == 2: #Képernyő jobb széle
                meteor.center_x = SCREEN_WIDTH
                meteor.center_y = random.randrange(SCREEN_HEIGHT)
            else: #Képernyő alja
                meteor.center_x = random.randrange(SCREEN_WIDTH)
                meteor.center_y = 0
            angle = math.atan2((self.player_sprite.center_y-meteor.center_y), (self.player_sprite.center_x-meteor.center_x)) #Meteor iránya
            meteor.angle = math.degrees(angle) #Meteor iránya fokban
            meteor.change_x=math.cos(angle) * METEOR_SPEED #Meteor x koordinátájának változtatása
            meteor.change_y=math.sin(angle) * METEOR_SPEED #Meteor y koordinátájának változtatása
            self.meteor_list.append(meteor) #Meteor hozzáadás a listához
        
        for bullet in self.bullet_list: #Rakéták listáján végigmegy
            hit=arcade.check_for_collision_with_list(bullet, self.meteor_list) #Megnézi van-e olyan rakéta, ami érintkezett meteorral
            if len(hit) >0: #Ha van rakétával érintkező meteor
                bullet.remove_from_sprite_lists() #Kitörli az adott rakétát
                for meteor in hit: #Végigmegy azokon a meteorokon, amik érintkeztek rakétával
                    meteor.remove_from_sprite_lists() #Kitörli a meteort
                    self.score += 1 #Növeli a pontszámot
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width: #Ha kimegy a rakéta a képernyőről
                bullet.remove_from_sprite_lists()#Kitörli a rakétát
        for meteor in self.meteor_list: #Végigmegy a meteorokon
            if meteor.bottom > self.width or meteor.top < 0 or meteor.right < 0 or meteor.left > self.width: #Ha kimegy a meteor a képernyőről
                meteor.remove_from_sprite_lists()#Kitörli a meteort
                
        self.bullet_list.update() #Frissíti a rakéták listáját
        self.player_list.update() #Frissíti a Játékos listáját
        self.meteor_list.update() #Frissíti a meteorok listáját

    def on_key_press(self, key, modifiers): #Billentyű lenyomása

        if key == arcade.key.LEFT or key == arcade.key.A: #Forgatás balra
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D: #Forgatás jobbra
            self.player_sprite.change_angle = -ANGLE_SPEED
        if key == arcade.key.SPACE: #Rakéta kilövése
            self.bullet_sound.play() #Rakéta hang lejátszása
            bullet = arcade.Sprite("missile.png",BULLET_SCALING) #Rakéta létrehozása
            bullet.center_x = self.player_sprite.center_x #Rakéta x koordinátája megegyezik a játékos x koordinátájával
            bullet.center_y = self.player_sprite.center_y #Rakéta y koordinátája megegyezik a játékos y koordinátájával
            bullet.angle = self.player_sprite.angle #Rakéta szöge
            bullet.change_y = math.cos(math.radians(bullet.angle)) * BULLET_SPEED #Rakéta y koordinátájának változása
            bullet.change_x = -math.sin(math.radians(bullet.angle)) * BULLET_SPEED #Rakéta x koordinátájának változása
            self.bullet_list.append(bullet) #Rakéta hozzáadása a rakéták listájához
        
        

    def on_key_release(self, key, modifiers): #Billentyű elengedése

        if key == arcade.key.LEFT or key == arcade.key.RIGHT or key == arcade.key.A or key == arcade.key.D: #Megállítja forgást
            self.player_sprite.change_angle = 0
        
            


def main(): #Egy függvény a játék indításához
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)#A játék osztályból létrehozunk eggyet
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()