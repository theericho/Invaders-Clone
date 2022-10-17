"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Eric Ho (eh643)
# December 12, 2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _hit: whether the alien has been hit by an alien bolt
    # Invariant: _hit is a bool (True or False)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getHit(self):
        """
        Returns whether there is a collision. If there is a collision between
        a bolt and ship, returns True, else False.
        """
        return self._hit

    def setHit(self,bolt):
        """
        Sets whether there is a collision with a bolt.

        Parameter bolt: A bolt that is being tested if there is a collision
        with the ship
        Precondition: bolt is a Bolt object
        """
        self._hit=self.collides(bolt)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x=GAME_WIDTH/2, y=SHIP_BOTTOM+SHIP_HEIGHT/2, \
    width=SHIP_WIDTH, height=SHIP_HEIGHT, source='ship.png', hit=False):
        """
        Initializes the ship.

        All the ship attributes are assigned.

        Parameter x: The starting x value of the ship
        Precondition: x is number (int or float)

        Parameter y: The starting y value of the ship
        Precondition: y is number (int or float)

        Parameter width: The width of the ship
        Precondition: width is number (int or float)

        Parameter height: The height of the ship
        Precondition: height is number (int or float)

        Parameter source: the image file of the ship
        Precondition: source is a string

        Parameter hit: whether or not the ship has been hit by a bolt yet
        Precondition: hit is a bool
        """
        super().__init__(x = x, y = y, width = width, height= height, \
        source=source, hit=hit)
        self._hit=hit

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if the alien bolt collides with the ship

        This method returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (self.contains((bolt.left,bolt.bottom)) or self.contains((bolt.right,\
        bolt.bottom)) or self.contains((bolt.left,bolt.top)) or self.contains((\
        bolt.right,bolt.top))) and bolt._isPbolt==False:
            return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _hit: whether the alien has been hit by a player bolt
    # Invariant: _hit is a bool (True or False)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getHit(self):
        """
        Returns whether there is a collision. If there is a collision between
        a bolt and alien, returns True, else False.
        """
        return self._hit

    def setHit(self,bolt):
        """
        Sets whether there is a collision with a bolt.

        Parameter bolt: A bolt that is being tested if there is a collision
        with the alien
        Precondition: bolt is a Bolt object
        """
        self._hit=self.collides(bolt)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, \
    source=ALIEN_IMAGES[0], hit=False):
        """
        Initializes the alien.

        All the alien attributes are assigned.

        Parameter x: The starting x value of the alien
        Precondition: x is number (int or float)

        Parameter y: The starting y value of the alien
        Precondition: y is number (int or float)

        Parameter width: The width of the alien
        Precondition: width is number (int or float)

        Parameter height: The height of the alien
        Precondition: height is number (int or float)

        Parameter source: the image file of the alien
        Precondition: source is a string

        Parameter hit: whether or not the alien has been hit by a bolt yet
        Precondition: hit is a bool
        """
        super().__init__(x = x, y = y, width = width, height= height, \
        source=source, hit=hit)
        self._hit=hit

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if (self.contains((bolt.left,bolt.bottom)) or self.contains((bolt.right,\
        bolt.bottom)) or self.contains((bolt.left,bolt.top)) or self.contains((\
        bolt.right,bolt.top))) and bolt._isPbolt==True:
            return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, red rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _isPbolt: bool indicating if bolt is from player or not
    # Invariant: _isPbolt is a bool (True or False)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getisPbolt(self):
        """
        Returns whether something is a player bolt.
        """
        return self._isPbolt

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='red',\
    linecolor='red',velocity=BOLT_SPEED):
        """
        Initializes the bolt.

        All the bolt attributes are assigned.

        Parameter x: The starting x value of the bolt
        Precondition: x is number (int or float)

        Parameter y: The starting y value of the bolt
        Precondition: y is number (int or float)

        Parameter width: The width of the bolt
        Precondition: width is number (int or float)

        Parameter height: The height of the bolt
        Precondition: height is number (int or float)

        Parameter fillcolor: The inside fill color of the bolt
        Precondition: RGB or HSV object or string of the color

        Parameter linecolor: The outline color of the bolt
        Precondition: RGB or HSV object or string of the color

        Parameter velocity: velocity of the bolt
        Precondition: velocity is a number (int or float)
        """
        super().__init__(x=x,y=y,width=width,height=height,fillcolor=fillcolor,\
        linecolor=linecolor,velocity=velocity)
        self._velocity= velocity
        self._isPbolt= self.isPlayerBolt()

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns whether something is a player bolt based on the y velocity

        If the bolt is a player bolt return True (the velocity is positive).
        Return False if not a player bolt (the velocity is negative).
        """
        if self._velocity>0:
            return True
        elif self._velocity<0:
            return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
