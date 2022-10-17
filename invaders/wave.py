"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Eric Ho (eh643)
# December 12, 2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _movingRight: whether aliens are moving right, False if not
    # Invariant: _movingRight is a bool (True or False)

    # Attribute _movecount: the number of times the alien "steps"
    # Invariant: _movecount is an int>=0

    # Attribute _stepthresh: the max number of alien "steps" before shooting bolt
    # Invariant: _stepthresh is an int>=0

    # Attribute _collist: a list of column index not containing columns with
    #all aliens "None"
    # Invariant: _collist is a list

    # Attribute _pause: whether or not the game should be paused momentarily
    # Invariant: _pause is a bool (True or False)

    # Attribute _triggerRespawn: whether or not the ship should be respawned
    # Invariant: _triggerRespawn is a bool (True or False)

    # Attribute _allDead: whether or not all the aliens are dead
    # Invariant: _allDead is a bool (True or False)

    # Attribute _crossdline: whether or not the aliens have crossed over dline
    # Invariant: _crossdline is a bool

    # Attribute _wavecounter: number of waves completed
    # Invariant: _wavecounter is an int >=0

    # Attribute _wavespeed: the number of seconds btwn alien steps
    # Invariant: _wavespeed is a float >0 and <=1

    # Attribute _score: the current number of points the player has
    # Invariant: _score is an int>=0

    # Attribute _justKilled: whether or not an alien was just killed
    # Invariant: _justKilled is a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of ship lives left
        """
        return self._lives

    def getPause(self):
        """
        Returns whether the game should be paused
        """
        return self._pause

    def setPause(self, bool):
        """
        Sets whether the game should be paused

        Parameter bool: new bool for whether game should be paused
        Precondition: bool is a boolean (True or False)
        """
        self._pause= bool

    def getAllDead(self):
        """
        Returns whether or not all the aliens are dead
        """
        return self._allDead

    def getcrossdline(self):
        """
        Returns whether or not aliens have crossed the defense line
        """
        return self._crossdline

    def getscore(self):
        """
        Returns the current number of points accumulated.
        """
        return self._score

    def getjustKilled(self):
        """
        Returns whether an alien was just killed.
        """
        return self._justKilled

    def setjustKilled(self,bool):
        """
        Sets whether or not an alien was just killed.

        Primarily used to update the score in app.py

        Parameter bool: new bool for whether an alien was killed
        Precondition: bool is a boolean (True or False)
        """
        self._justKilled=bool

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self,wavecounter,score):
        """
        Initializes the wave.

        All the attributes are assigned. The ship, aliens, defense line, bolt
        list etc. are created by this function.

        Parameter wavecounter: number of waves completed
        Precondition: wavecounter is an int >=0

        Parameter score: the player's points accumulated over the game
        Precondition: score is an int>=0 in multiples of 10
        """
        self._aliens=[]
        self._movingRight=True
        self._make_aliens()
        self._ship=Ship()
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linewidth=2,linecolor='black')
        self._time=0
        self._bolts=[]
        self._movecount=0
        self._stepthresh=random.randint(1,BOLT_RATE)
        self._collist=list(range(0,ALIENS_IN_ROW))    #col index start at 0
        self._lives=3               #EACH NEW WAVE MEANS 3 LIVES!!
        self._pause=False
        self._triggerRespawn=False
        self._allDead=False
        self._crossdline=False
        self._wavecounter=wavecounter
        self._wavespeed=ALIEN_SPEED-(self._wavecounter*ALIEN_SP_DEC)
        self._score=score
        self._justKilled=False


    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Method to move ship, aliens, and bolts and change class attributes.
        This is the method that basically plays the majority of the game.

        Parameter input: the players keyboard input
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._allAliensDead()
        self._checkAlienPos()
        self._moveShip(input)
        self._alienWalk(dt)
        self._makeBolt(input)
        self._moveBolt()
        self._makeAlienBolt()
        self._collisions()
        self._trackLives()
        self._respawnShip()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Method to draw the aliens, ship, and bolts

        Parameter view: The view window
        Precondition: view is a Gview instance
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.draw(view)
        if self._ship!=None:
            self._ship.draw(view)
        self._dline.draw(view)
        if self._bolts!=[]:
            for bolt in self._bolts:
                bolt.draw(view)

    # HELPER METHODS
    def _make_aliens(self):
        """
        Helper function for the __init__, makes a 2D list of aliens (an array)

        The correct spacing of the aliens is also achieved when making the
        2D list of aliens. The aliens start initially moving right. Alien images
        will vary depend on the row the alien is in.
        """
        i=0
        y_corr=GAME_HEIGHT-ALIEN_CEILING-(ALIEN_ROWS-1)*(ALIEN_HEIGHT+ \
        ALIEN_V_SEP)-ALIEN_HEIGHT/2
        while i<ALIEN_ROWS:
            alien_row=[]
            c=0
            x_corr=ALIEN_H_SEP+ALIEN_WIDTH/2
            while c<ALIENS_IN_ROW:
                alien_row.append(Alien(x_corr,y_corr,source= \
                ALIEN_IMAGES[i//2%3]))
                x_corr+=ALIEN_H_SEP+ALIEN_WIDTH
                c+=1
            self._aliens.append(alien_row)
            y_corr+=ALIEN_HEIGHT+ALIEN_V_SEP
            i+=1

    def _moveShip(self,input):
        """
        Moves ship left or right SHIP_MOVEMENT depending on the key pressed

        Parameter input: the players keyboard input
        Precondition: input is an instance of GInput
        """
        if self._ship!=None:
            if input.is_key_down('left'):
                if self._ship.x-SHIP_MOVEMENT>=SHIP_WIDTH/2:
                    self._ship.x-=SHIP_MOVEMENT
            if input.is_key_down('right'):
                if self._ship.x+SHIP_MOVEMENT<=GAME_WIDTH-SHIP_WIDTH/2:
                    self._ship.x+=SHIP_MOVEMENT

    def _alienWalk(self,dt):
        """
        Walks the aliens back and forth.

        Keeps track of the time passing and number of moves of the aliens by
        incrementing class attributes. The left or right most alien is found
        (the alien should not be None). If the left-most alien reaches the left,
        all the aliens move down and then right. If the right-most alien reaches
        the right, all aliens move down then left.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._time<self._wavespeed:
            self._time+=dt
        if self._time>=self._wavespeed:
            self._movecount+=1
            col_list=[]
            for i in range(0,ALIENS_IN_ROW):
                col_list.append(i)
            alien=self._findLorR(col_list)        #find left or right most alien
            if alien!=None:
                if (self._movingRight and alien.x+ALIEN_H_WALK+ALIEN_WIDTH/2>= \
                GAME_WIDTH-ALIEN_H_SEP) or \
                    (not self._movingRight and alien.x-ALIEN_H_WALK- \
                    ALIEN_WIDTH/2<=ALIEN_H_SEP):
                    for row in self._aliens:
                        for alien in row:
                            if alien is not None:
                                alien.y-=ALIEN_V_WALK
                    self._movingRight= not self._movingRight
                else:
                    direction=1
                    if not self._movingRight:           #move left!
                        direction=-1
                    for row in self._aliens:
                        for alien in row:
                            if alien is not None:
                                alien.x+=ALIEN_H_WALK*direction
            self._time=0

    #helper of helper method; _alienWalk() helper
    def _findLorR(self,col_list):
        """
        Returns the left or right most alien that is not dead

        (i.e. Finds the left /right-most alien that is not None). This is a
        helper for the _alienWalk() method which moves the aliens back and forth

        Parameter col_list: list containing the columns of aliens
        Precondition: col_list is a list
        """
        alien=None
        while len(col_list)>0 and alien is None:
            if self._movingRight:
                for i in range(0,ALIEN_ROWS):
                    right_alien=self._aliens[i][col_list[-1]]
                    if right_alien is not None:
                        alien=right_alien
                        break
                del col_list[-1]
            else:
                for i in range(0,ALIEN_ROWS):
                    left_alien=self._aliens[i][col_list[0]]
                    if left_alien is not None:
                        alien=left_alien
                        break
                del col_list[0]
        return alien

    def _makeBolt(self,input):
        """
        Creates the a new player bolt with the press of 'spacebar'

        A new player bolt can only be created if there are no other player bolts
        active in the view and if there is a ship alive. Player bolts are red.

        Parameter input: the players keyboard input
        Precondition: input is an instance of GInput
        """
        canDraw=True
        for bolt in self._bolts:
            if bolt.getisPbolt():
                canDraw=False
                break
            else:
                canDraw=True
        if input.is_key_down('spacebar') and canDraw==True and self._ship!=None:
            self._bolts.append(Bolt(x=self._ship.x,y=self._ship.y+BOLT_HEIGHT/2\
            +SHIP_HEIGHT/2))

    def _moveBolt(self):
        """
        Move the bolts up for player bolt and down for alien bolt. Deletes bolt.

        Player bolts move BOLT_SPEED up with every animation frame. Alien bolts
        move BOLT_SPEED down with every animation frame. Bolts are deleted as
        the y values of the bolts reach the edge of the window.
        """
        for bolt in self._bolts:
            if bolt.getisPbolt()==True:
                bolt.y+=BOLT_SPEED
            else:
                bolt.y-=BOLT_SPEED
        i=0
        while i < len(self._bolts):
            if self._bolts[i].y>GAME_HEIGHT or self._bolts[i].y<0:
                del self._bolts[i]
            else:
                i += 1

    def _makeAlienBolt(self):
        """
        Create bolts to be fired from a random alien at the bottom of column

        Uses list of column indexes to randomly choose from. If all the aliens
        in the column are None, the column will be removed from the list with
        the column indexes. Therefore, that column cannot be selected to have a
        bolt fired from it. Alien fires if the move counter of the aliens
        reaches the random threshold. Alien bolts are blue.
        """
        while len(self._collist)>0 and self._movecount==self._stepthresh:
            randnum=random.choice(self._collist)
            alien=None
            i=0
            while i<len(self._aliens) and alien==None:
                currAlien=self._aliens[i][randnum]
                if currAlien!=None:
                    alien=currAlien
                i+=1
            if alien==None:
                self._collist.remove(randnum)   #no aliens can shoot in this col
            else:                                   #alien shoots
                self._bolts.append(Bolt(x=alien.x,y=alien.y-ALIEN_HEIGHT/2- \
                BOLT_HEIGHT/2,velocity=-BOLT_SPEED,fillcolor='blue', linecolor=\
                "blue"))
                self._movecount=0
                self._stepthresh=random.randint(1,BOLT_RATE)

    # HELPER METHODS FOR COLLISION DETECTION
    def _collisions(self):
        """
        Collision detection for the alien and ship bolts.

        If collision is detected, delete that bolt from the list of bolts.
        If the alien is hit by a plater bolt, then it is set to None. If the
        ship is hit by an alien bolt it is set to None. The alien speed is
        increased with every alien that is killed by multiplying self._wavespeed
        to INCREMENT.
        """
        i=0
        while i<len(self._aliens):                      #alien collisions
            alienind=0
            while alienind<len(self._aliens[0]):
                boltind=0
                while boltind<len(self._bolts) and self._aliens[i][alienind]!=None:
                    self._aliens[i][alienind].setHit(self._bolts[boltind])
                    if self._aliens[i][alienind].getHit()==True:
                        self._wavespeed*=(INCREMENT)   #increment alien speed
                        self._score+=((i//2)+1)*10
                        self._justKilled=True
                        del self._bolts[boltind]        #delete bolt
                        self._aliens[i][alienind]=None      #alien set to None
                    else:
                        boltind+=1
                alienind+=1
            i+=1
        if len(self._bolts)>0:                          #ship collisions
            i=0
            while i<len(self._bolts) and self._ship!=None:
                self._ship.setHit(self._bolts[i])
                if self._ship.getHit()==True:
                    del self._bolts[i]
                    self._ship=None
                else:
                    i+=1

    def _trackLives(self):
        """
        If ship is hit by a bolt, decrease lives and pause game. Allow for the
        ship to respawn.
        """
        if self._ship==None and self._pause==False and self._triggerRespawn==False:
            self._lives-=1
            self._pause=True
            self._triggerRespawn=True


    def _respawnShip(self):
        """
        If ship is hit by a bolt and can respawn, make a new ship.

        The ship cannot be respawned until the ship is killed again. (i.e.
        the new ship is hit by another bolt). The ship respawns in the middle
        of the window.
        """
        if self._ship==None and self._pause== False and self._triggerRespawn==True:
            self._ship=Ship()
            self._triggerRespawn=False

    def _allAliensDead(self):
        """
        Checks if all aliens are None (i.e. dead).

        If all the aliens are dead, then set the corresponding class attribute
        to True
        """
        nonecounter=0
        for row in self._aliens:
            for alien in row:
                if alien==None:
                    nonecounter+=1
                if nonecounter==(ALIEN_ROWS)*(ALIENS_IN_ROW):
                    self._allDead=True

    def _checkAlienPos(self):
        """
        Checks if any of the aliens have crossed the defense line.

        If aliens cross the dline, then set the corresponding class attribute
        to True
        """
        for row in self._aliens:
            for alien in row:
                if alien!=None and (alien.y-ALIEN_HEIGHT/2)<= DEFENSE_LINE:
                    self._crossdline= True
                    print(self._crossdline)
