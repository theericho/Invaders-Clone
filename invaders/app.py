"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Eric Ho (eh643)
# December 12, 2019
"""
from consts import *
from game2d import *
from wave import *
import numpy as np


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _lastkey_s: if s was previously pressed; If pressed, then True.
    # Invariant: _lastkey_s is a bool

    # Attribute _wavecounter: number of waves completed
    # Invariant: _wavecounter is an int >=0

    # Attribute _scoretotal: total score over the wave(s)
    # Invariant: _scoretotal is an int>=0

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state=STATE_INACTIVE
        self._wavecounter=0
        self._scoretotal=0
        start_text="Press 'S' to Play"
        self._lastkey_s = False
        self._text = GLabel(text=start_text,font_size=70, \
        font_name='Arcade.ttf',left=140,bottom=350)

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state== STATE_INACTIVE:
            self._checkStartState()
        self._startgame()
        if self._state==STATE_ACTIVE:
            self._checkWin()
            self._checkCross()
            self._addScore()
            self._showLivesWave()
            self._wave.update(self.input,dt)
            self._stateShip()
        if self._state== STATE_PAUSED:
            self._checkPaused()
        if self._state==STATE_CONTINUE:
            self._wave.update(self.input,dt)
            self._state=STATE_ACTIVE

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        if self._state==STATE_INACTIVE:
            self._text.draw(self.view)
        if self._state==STATE_ACTIVE:
            self._wave.draw(self.view)
            self._text.draw(self.view)
        if self._state==STATE_PAUSED:
            self._wave.draw(self.view)
            self._text.draw(self.view)
        if self._state==STATE_CONTINUE:
            self._wave.draw(self.view)
        if self._state==STATE_COMPLETE:
            self._text.draw(self.view)


    # HELPER METHODS FOR THE STATES GO HERE
    def _checkStartState(self):
        """
        Changes the current state to STATE_NEWWAVE if 's' is pressed

        This method checks for a key press of 's', and if there is one, changes
        the state to STATE_NEWWAVE.  A key press is when a key is pressed for
        the FIRST TIME. We do not want the state to continue to change as we
        hold down the key.
        """
        #modified from the given example _determineState helper method in state.py
        pressed_s = self.input.is_key_down('s')
        change = pressed_s is True and self._lastkey_s is False
        if change:
            self._state = STATE_NEWWAVE
        self._lastkey_s= pressed_s

    def _startgame(self):
        """
        Initializes new Wave object and changes current state to STATE_ACTIVE

        This initalization of Wave object and state change only happens if
        the current state is STATE_NEWWAVE
        """
        if self._state==STATE_NEWWAVE:
            self._wave=Wave(wavecounter=self._wavecounter,score=self._scoretotal)
            self._state=STATE_ACTIVE

    def _stateShip(self):
        """
        Changes state to STATE_PAUSED or STATE_ COMPLETE based on lives left

        Gets the number of lives remaining in the Wave and whether or not the
        game should be paused using a getter and change. A string of the
        corresponding text for the game is assigned to self._text.
        """
        reset_text="Lives: "+str(self._wave.getLives())+", Press 'S' to Continue"
        dead_text="Lives: 0, Game Over"
        if self._wave.getLives()>0 and self._wave.getPause()==True:
            self._state=STATE_PAUSED
            self._text=GLabel(text=reset_text,font_size=50, \
            font_name='Arcade.ttf',left=60,bottom=350)
            self._wave.setPause(False)
        if self._wave.getLives()==0 and self._wave.getPause()==True:
            self._state=STATE_COMPLETE
            self._text=GLabel(text=dead_text,font_size=70, \
            font_name='Arcade.ttf',left=100,bottom=350)

    def _checkPaused(self):
        """
        Changes state to STATE_CONTINUE if 's' is pressed

        This method checks for a key press of 's', and if there is one, changes
        the state to STATE_CONTINUE.  A key press is when a key is pressed for
        the FIRST TIME.
        """
        #modified from the given example _determineState helper method in state.py
        pressed_s = self.input.is_key_down('s')
        change = pressed_s is True and self._lastkey_s is False
        if change:
            self._state = STATE_CONTINUE
        self._lastkey_s= pressed_s

    def _checkWin(self):
        """
        State changed to STATE_NEWWAVE if all aliens are dead.

        If all aliens are dead, increase the wavecounter and make a new wave.
        """
        if self._wave.getAllDead()==True:
            self._wavecounter+=1
            self._state=STATE_NEWWAVE

    def _checkCross(self):
        """
        State changed to STATE_COMPLETE if aliens cross the defense line.
        Corresponding text is assigned to self._text to reflect that the player
        lost the game.
        """
        breach_text="Aliens breached defenses.\n Game Over"
        if self._wave.getcrossdline()==True:
            self._state=STATE_COMPLETE
            self._text=GLabel(text=breach_text,font_size=50, \
            font_name='Arcade.ttf',left=100,bottom=350)

    def _showLivesWave(self):
        """
        Show the amount of ship lives left and the wave the player is on.

        This shows the waves starting from 1.
        """
        lives_text="Lives: "+str(self._wave.getLives())+"   Wave: "+\
        str(self._wavecounter+1)+"   Points: "+str(self._scoretotal)
        self._text=GLabel(text=lives_text,font_size=50, \
        font_name='Arcade.ttf',left=20,bottom=630)

    def _addScore(self):
        """
        Set the current running total of points the player accumulated.

        Set the class attribute in wave.py to False to know when to update score
        again.
        """
        if self._wave.getjustKilled()==True:
            self._scoretotal=self._wave.getscore()
            self._wave.setjustKilled(False)
