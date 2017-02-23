# -*- coding:Utf-8 -*-

from ttk import *
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *

from mensico.tabs import Tab, TabBar
from mensico import engine


class BoardInGUI(engine.Board):
    def askForInput(self, options):
        """ Ask the user for input. """
        return [options[0], options[1]]


class MainWindow(Tk):
    """Main Window.

    User interface for selecting the program's mode:
        - Play
        - Test
    """

    def __init__(self):
        """ Creating the window. """

        # init the superclass
        Tk.__init__(self)

        # window title
        self.title(engine.VERSION + ' Mode Select')

        # Game Name
        (Label(self, text='MensIco', underline=1)
         .pack(side=TOP, padx=5, pady=5))

        # MensIco Icon
        self.icon = PhotoImage(file='data/resources/Icon.gif')
        self.iconLabel = Label(self, text='MensIco', image=self.icon)
        self.iconLabel.icon = self.icon
        self.iconLabel.pack(side=LEFT, padx=5, pady=5)

        # mode indicator variable
        self.mode = IntVar()
        self.mode.set(1)

        # radiobuttons for the modes
        (Radiobutton(self, text='Play', variable=self.mode, value=1)
         .pack(side=TOP, padx=5, pady=5))
        (Radiobutton(self, text='Test', variable=self.mode, value=2)
         .pack(side=TOP, padx=5, pady=5))

        # launch button
        (Button(self, text='Launch',
                command=lambda: self.startProgram(self.mode))
         .pack(side=TOP, padx=5, pady=5))

        # what's this button
        (Button(self, text="What's this?", command=self.printHelp)
         .pack(side=TOP, padx=5, pady=5))

        # quit button
        (Button(self, text='Quit', command=self.quit)
         .pack(side=BOTTOM, padx=5, pady=5))
        self.protocol('WM_DELETE_WINDOW', self.quit)

    def printHelp(self):
        """ Show help window."""

        # window init
        self.help = Toplevel(self)
        self.help.title(engine.VERSION + ' test results')

        # show the description
        description = open('data/resources/description.txt').read()
        Label(self.help, text=description, justify=LEFT).pack(padx=5, pady=5)

        # close button
        (Button(self.help, text='Ok', command=self.help.destroy)
         .pack(padx=5, pady=5))

        self.help.protocol('WM_DELETE_WINDOW', self.help.destroy)

    def startProgram(self, mode):
        """ Launch the program in the selected mode. """

        # if user wants to play, launch GameWindow
        if mode.get() == 1:
            GameWindow(self)
            self.withdraw()

        # else start TestWindow
        elif mode.get() == 2:
            TestWindow(self)
            self.withdraw()


class GameWindow(Tk):
    """Window application.

    Create a simple user interface for human players.
    """

    def __init__(self, parent):
        """Creating the basic overlay. """

        # set window parent
        self.parent = parent
        Tk.__init__(self)

        # create the game field
        self.game = BoardInGUI(human=1)

        # -------------------- Init: Widget variables -------------------------

        # dictionary of the coordinates on the canvas and the
        # corresponding positions in the game
        # id: [rect_x1, rect_y1, rect_x2, rect_x3]
        # id for coordinates
        self.positions = {
            1: [50, 400, 100, 450],
            2: [100, 400, 150, 450],
            3: [150, 400, 200, 450],
            4: [200, 400, 250, 450],
            5: [250, 400, 300, 450],

            6: [50, 350, 100, 400],
            7: [100, 350, 150, 400],
            8: [150, 350, 200, 400],
            9: [200, 350, 250, 400],
            10: [250, 350, 300, 400],

            11: [50, 300, 100, 350],
            12: [100, 300, 150, 350],
            13: [150, 300, 200, 350],
            14: [200, 300, 250, 350],
            15: [250, 300, 300, 350],

            16: [50, 250, 100, 300],
            17: [100, 250, 150, 300],
            18: [150, 250, 200, 300],
            19: [200, 250, 250, 300],
            20: [250, 250, 300, 300],

            21: [50, 200, 100, 250],
            22: [100, 200, 150, 250],
            23: [150, 200, 200, 250],
            24: [200, 200, 250, 250],
            25: [250, 200, 300, 250],

            26: [50, 150, 100, 200],
            27: [100, 150, 150, 200],
            28: [150, 150, 200, 200],
            29: [200, 150, 250, 200],
            30: [250, 150, 300, 200],

            31: [50, 100, 100, 150],
            32: [100, 100, 150, 150],
            33: [150, 100, 200, 150],
            34: [200, 100, 250, 150],
            35: [250, 100, 300, 150],

            36: [50, 50, 100, 100],
            37: [100, 50, 150, 100],
            38: [150, 50, 200, 100],
            39: [200, 50, 250, 100],
            40: [250, 50, 300, 100]
        }

        # own coordinates
        # id: [x, y]
        self.own_pos = {
            1: [0, 1], 2: [0, 2], 3: [0, 3], 4: [0, 4], 5: [0, 5],
            6: [1, 1], 7: [1, 2], 8: [1, 3], 9: [1, 4], 10: [1, 5],
            11: [2, 1], 12: [2, 2], 13: [2, 3], 14: [2, 4], 15: [2, 5],
            16: [3, 1], 17: [3, 2], 18: [3, 3], 19: [3, 4], 20: [3, 5],
            21: [4, 1], 22: [4, 2], 23: [4, 3], 24: [4, 4], 25: [4, 5],
            26: [5, 1], 27: [5, 2], 28: [5, 3], 29: [5, 4], 30: [5, 5],
            31: [6, 1], 32: [6, 2], 33: [6, 3], 34: [6, 4], 35: [6, 5],
            36: [7, 1], 37: [7, 2], 38: [7, 3], 39: [7, 4], 40: [7, 5]
        }

        # opponents coordinates
        # id: [x, y]
        self.opp_pos = {
            1: [7, 5], 2: [7, 4], 3: [7, 3], 4: [7, 2], 5: [7, 1],
            6: [6, 5], 7: [6, 4], 8: [6, 3], 9: [6, 2], 10: [6, 1],
            11: [5, 5], 12: [5, 4], 13: [5, 3], 14: [5, 2], 15: [5, 1],
            16: [4, 5], 17: [4, 4], 18: [4, 3], 19: [4, 2], 20: [4, 1],
            21: [3, 5], 22: [3, 4], 23: [3, 3], 24: [3, 2], 25: [3, 1],
            26: [2, 5], 27: [2, 4], 28: [2, 3], 29: [2, 2], 30: [2, 1],
            31: [1, 5], 32: [1, 4], 33: [1, 3], 34: [1, 2], 35: [1, 1],
            36: [0, 5], 37: [0, 4], 38: [0, 3], 39: [0, 2], 40: [0, 1]
        }

        # position ids
        self.ownPosition = 3
        self.oppPosition = 38
        self.ownDec = IntVar()
        self.oppDec = IntVar()

        # ---------------------- Init: Window drawing -------------------------

        # name the window
        self.title(engine.VERSION)

        # Create canvas
        self.can = Canvas(self, width=350, height=500, bg='dark green')

        # draw gamefield
        self.can.create_rectangle(50, 50, 300, 450, width=3, fill='grey')
        self.lines = [
            [50, 100, 300, 100],
            [50, 150, 300, 150],
            [50, 200, 300, 200],
            [50, 250, 300, 250],
            [50, 300, 300, 300],
            [50, 350, 300, 350],
            [50, 400, 300, 400],
            [100, 50, 100, 450],
            [150, 50, 150, 450],
            [200, 50, 200, 450],
            [250, 50, 250, 450],
            [300, 50, 300, 450]
        ]
        for line in self.lines:
            self.can.create_line(line, width=3)
        self.can.pack(side=LEFT, padx=5, pady=5)

        # draw scoreboard
        self.can.create_text(300, 10, text='H',
                             fill='red', font='Arial 14 bold')
        self.can.create_text(320, 10, text='AI',
                             fill='red', font='Arial 14 bold')
        self.can.create_text(300, 30, text=str(self.game.player2.getWins()),
                             fill='red', font='Arial 14 bold', tags='wins')
        self.can.create_text(320, 30, text=str(self.game.player1.getWins()),
                             fill='red', font='Arial 14 bold', tags='wins')

        # draw players
        self.putTri(self.ownPosition, self.oppPosition)
        # darkens the possible steps
        self.putSquares()

        # create buttons
        # step button
        self.stepButton = Button(self, text='Step', command=self.doStep)
        self.stepButton.pack(side=TOP, padx=5, pady=5)

        # "Learner" sign to separate from the step button
        Label(self, text='\n\nLearner').pack(side=TOP, padx=5, pady=5)

        # load strategy button
        self.loadButton = Button(
            self,
            text='Load',
            command=lambda: self.game.player1.loadStrategy(askopenfilename(
                filetypes=[('MensIco Strategy Files', '*.mstr')])))
        self.loadButton.pack(side=TOP, padx=5, pady=5)

        # save strategy button
        self.saveButton = Button(
            self,
            text='Save',
            command=lambda: self.game.player1.saveStrategy(asksaveasfilename(
                filetypes=[('MensIco Strategy Files', '*.mstr')])))
        self.saveButton.pack(side=TOP, padx=5, pady=5)

        # quit button
        (Button(self, text='Quit', command=self.closeAll)
         .pack(side=BOTTOM, padx=5, pady=5))
        self.protocol('WM_DELETE_WINDOW', self.closeAll)

        # reset button
        self.resetButton = Button(self, text='Reset',
                                  command=self.reset, state=['disabled'])
        self.resetButton.pack(side=BOTTOM, padx=5, pady=5)

        # mouse event handler
        self.can.bind("<Button-1>", self.putX)
        # osx fix
        self.can.bind("<Button-2>", self.putCircle)
        self.can.bind("<Button-3>", self.putCircle)

        # space also work as doStep button
        self.bind("<space>", self.doStepByButton)

    # -------------------------- Window Methods -------------------------------

    def closeAll(self):
        """ Close all remaining windows. """
        self.destroy()
        self.parent.quit()

    # ----------------------- Drawing Methods ---------------------------------

    def inside(self, x, y):
        """Returns the id for the canvas' x,y coordinates."""
        for key, value in self.positions.items():
            if x > value[0] and x < value[2] and y > value[1] and y < value[3]:
                return key

    def drawCircle(self, x, y):
        """First remove any existing circle from the canvas,
        then draw a new circle to the given coordinates. """
        # we only want 1 circle a time,
        # so remove any existing circle from the canvas
        self.can.delete('circle')
        self.can.create_oval(x + 5, y + 5, x + 45, y + 45,
                             width=5, outline='red', tags='circle')

    def drawX(self, x, y):
        """First remove any existing X from the canvas,
        then draw a new X to the given coordinates. """
        # we only want 1 X a time, so remove any existing X from the canvas
        self.can.delete('X')
        self.can.create_line(x + 5, y + 5, x + 45, y + 45,
                             width=5, fill='green', tags='X')
        self.can.create_line(x + 5, y + 45, x + 45, y + 5,
                             width=5, fill='green', tags='X')

    def drawTriangle(self, x, y, player):
        """First remove any existing triangle from the canvas,
        then draw a new one to the given coordinates."""
        # create a separate tagname for p1 and p2
        tagName = 'player' + str(player)
        # delete any previous instance
        self.can.delete(tagName)
        if player == 1:
            self.can.create_polygon(x + 25, y + 5,
                                    x + 5, y + 45,
                                    x + 45, y + 45,
                                    width=5, fill='orange', outline='black',
                                    tags=tagName)
        else:
            self.can.create_polygon(x + 5, y + 5,
                                    x + 45, y + 5,
                                    x + 25, y + 45,
                                    width=5, fill='blue', outline='black',
                                    tags=tagName)

    def drawUnitedTriangle(self, x, y):
        """First remove any existing triangle from the canvas,
        then draw a new one to the given coordinates."""
        # delete any previous instance
        self.can.delete('player1', 'player2')
        # create the two small triangles for the players
        self.can.create_polygon(x + 20, y + 5, x + 5, y + 30, x + 35, y + 30,
                                width=5, fill='orange', outline='black',
                                tags='player1')
        self.can.create_polygon(x + 30, y + 45, x + 15, y + 20, x + 45, y + 20,
                                width=5, fill='blue', outline='black',
                                tags='player2')

    def drawSquare(self, x, y):
        """ Draws a new square. """
        # draw the square
        self.can.create_rectangle(x + 1, y + 1, x + 49, y + 49,
                                  fill='snow', tags='square')

    def validX(self, id):
        """ Checks if the selected cell is valid for an X. """

        act = self.own_pos[self.ownPosition]
        next = self.own_pos[id]

        return (act[0] + 1 == next[0] and
                (act[1] + 1 == next[1] or
                 act[1] == next[1] or
                 act[1] - 1 == next[1]))

    def validCircle(self, id):
        """ Checks if the selected cell is valid for a Circle. """

        act = self.opp_pos[self.oppPosition]
        next = self.opp_pos[id]

        return (act[0] + 1 == next[0] and
                (act[1] + 1 == next[1] or
                 act[1] == next[1] or
                 act[1] - 1 == next[1]))

    def putCircle(self, event):
        """ Draw a Circle to the selected sqare. """
        # if a circle can be put here ...
        if self.validCircle(self.inside(event.x, event.y)) == 1:
            print 'click'
            # get and set our decision's id as well
            self.oppDec = self.inside(event.x, event.y)
            # get the corresponding coordinates, and draw the circle
            dest = self.positions[self.oppDec]
            self.drawCircle(dest[0], dest[1])
        else:
            print 'wrong_click'

    def putX(self, event):
        """ Draw an X to the selected sqare. """
        # if an X can be put here ...
        if self.validX(self.inside(event.x, event.y)) == 1:
            print 'click'
            # get and set our decision's id as well
            self.ownDec = self.inside(event.x, event.y)
            # get the corresponding coordinates, and draw the X
            dest = self.positions[self.ownDec]
            self.drawX(dest[0], dest[1])
        else:
            print 'wrong_click'

    def putTri(self, key_p1, key_p2):
        """ Draw the players. """
        # from ids get the coordinates
        dest_p1 = self.positions[key_p1]
        dest_p2 = self.positions[key_p2]

        # check if the players are in the same cell
        if key_p1 == key_p2:
            # draw a "united triangle constallation"
            self.drawUnitedTriangle(dest_p1[0], dest_p1[1])
        else:
            # draw separate triangles for the players
            self.drawTriangle(dest_p1[0], dest_p1[1], 1)
            self.drawTriangle(dest_p2[0], dest_p2[1], 2)

    def putSquares(self):
        """ Darkens cells for the possible steps. """

        # delete previous squares
        self.can.delete('square')
        # find all candidates:
        # create a list for them
        candidates = []

        # get current positions
        ownAct = self.own_pos[self.ownPosition]
        oppAct = self.opp_pos[self.oppPosition]

        # store the id's of the next possible steps
        candidates.append(self.find_key(self.own_pos,
                                        [ownAct[0] + 1, ownAct[1] - 1]))
        candidates.append(self.find_key(self.own_pos,
                                        [ownAct[0] + 1, ownAct[1]]))
        candidates.append(self.find_key(self.own_pos,
                                        [ownAct[0] + 1, ownAct[1] + 1]))

        # store the id's of the next possible opponent steps
        candidates.append(self.find_key(self.opp_pos,
                                        [oppAct[0] + 1, oppAct[1] - 1]))
        candidates.append(self.find_key(self.opp_pos,
                                        [oppAct[0] + 1, oppAct[1]]))
        candidates.append(self.find_key(self.opp_pos,
                                        [oppAct[0] + 1, oppAct[1] + 1]))

        # if it's a valid position, put a square there
        for candidate in candidates:
            if candidate is not None:
                act = self.positions[candidate]
                self.drawSquare(act[0], act[1])

    def find_key(self, dic, val):
        """return the key of dictionary dic given the value"""
        try:
            return [k for k, v in dic.iteritems() if v == val][0]
        except:
            return None

    # ------------------------- Game Related Methods ------------------------

    def validSetup(self):
        """ Checks if the setup is correct. """
        # if we have a circle and an X ...
        if self.can.find_withtag('circle') and self.can.find_withtag('X'):
            # get the current positions
            actOwn = self.own_pos[self.ownPosition]
            nextOwn = self.own_pos[self.ownDec]
            actOpp = self.opp_pos[self.oppPosition]
            nextOpp = self.opp_pos[self.oppDec]
            # check if the circle is in front of the current position
            # and if the X is in the right place too ...
            if ((actOwn[0] + 1 == nextOwn[0] and
                 (actOwn[1] - 1 == nextOwn[1] or
                  actOwn[1] == nextOwn[1] or
                  actOwn[1] + 1 == nextOwn[1])) and

                (actOpp[0] + 1 == nextOpp[0] and
                 (actOpp[1] - 1 == nextOpp[1] or
                  actOpp[1] == nextOpp[1] or
                  actOpp[1] + 1 == nextOpp[1]))):
                # everything is fine!
                return 1
            else:
                # Circle/X should be replaced!
                print "error!"
                print self.own_pos[self.ownPosition], self.own_pos[self.ownDec]
                print self.opp_pos[self.oppPosition], self.opp_pos[self.oppDec]
                return 0
        else:
            # Circle/X should be selected!
            # print "error! missing signs!"
            return 0

    def doStepByButton(self, event):
        self.doStep()

    # do one step!
    def doStep(self):
        """ Setup the decisions, and do one step. """
        # if it's not game over yet ...
        if not self.game.gameOver == 1:
            # and if the current setup is valid ...
            if self.validSetup() == 1:
                # the user should not save or load during a match!
                self.loadButton.configure(state=['disabled'])
                self.saveButton.configure(state=['disabled'])

                # get the coordinates from the ids
                X = self.own_pos[self.ownDec]
                Y = self.opp_pos[self.oppDec]

                options = [X, Y]

                # do one step with the 2nd type learning
                self.game.doOneStep(engine.LEARNINGTYPE, options)

                # set the positions from the result of the game.doOneStep
                self.ownPosition = self.find_key(
                    self.own_pos, self.game.player2.getOwnCoord())
                self.oppPosition = self.find_key(
                    self.opp_pos, self.game.player2.getOppCoord())

                # draw the triagles and shadings
                self.putSquares()
                self.putTri(self.ownPosition, self.oppPosition)

                # delete the cirle and the X
                self.can.delete('circle')
                self.can.delete('X')

        # if it's game over...
        if self.game.isGameOver() == 1:

            # delete scores, and shadings
            self.can.delete('wins')
            self.can.delete('square')

            # draw the new ones
            self.can.create_text(
                300, 30, fill='red', font='Arial 14 bold', tags='wins',
                text=str(self.game.player2.getWins()))
            self.can.create_text(
                320, 30, fill='red', font='Arial 14 bold', tags='wins',
                text=str(self.game.player1.getWins()))

            # set button states
            self.stepButton.configure(state=['disabled'])
            self.resetButton.configure(state=['normal'])
            self.loadButton.configure(state=['normal'])
            self.saveButton.configure(state=['normal'])

            # trolling
            if self.oppPosition in [1, 2, 3, 4, 5]:
                print 'Too bad!'

    def reset(self):
        """ Reset the game. """
        # reset the game itself
        self.game.reset()

        # set the players to their intended place
        self.ownPosition = self.find_key(self.own_pos,
                                         self.game.player2.getOwnCoord())
        self.oppPosition = self.find_key(self.opp_pos,
                                         self.game.player2.getOppCoord())
        self.putTri(self.ownPosition, self.oppPosition)

        # remove the circles and Xs, and darkens possible steps
        self.can.delete('circle')
        self.can.delete('X')
        self.putSquares()

        # configure the buttons
        self.resetButton.configure(state=['disabled'])
        self.stepButton.configure(state=['normal'])
        self.loadButton.configure(state=['normal'])
        self.saveButton.configure(state=['normal'])


# -----------------------------------------------------------------------------
# ----------------------------- TestWindow class ------------------------------
# -----------------------------------------------------------------------------
class TestWindow(Tk):
    """
    Window application.

    Create a simple user interface for testing.
    """

    def __init__(self, parent):
        """ Creating the basic overlay. """

        # The window should know its parent
        self.parent = parent
        # init the superclass
        Tk.__init__(self)
        # create the game field
        self.game = BoardInGUI()

        # title of the window
        self.title(engine.VERSION + ' tester interface')

        # option variables
        # learner (default: NULL learner)
        self.selectedLearner = IntVar(master=self)
        self.selectedLearner.set(0)
        # list of the learners for radiobuttons
        self.options = [
            'NULL learner',
            'Dummy learner',
            'Neural learner v1',
            'Neural learner v2',
            'ADABoost learner',
            'Naive Bayes learner',
        ]

        # create setup area
        # create a separate frame for the setup
        self.setupFrame = Frame(self)
        self.setupFrame.pack(side=LEFT, padx=5, pady=5)
        # create the radiobuttons
        for id, text in enumerate(self.options):
            (Radiobutton(self.setupFrame, text=text, value=id,
                         variable=self.selectedLearner)
             .pack(side=TOP, padx=5, pady=5))

        # create a scale
        self.numberOfGames = Scale(self.setupFrame,
                                   length=250,
                                   orient=HORIZONTAL,
                                   label='Number of games to play:',
                                   troughcolor='dark grey',
                                   sliderlength=20,
                                   showvalue=1,
                                   from_=1,
                                   to=10000,
                                   tickinterval=5000)
        self.numberOfGames.pack(padx=5, pady=5)

        # create buttons
        # test button
        self.testButton = Button(self, text='Test', command=self.test)
        self.testButton.pack(side=TOP, padx=5, pady=5)

        # Caption
        Label(self, text='Opponent').pack(side=TOP, padx=5)

        # Load opponent strategy button
        self.loadButton = Button(
            self,
            text='Load',
            command=lambda: self.game.player2.loadStrategy(askopenfilename(
                filetypes=[('MensIco Strategy Files', '*.mstr')])))
        self.loadButton.pack(side=TOP, padx=5)

        # Caption
        Label(self, text='\nLearner').pack(side=TOP, padx=5)

        # Reset learner button
        self.resetLearnerButton = Button(self, text='Reset',
                                         command=self.resetLearner)
        self.resetLearnerButton.pack(side=TOP, padx=5)

        # quit button
        (Button(self, text='Quit', command=self.closeAll)
         .pack(side=BOTTOM, padx=5, pady=5))
        self.protocol('WM_DELETE_WINDOW', self.closeAll)

# ---------------------- Test Window Related Methods --------------------------

    def closeAll(self):
        """ Close every remaining window. """

        # try to close the result window
        try:
            self.closeResults()
        except Exception as e:
            print e
        # close the window and quit from the main window
        self.destroy()
        self.parent.quit()

    def closeResults(self):
        """ Close results subwindow."""

        # close result window
        self.results.destroy()

        # set the scores to 0
        self.game.player1.setWins(0)
        self.game.player2.setWins(0)

        # allow the user to execute a new testrun
        self.testButton.configure(state=['normal'])

    def resetLearner(self):
        """ Reset the learner to the initial values. """
        self.game.player1.position_matrix()
        self.game.player1.opponent_matrix()

# -------------------------- Test Method -------------------------------------

    def test(self):
        """ Test with the current setup. """

        # do not click on the testButton too many times!
        self.testButton.configure(state=['disabled'])

        # get the learner type and the number of games to play
        numGam = self.numberOfGames.get()
        ltype = self.selectedLearner.get()
        matrices = self.game.getMatrices()
        # logging variables
        self.error = engine.Error(matrices[0], matrices[1],
                                  matrices[2], matrices[3], 1)
        self.error_list = []
        self.wins = []

        self.progress = Toplevel(self)
        self.progress.title('Progress')
        bar = Progressbar(self.progress, orient='horizontal', length=400)
        bar.pack(padx=5, pady=5)
        amount = 100.0 / (numGam / 100.)

        # run the test numberOfGames times
        for i in range(numGam):
            while not self.game.isGameOver():
                self.game.doOneStep(ltype)
            # log the error value and the win ratio
            if i < 150:
                self.error.calculateError()
                self.error_list.append([i, self.error.getError()])
                p1wins = self.game.player1.getWins()
                p2wins = self.game.player2.getWins()
                if p1wins + p2wins > 0:
                    self.wins.append([i, p1wins / float(p1wins + p2wins)])
                else:
                    self.wins.append([i, 0.0])
            elif i % 60 == 0:
                self.error.calculateError()
                self.error_list.append([i, self.error.getError()])
                p1wins = self.game.player1.getWins()
                p2wins = self.game.player2.getWins()
                if p1wins + p2wins > 0:
                    self.wins.append([i, p1wins / float(p1wins + p2wins)])
                else:
                    self.wins.append([i, 0.0])
            self.game.reset()
            if i % 100 == 0:
                bar.step(amount)
                self.progress.update_idletasks()

        self.progress.destroy()

        # when done with computing,
        # show the result in a pop-up window
        self.results = Toplevel(self)
        self.results.title(engine.VERSION + ' test results')

        # put the results into tabs
        bar = TabBar(self.results)

        # One tab for the probability plots
        tab_probability_plots = Tab(self.results, 'Probability plots')

        # show the selected line's probabilities for AI
        # create a Frame for the canvases
        self.results.resultPlotFrameAI = Frame(tab_probability_plots)

        # create a canvas inside the Frame for steps and for prediction
        self.results.resultPlotFrameAI.resultCanvasPos = Canvas(
            self.results.resultPlotFrameAI, width=200, height=150)
        self.results.resultPlotFrameAI.resultCanvasOpp = Canvas(
            self.results.resultPlotFrameAI, width=200, height=150)

        # draw coordinate systems
        self.drawCoordSystem(self.results.resultPlotFrameAI.resultCanvasPos,
                             'AI step probabilities')
        self.drawCoordSystem(self.results.resultPlotFrameAI.resultCanvasOpp,
                             'AI pred probabilities')

        # pack canvases
        self.results.resultPlotFrameAI.resultCanvasPos.pack(side=LEFT,
                                                            padx=5, pady=5)
        self.results.resultPlotFrameAI.resultCanvasOpp.pack(side=LEFT,
                                                            padx=5, pady=5)

        # pack the Frame for the canvases
        self.results.resultPlotFrameAI.pack(padx=5, pady=5)

        # show the selected line's probabilities for static opponent
        # create a Frame for the canvases
        self.results.resultPlotFrameOpp = Frame(tab_probability_plots)

        # create a canvas inside the Frame for steps and for prediction
        self.results.resultPlotFrameOpp.resultCanvasPos = Canvas(
            self.results.resultPlotFrameOpp, width=200, height=150)
        self.results.resultPlotFrameOpp.resultCanvasOpp = Canvas(
            self.results.resultPlotFrameOpp, width=200, height=150)

        # draw coordinate systems
        self.drawCoordSystem(self.results.resultPlotFrameOpp.resultCanvasPos,
                             'Static Opponent step probabilities')
        self.drawCoordSystem(self.results.resultPlotFrameOpp.resultCanvasOpp,
                             'Static Opponent pred probabilities')

        # pack canvases
        self.results.resultPlotFrameOpp.resultCanvasOpp.pack(side=LEFT,
                                                             padx=5, pady=5)
        self.results.resultPlotFrameOpp.resultCanvasPos.pack(side=LEFT,
                                                             padx=5, pady=5)

        # pack the Frame for the canvases
        self.results.resultPlotFrameOpp.pack(padx=5, pady=5)

        # radiobuttons for lines
        # create a new frame for them
        self.results.resultPlotRadiobuttonFrame = Frame(tab_probability_plots)

        # variable for the value
        self.results.resultPlotRadiobuttonFrame.lineNumber = IntVar(
            master=tab_probability_plots)
        self.results.resultPlotRadiobuttonFrame.lineNumber.set(1)

        # then put them into it
        for i in range(1, 9):
            Radiobutton(
                self.results.resultPlotRadiobuttonFrame,
                text=str(i), value=i, command=self.drawCurves,
                variable=self.results.resultPlotRadiobuttonFrame.lineNumber
            ).pack(side=LEFT)

        # draw the first curve
        self.results.resultPlotRadiobuttonFrame.lineNumber.set(1)
        self.drawCurves()

        # pack the frame
        self.results.resultPlotRadiobuttonFrame.pack(padx=5, pady=5)

        # log buttons in a Frame
        # create Frame
        self.results.logFrame = Frame(tab_probability_plots)
        self.results.logFrame.pack(padx=5)

        # log button for step strategy
        Button(
            self.results.logFrame, text='Log Steps!',
            command=lambda: self.game.player1.logPosMat(asksaveasfilename(
                filetypes=[('Comma Separated Values File', '*.csv')]))
        ).pack(side=LEFT, pady=5)

        # log button for prediction strategy
        Button(
            self.results.logFrame, text='Log Preds!',
            command=lambda: self.game.player1.logOppMat(asksaveasfilename(
                filetypes=[('Comma Separated Values File', '*.csv')]))
        ).pack(side=LEFT, pady=5)

        # save strategy button
        Button(
            tab_probability_plots, text='Save Strategy',
            command=lambda: self.game.player1.saveStrategy(asksaveasfilename(
                filetypes=[('MensIco Strategy Files', '*.mstr')]))
        ).pack(side=TOP, padx=5)

        # One tab for the win ratio
        tab_win_ratio = Tab(self.results, 'Win ratio')

        # create a fram for the plots
        self.results.winFrame = Frame(tab_win_ratio)

        # create canvas for the win ratio barplot and plot
        self.results.winRatioBarPlot = Canvas(self.results.winFrame,
                                              width=200, height=150)
        if len(self.wins) > 0:
            self.results.winRatioPlot = Canvas(self.results.winFrame,
                                               width=200, height=150)

        # draw coordinate system for barplot
        self.drawCoordSystem(self.results.winRatioBarPlot,
                             'AI - Static opponent win ratio')
        # draw the barplot
        self.drawWinBars(numGam)
        # pack the canvas
        self.results.winRatioBarPlot.pack(side=LEFT, padx=5, pady=5)

        # draw coordinate system for the plot, and draw curves if it's possible
        # no games play, so no plot
        if len(self.wins) == 0:
            pass
        # detailed version
        elif len(self.wins) <= 15:
            winlist = []
            for i, val in self.wins:
                winlist.append(val)
            self.drawCoordSystem(
                self.results.winRatioPlot,
                'AI - Static opponent win ratio through iterations',
                space=180. / len(self.wins),
                x_ticks=len(self.wins))
            self.drawErrorCurve(self.results.winRatioPlot,
                                winlist,
                                180. / len(self.wins))
            self.results.winRatioPlot.pack(padx=5, pady=5)
        # larger scope
        elif len(self.wins) <= 150:
            winlist = []
            for i, val in self.wins:
                winlist.append(val)
            self.drawCoordSystem(
                self.results.winRatioPlot,
                'AI - Static opponent win ratio through iterations',
                no_draw=1)
            self.drawErrorCurve(self.results.winRatioPlot,
                                winlist,
                                180. / len(self.wins),
                                110)
            self.results.winRatioPlot.pack(padx=5, pady=5)
        # show every 100th error ratio
        else:
            winlist = []
            for i, val in self.wins:
                if i % 60 == 0:
                    winlist.append(val)
            self.drawCoordSystem(
                self.results.winRatioPlot,
                'AI - Static opponent win ratio through iterations',
                no_draw=1)
            self.drawErrorCurve(self.results.winRatioPlot,
                                winlist,
                                180. / len(winlist),
                                110)
            self.results.winRatioPlot.pack(padx=5, pady=5)

        # pack the frame
        self.results.winFrame.pack(padx=5, pady=5)

        # if we have something to log, give save option to the user
        if len(self.wins) > 0:
            # Log button
            Button(tab_win_ratio, text='Log win ratio',
                   command=lambda: self.doLog(self.wins)).pack(padx=5, pady=5)

        # One for the error-level change
        tab_error_level = Tab(self.results, 'Error')
        # create a frame for the canvases
        self.results.errorFrame = Frame(tab_error_level)

        # caption on the y axis
        y_caption = '11.0'

        # scenarios regarding to iteration numbers
        # if 0 iterations happened:
        if len(self.error_list) == 0:
            # tell the user what happened
            (Label(self.results.errorFrame,
                   text='0 iterations was set, so no error output.')
             .pack(padx=5, pady=5))

        # if less than or equals to 15 rounds happened:
        elif len(self.error_list) <= 15:
            # draw a plot for the first 15 iterations
            # prepare a list for the values
            list_15 = []

            # fill up the list
            for i, val in self.error_list:
                list_15.append(val)

            # compute the correct spacing
            space = 180. / len(list_15)

            # create the plot for the first 15 iterations
            self.results.errorRatePlot15 = Canvas(self.results.errorFrame,
                                                  width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot15,
                                 'Error value in regard of iterations',
                                 y_caption, space, len(list_15))
            self.drawErrorCurve(self.results.errorRatePlot15, list_15, space)
            self.results.errorRatePlot15.pack(side=LEFT, padx=5, pady=5)

        # if less than or equals to 150 rounds happened:
        elif len(self.error_list) <= 150:
            # draw a plot for the first 15, and for the first 150 iterations

            # prepare lists for the values
            list_15 = []
            list_150 = []

            # fill up the lists
            for i, val in self.error_list:
                if i <= 15:
                    list_15.append(val)
                list_150.append(val)

            # compute the correct spacing
            space_15 = 180. / len(list_15)
            space_150 = 180. / len(list_150)

            # create the plot for the first 15 iterations
            self.results.errorRatePlot15 = Canvas(self.results.errorFrame,
                                                  width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot15,
                                 'Error value in regard of iterations',
                                 y_caption, space_15, len(list_15))
            self.drawErrorCurve(self.results.errorRatePlot15,
                                list_15, space_15)
            self.results.errorRatePlot15.pack(side=LEFT, padx=5, pady=5)

            # create the plot for the first 150 iterations
            self.results.errorRatePlot150 = Canvas(self.results.errorFrame,
                                                   width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot150,
                                 'Error value in regard of iterations',
                                 y_caption, space_150, len(list_150), 1)
            self.drawErrorCurve(self.results.errorRatePlot150,
                                list_150, space_150)
            self.results.errorRatePlot150.pack(side=LEFT, padx=5, pady=5)

        # if more than 150 rounds happened:
        else:
            # draw a plot for the first 15, the first 150,
            # and every 100th iteration

            # prepare lists for values
            list_15 = []
            list_150 = []
            list_10000 = []

            # fill up the lists
            for i, val in self.error_list:
                if i <= 15:
                    list_15.append(val)
                if i <= 150:
                    list_150.append(val)
                if i % 60 == 0:
                    list_10000.append(val)

            # compute the correct spacing
            space_15 = 180. / len(list_15)
            space_150 = 180. / len(list_150)
            space_10000 = 180. / len(list_10000)

            # create the plot for the first 15 iterations
            self.results.errorRatePlot15 = Canvas(self.results.errorFrame,
                                                  width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot15,
                                 'Error value in regard of iterations',
                                 y_caption, space_15, len(list_15))
            self.drawErrorCurve(self.results.errorRatePlot15,
                                list_15, space_15)
            self.results.errorRatePlot15.pack(side=LEFT, padx=5, pady=5)

            # create the plot for the first 150 iterations
            self.results.errorRatePlot150 = Canvas(self.results.errorFrame,
                                                   width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot150,
                                 'Error value in regard of iterations',
                                 y_caption, space_150, len(list_150), 1)
            self.drawErrorCurve(self.results.errorRatePlot150,
                                list_150, space_150)
            self.results.errorRatePlot150.pack(side=LEFT, padx=5, pady=5)

            # create the plot for every 100th iteration
            self.results.errorRatePlot10000 = Canvas(self.results.errorFrame,
                                                     width=200, height=150)
            self.drawCoordSystem(self.results.errorRatePlot10000,
                                 'Error value in regard of iterations',
                                 y_caption, space_10000, len(list_10000), 1)
            self.drawErrorCurve(self.results.errorRatePlot10000,
                                list_10000, space_10000)
            self.results.errorRatePlot10000.pack(side=LEFT, padx=5, pady=5)

        # pack the frame
        self.results.errorFrame.pack(padx=5, pady=5)

        # if we have something to log, give save option to the user
        if not len(self.error_list) == 0:
            # Log button
            Button(
                tab_error_level, text='Log error values',
                command=lambda: self.doLog(self.error_list)
            ).pack(padx=5, pady=5)

        # complete the tab system
        bar.add(tab_probability_plots)
        bar.add(tab_win_ratio)
        bar.add(tab_error_level)
        bar.show()

        # close window button
        (Button(self.results, text='Close', command=self.closeResults)
         .pack(side=BOTTOM, padx=5, pady=5))
        self.results.protocol('WM_DELETE_WINDOW', self.closeResults)

# -------------------------- Drawing methods ----------------------------------

    def drawCoordSystem(self, canvas, caption, y_caption='1.0',
                        space=25, x_ticks=7, no_draw=0):
        """ Draws a basic coordinate system. (Size: 150 x 200 (height x width))
        """

        # captions
        canvas.create_text(100, 20, text=caption, font='Arial 7')

        # draw the coordinate system
        # x axis
        canvas.create_line(10, 140, 195, 140, arrow=LAST)

        # y axis
        canvas.create_line(10, 140, 10, 10, arrow=LAST)

        if no_draw == 0:
            # ticks on x axis
            for i in range(1, x_ticks):
                canvas.create_line(10 + i * space, 135, 10 + i * space, 145)

        # ticks on y axis
        canvas.create_line(5, 30, 15, 30)

        # tick captions on y axis
        canvas.create_text(25, 30, text=y_caption, font='Arial 7')

    def drawWinBars(self, numberOfGames):
        """ Draw win bars. """

        # remove previous bars
        self.results.winRatioBarPlot.delete('bars')

        # draw x axis captions
        self.results.winRatioBarPlot.create_text(72, 147, font='Arial 7',
                                                 text='AI')
        self.results.winRatioBarPlot.create_text(127, 147, font='Arial 7',
                                                 text='Static Opponent')

        # get the heights
        if numberOfGames == 0:
            heights = [0.0, 0.0]
        else:
            p1wins = float(self.game.player1.getWins())
            p2wins = float(self.game.player2.getWins())
            heights = [p1wins / numberOfGames, p2wins / numberOfGames]

        # draw the bars
        self.results.winRatioBarPlot.create_rectangle(
            60, 140 - heights[0] * 110, 85, 140,
            outline='red', fill='red', tags='bars')
        self.results.winRatioBarPlot.create_rectangle(
            110, 140 - heights[1] * 110, 135, 140,
            outline='red', fill='red', tags='bars')

        # print results to the top of the bars
        self.results.winRatioBarPlot.create_text(
            72, 40, text=str(self.game.player1.getWins()), font='Arial 7')
        self.results.winRatioBarPlot.create_text(
            122, 40, text=str(self.game.player2.getWins()), font='Arial 7')

    def drawCurves(self):
        """ Draw the curves to the plots. """

        # remove previous curves
        self.results.resultPlotFrameAI.resultCanvasPos.delete('curve')
        self.results.resultPlotFrameAI.resultCanvasOpp.delete('curve')
        self.results.resultPlotFrameOpp.resultCanvasPos.delete('curve')
        self.results.resultPlotFrameOpp.resultCanvasOpp.delete('curve')

        # get the line number
        lineNumber = (
            self.results.resultPlotRadiobuttonFrame.lineNumber.get() - 1)
        # create a list for the curves. Stores the coordinates.
        AICurve_pos = []
        AICurve_opp = []
        OppCurve_pos = []
        OppCurve_opp = []
        # for the actual line:
        for i in range(0, 7):
            # get the x and y coordinates...
            x = 10 + i * 25
            AIY_pos = 1 - self.game.player1.getPosMatItem(lineNumber, i)
            AIY_opp = 1 - self.game.player1.getOppMatItem(lineNumber, i)
            OppY_pos = 1 - self.game.player2.getPosMatItem(lineNumber, i)
            OppY_opp = 1 - self.game.player2.getOppMatItem(lineNumber, i)
            # and append them to the list.
            AICurve_pos.append((x, AIY_pos * 140))
            AICurve_opp.append((x, AIY_opp * 140))
            OppCurve_pos.append((x, OppY_pos * 140))
            OppCurve_opp.append((x, OppY_opp * 140))

        # finally, draw the curves
        self.results.resultPlotFrameAI.resultCanvasPos.create_line(
            AICurve_pos, fill='red', smooth=1, tags='curve')
        self.results.resultPlotFrameAI.resultCanvasOpp.create_line(
            AICurve_opp, fill='red', smooth=1, tags='curve')
        self.results.resultPlotFrameOpp.resultCanvasPos.create_line(
            OppCurve_pos, fill='red', smooth=1, tags='curve')
        self.results.resultPlotFrameOpp.resultCanvasOpp.create_line(
            OppCurve_opp, fill='red', smooth=1, tags='curve')

    def drawErrorCurve(self, canvas, values, space, valueMultiplicator=10):
        """ Draw the error curves. """

        canvas.delete('curve')
        curve = []

        if len(values) == 1:
            curve.append([10, 140 - values[0] * valueMultiplicator])
            curve.append([180, 140 - values[0] * valueMultiplicator])

        else:
            for num, value in enumerate(values):
                curve.append([10 + num * space,
                              140 - value * valueMultiplicator])

        canvas.create_line(curve, fill='red', smooth=1, tags='curve')

    def doLog(self, logList):
        """ Save iterations and values from the given list to a .csv file. """

        try:
            logFileName = asksaveasfilename(
                filetypes=[('Comma Separated Values File', '*.csv')])
            logFile = open(logFileName, 'w')
        except:
            print "Can't write to", logFileName, "!"
            raise
        logFile.write("iteration; error\n")
        for i, val in logList:
            logFile.write(str(i) + '; ' + str(val) + '\n')
        logFile.close()
