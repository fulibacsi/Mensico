# -*- coding:Utf-8 -*-
## ----- mensico_engine_v15.py -----
##
##  The program implements the game MensIco, and some learning method to learn the opponent's
##  strategy.
##
##
##  Classes:
##      - ProbMat
##          Stores a probability matrix of a given size.
##
##      - Player
##          Implements a MensIco player.
##
##      - Board
##          Implements the game's board, players, the actions, and the learning methods as well.
##
##      - Error
##          Implements error measuring.
##
##
## Copyright (C) 2012, Fülöp, András, fulibacsi@gmail.com
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


# imports
import random
import math
from fractions import Fraction
import itertools


# -----------------------------------------------------------------------------------------------------
# ----------------------------------------- GLOBAL VARIABLES ------------------------------------------
# -----------------------------------------------------------------------------------------------------

# smallest float value to use
MINFLOAT = math.ldexp(1.0, -30)

# probability of exploring instead of exploiting
# AI - learner
# SO - static opponent
# if set to 1.0, every decision is based on the stored probabilities
# if set to 0.0, every decision is totally random
AIPROBOFEXPLORE = 1.0
SOPROBOFEXPLORE = 1.0

# learning constant
LEARNINGCONSTANT = 0.5

# type of learning
# possible values:
#    0 - no learning
#    1 - dummy learning
#    2 - neural learning v1
#    3 - neural learning v2
#    4 - adaboost learning
#    5 - naive bayes learning
LEARNINGTYPE = 2

# type of error measuring
# possible values:
#    0 - Root Mean Squared Error
#    1 - Kullback - Leibler Divergence
#    2 - Chi - Squared Divergence
#    3 - Greatest Difference
ERRORTYPE = 1

# version number
VERSION = 'MensIco2 v1.5 beta'


# -----------------------------------------------------------------------------------------------------
# ------------------------------------------- ProbMat class -------------------------------------------
# -----------------------------------------------------------------------------------------------------


class ProbMat:
    """Storing and managing probability matrices."""

    # init a probability matrix - create the matrix itself
    def __init__(self, x = 5, y = 8):
        """ Init a matrix with the given dimensions. """

        self.matrix = [[0.0 for col in range(x+2)] for row in range(y)]
        for i in range(2,len(self.matrix)):
            for j in range(1,len(self.matrix[i])-1):
                self.matrix[i][j] = 1.0/x
        self.matrix[0][(x+2)/2] = 1.0
        for i in range((x+2)/2-1, (x+2)/2+2, 1):
            self.matrix[1][i] = 0.3


    # reset a probability matrix to the initial state
    def __call__(self, x = 5, y = 8):
        """ Reset a matrix with the given dimensions to the initial state. """

        self.matrix = [[0.0 for col in range(x+2)] for row in range(y)]
        for i in range(2,len(self.matrix)):
            for j in range(1,len(self.matrix[i])-1):
                self.matrix[i][j] = 1.0/x
        self.matrix[0][(x+2)/2] = 1.0
        for i in range((x+2)/2-1, (x+2)/2+2, 1):
            self.matrix[1][i] = 0.3


# setters, getters

    # get the matrix
    def getMatrix(self):
        return self.matrix

    # set the matrix to a specified matrix - NOT CHECKING!!!
    def setMatrix(self, preset_matrix):
        self.matrix = preset_matrix[:]

    # get a specified matrix item
    def getMatrixItem(self, x, y):
        return self.matrix[x][y]

    # set a specified matrix item to a value
    def setMatrixItem(self, x, y, value):
        self.matrix[x][y] = value

# end of setters, getters


    # rescale the probability matrix
    def rescale(self, line = -1):
        """ Rescale the whole matrix, or one of the rows."""

        if line == -1:
            # we rescale the whole matrix
            for act in self.matrix:
                # get the minimum value of the current row and add a small value to it
                minimum = abs(min(act)) + MINFLOAT
                # add this to every element in the act. row
                for i in range(1,len(act)-1):
                    if not act[i] == 0.0:
                        act[i] = act[i] + minimum
                # get the total value in the row...
                summa = sum(act)
                # and divide every element by this total value
                for i in range(1,len(act)-1):
                    act[i] = act[i]/summa
        else:
            # we rescale a row
            act = self.matrix[line]
            # get the minimum value of the row and add a small value to it
            minimum = abs(min(act)) + MINFLOAT
            # add this to every element in the row
            for i in range(1,len(act)-1):
                if not act[i] == 0.0:
                    act[i] = act[i] + minimum
            # get the total value in the row...
            summa = sum(act)
            # and divide every element by this total value
            for i in range(1,len(act)-1):
                act[i] = act[i]/summa


    # log the matrix in a useable form
    def logMatrix(self, logFileName):
        """ Log the values of the matrix to the specified file."""

        try:
            logFile = open(logFileName, 'w')
        except:
            print "Can't write to", logFileName, "!"
            raise
        logFile.write("x; y; value\n")
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[i])):
                logFile.write(str(i) + '; ' + str(j) + '; ' + str(self.matrix[i][j]) + '\n')
        logFile.close()



# -----------------------------------------------------------------------------------------------------
# -------------------------------------------- Agent class --------------------------------------------
# -----------------------------------------------------------------------------------------------------


class Agent:
    """A gaming agent."""

    # init the agent
    def __init__(self, x_koord = 0, y_koord = 0, opp_x = 0, opp_y = 0, pos_mat = ProbMat(5,8), opp_mat = ProbMat(5,8)):
        self.x = x_koord
        self.y = y_koord
        self.wins = 0
        self.oppX = opp_x
        self.oppY = opp_y
        self.position_matrix = pos_mat
        self.opponent_matrix = opp_mat


# setters, getters

    # get own coordinates
    def getOwnCoord(self):
        return [self.x, self.y]

    # set own coordinates to a specified coordinate
    def setOwnCoord(self, x_koord, y_koord):
        self.x = x_koord
        self.y = y_koord

    # get opponent's coordinates
    def getOppCoord(self):
        return [self.oppX, self.oppY]

    # set opponent's coordinates to a specified coordinate
    def setOppCoord(self, x_koord, y_koord):
        self.oppX = x_koord
        self.oppY = y_koord

    # get the position matrix
    def getPosMat(self):
        return self.position_matrix.getMatrix()

    # set the position matrix to a matrix
    def setPosMat(self, dec_mat):
        self.position_matrix.setMatrix(dec_mat)

    # get a specified element from the position matrix
    def getPosMatItem(self, x, y):
        return self.position_matrix.getMatrixItem(x, y)

    # set the position matrix specified element to a value
    def setPosMatItem(self, x, y, value):
        self.position_matrix.setMatrixItem(x, y, value)

    # rescale position matrix
    def rescalePosMat(self, line = - 1):
        self.position_matrix.rescale(line)

    # get the opponent's matrix
    def getOppMat(self):
        return self.opponent_matrix.getMatrix()

    # set the opponent's matrix to a matrix
    def setOppMat(self, dec_mat):
        self.opponent_matrix.setMatrix(dec_mat)

    # get a specified element from the opponent's matrix
    def getOppMatItem(self, x, y):
        return self.opponent_matrix.getMatrixItem(x, y)

    # set the opponent's matrix specified element to a value
    def setOppMatItem(self, x, y, value):
        self.opponent_matrix.setMatrixItem(x, y, value)

    # rescale opponent's matrix
    def rescaleOppMat(self, line = - 1):
        self.opponent_matrix.rescale(line)

    # log position matrix to PosMat.csv
    def logPosMat(self, logFileName = "PosMat.csv"):
        self.position_matrix.logMatrix(logFileName)

    # log opponent's matrix to OppMat.csv
    def logOppMat(self, logFileName = "OppMat.csv"):
        self.opponent_matrix.logMatrix(logFileName)

    # get the number of wins
    def getWins(self):
        return self.wins

    # set the number of wins
    def setWins(self, value):
        self.wins = value

    # increase the number of wins
    def incWins(self):
        self.wins = self.wins + 1

# end of setters, getters


    # Save strategy to a file
    def saveStrategy(self, filename):
        """ Save probability matrices to a file. """
        try:
            outfile = open(filename,'w')
            outfile.write("# player move\n")
            for line in self.getPosMat():
                for i, elem in enumerate(line):
                    if i < len(line) - 1:
                        outfile.write(str(elem) + ', ')
                    else:
                        outfile.write(str(elem) + '\n')
            outfile.write("# player pred\n")
            for line in self.getOppMat():
                for i, elem in enumerate(line):
                    if i < len(line) - 1:
                        outfile.write(str(elem) + ', ')
                    else:
                        outfile.write(str(elem) + '\n')
            outfile.close()
            print "Saved to " + filename
        except:
            print "Could not save strategy!"



    # Load strategy from a file
    def loadStrategy(self, filename, nolog = 0):
        """ Load probability matrices from a file. """
        try:
            infile = open(filename, 'r')
            problist = infile.readlines()
            infile.close()
            temp = [[], []]
            current = -1
            actlist = temp[current]
            for line in problist:
                if line[0] == '#':
                    current += 1
                    actlist = temp[current]
                else:
                    actlist.append(map(float, line.rstrip().split(', ')))

            self.setPosMat(temp[0])
            self.setOppMat(temp[1])
            if nolog == 0:
                print "Loaded from " + filename
        except:
            print "Could not open the specified strategy file, playing default strategy!"



    # special thanks to Eli Bendersky for the Weighted random generation benchmarks!
    # http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
    def weighted_choice_sub(self, weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i



    # where should I step? Where would the opponent step?
    def decide(self, prob = 1.0):
        """ Make a decision based on probabilities. """

        # create an empty decision
        dec = []

        try:
            # create a list for the possible step's probability
            pos_list = [self.position_matrix.getMatrixItem(self.x + 1, self.y - 1) * 100, self.position_matrix.getMatrixItem(self.x + 1, self.y) * 100,\
            self.position_matrix.getMatrixItem(self.x + 1, self.y + 1) * 100]
            # and for the positions
            pos_l = [[self.x + 1, self.y - 1], [self.x + 1, self.y], [self.x + 1, self.y + 1]]
            # remove the impossible steps
            for i in range(len(pos_list) - 1, -1, -1):
                if pos_list[i] <= 0.0:
                    del pos_l[i]
                    del pos_list[i]

            # create a list for the opponent's step's probability
            opp_list = [self.opponent_matrix.getMatrixItem(self.oppX + 1, self.oppY - 1) * 100, self.opponent_matrix.getMatrixItem(self.oppX + 1, self.oppY) * 100,\
            self.opponent_matrix.getMatrixItem(self.oppX + 1, self.oppY + 1) * 100]
            # and for the positions
            opp_l = [[self.oppX + 1, self.oppY - 1], [self.oppX + 1, self.oppY], [self.oppX + 1, self.oppY + 1]]
            # remove the impossible steps
            for i in range(len(opp_list) - 1, -1, -1):
                if opp_list[i] <= 0.0:
                    del opp_l[i]
                    del opp_list[i]

        except:
            print self.x, self.y, self.oppX, self.oppY
            self.position_matrix.setMatrixItem(self.x, self.y, 'x')
            for act in self.position_matrix.getMatrix():
                print act
            self.opponent_matrix.setMatrixItem(self.oppX, self.oppY, 'x')
            for act in self.opponent_matrix.getMatrix():
                print act
            raise

        # if we don't explore the gamespace
        if(random.random() < prob):
            # create the next step based on probabilities
            dec.append(pos_l[self.weighted_choice_sub(pos_list)])
        else:
            # choose randomly
            decision = random.choice(pos_l)
            dec.append(decision)

        # if we don't explore the gamespace
        if(random.random() < prob):
            # create the opponent's next step based on probabilities
            dec.append(opp_l[self.weighted_choice_sub(opp_list)])
        else:
            # choose randomly
            decision = random.choice(opp_l)
            dec.append(decision)

        return dec


    # manually set the decision, if the setup is valid
    def setDecision(self, pos, opp):
        if self.position_matrix.getMatrixItem(pos[0], pos[1]) != 0.0 and self.opponent_matrix.getMatrixItem(opp[0], opp[1]) != 0.0:
            return [pos, opp]
        else:
            print 'Invalid positions!'
            return None


# --------------------- Learning method related misc functions -----------------------------------

    # greatest common multiply
    def gcd(self, num1, num2):
        while num2 > 0:
            num1, num2 = num2, num1 % num2
        return num1

    # least common divisor
    def lcm(self, num1, num2):
        result = num1 * num2 / self.gcd(num1, num2)
        return result


# --------------------------------- Learning methods ----------------------------------------------




    # learn from the actual step
    def learn(self, iCanStep, oppCanStep, myMove, oppMove, learningConstant, typeOfLearning):
        """ Learning from the actual step.

        Modifies the corresponding probabilities based on different learning algorithms. To maintain the
        probabilistic nature of the game's matrix, rescale the modified row.

        """

        # - 0 -
        # Learning method NULL
        # Do not learn anything!
        if typeOfLearning == 0:
            pass


        # - 1 -
        # Learning method v1
        # lame learning: modify the probability matrix by increasing / decreasing the
        # corresponding probability by 10 %
        elif typeOfLearning == 1:
            if iCanStep == 1 and oppCanStep == 1:
                # inc p1 dest, dec p1 pred
                temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * 1.1
                self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * 0.9
                self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

            elif iCanStep == 1 and oppCanStep == 0:
                # inc p1 dest, inc p1 pred
                temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * 1.1
                self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * 1.1
                self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

            elif iCanStep == 0 and oppCanStep == 1:
                # dec p1 dest, dec p1 pred
                temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * 0.9
                self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * 0.9
                self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

            elif iCanStep == 0 and oppCanStep == 0:
                # dec p1 dest, inc p1 pred
                temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * 0.9
                self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * 1.1
                self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

            # rescaling to get probabilities instead of weights
            try:
                actline = myMove[0][0]
                self.rescalePosMat(actline)
                actline = myMove[1][0]
                self.rescaleOppMat(actline)
            except:
                print myMove[0][0], myMove[1][0]
                raise


        # Learning method v2
        # neural learning: modify the probability matrix according to the backpropagation
        # learning rule -> w(k) = w(k-1) + alpha * error * SUM(x_i)
        # in this case:
        # x_i = predecessors probability
        # error = -1 if wrong, 1 in other case
        # alpha = learningConstant
        # temp = alpha * error * SUM(x_i)
        elif typeOfLearning == 2:
            try:
                if iCanStep == 1 and oppCanStep == 1:
                    # p1 dest inc, dec p1 pred
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (1) * \
                                (self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] - 1) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1]) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] + 1))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (-1) * \
                                (self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] - 1) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1]) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] + 1))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 1 and oppCanStep == 0:
                    # p1 dest inc, p1 pred inc
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (1) * \
                                (self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] - 1) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1]) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] + 1))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (1) * \
                                (self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] - 1) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1]) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] + 1))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 0 and oppCanStep == 1:
                    # dec p1 dest, dec p1 pred
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (-1) * \
                                (self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] - 1) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1]) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] + 1))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (-1) * \
                                (self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] - 1) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1]) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] + 1))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 0 and oppCanStep == 0:
                    # dec p1 dest, p1 pred inc
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (-1) * \
                                (self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] - 1) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1]) + \
                                 self.getPosMatItem(myMove[0][0] - 1, myMove[0][1] + 1))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (1) * \
                                (self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] - 1) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1]) + \
                                 self.getOppMatItem(myMove[1][0] - 1, myMove[1][1] + 1))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                # rescaling to get probabilities instead of weights
                try:
                    actline = myMove[0][0]
                    self.rescalePosMat(actline)
                    actline = myMove[1][0]
                    self.rescaleOppMat(actline)
                except:
                    print myMove[0][0], myMove[1][0]
                    raise

            except:
                print myMove
                raise


        # - 3 -
        # Learning method v3
        # neural learning v2: modify the probability matrix according to the backpropagation
        # learning rule -> w(k) = w(k-1) + alpha * error * x_previous
        # in this case:
        # x_previous = predecessor's probability
        # error = -1 if wrong, 0 in other case
        # alpha = learningConstant
        # temp = alpha * error * x_previous
        elif typeOfLearning == 3:
            try:
                if iCanStep == 1 and oppCanStep == 1:
                    # p1 dest inc, dec p1 pred
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (1) * \
                                self.getPosMatItem(self.getOwnCoord()[0],self.getOwnCoord()[1])
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (-1) * \
                                self.getOppMatItem(self.getOppCoord()[0],self.getOppCoord()[1])
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 1 and oppCanStep == 0:
                    # p1 dest inc, p1 pred inc
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (1) * \
                                self.getPosMatItem(self.getOwnCoord()[0],self.getOwnCoord()[1])
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (1) * \
                                self.getOppMatItem(self.getOppCoord()[0],self.getOppCoord()[1])
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 0 and oppCanStep == 1:
                    # dec p1 dest, dec p1 pred
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (-1) * \
                                self.getPosMatItem(self.getOwnCoord()[0],self.getOwnCoord()[1])
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (-1) * \
                                self.getOppMatItem(self.getOppCoord()[0],self.getOppCoord()[1])
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)

                elif iCanStep == 0 and oppCanStep == 0:
                    # dec p1 dest, p1 pred inc
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) + learningConstant * (-1) * \
                                self.getPosMatItem(self.getOwnCoord()[0],self.getOwnCoord()[1])
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) + learningConstant * (1) * \
                                self.getOppMatItem(self.getOppCoord()[0],self.getOppCoord()[1])
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)


                # rescaling to get probabilities instead of weights
                try:
                    actline = myMove[0][0]
                    self.rescalePosMat(actline)
                    actline = myMove[1][0]
                    self.rescaleOppMat(actline)
                except:
                    print myMove[0][0], myMove[1][0]
                    raise

            except:
                print myMove
                raise


        # - 4 -
        # Learning method v4
        # ADABoost weighting - Use a weight modification similar to ADABoost weight modification
        # To work appropriately, we have to invert the rule: If the step went well, inrease probability
        # if not, decrease probability. So we will remove the (-1) multiplicator from the equation.
        #
        # ADABoost terminology:
        # h_t(x_i) - decision
        # y(i) - real outcome
        # D_t(i) - actual weight
        # D_t+1(i) - next weight
        # epsilon_t - weighted error rate
        # Z_t - normalization factor
        # I - indicator function
        # epsilon_t = SUM_i=1^m (D_t(i) * I(y(i) = h_t(x_i)))
        # alpha_t = (1 / 2) * ln((1 - epsilon_t) / epsilon_t)
        # Z_t = SUM_i (D_t(i) * exp(-1 * alpha_t * y_i * h_t(x_i)))
        # D_t+1(i) = (D_t(i) * exp(-1 * alpha_t * y_i * h_t(x_i))) / Z_t
        #
        # implemented method:
        # - if my step was predicted:
        #       epsilon = SUM_i=1^3 (w(i))
        # - if my prediction was wrong:
        #       epsilon = w(my_pred) + w(opp_step)
        # - if epsilon < 0.5, add 0.5 to epsilon
        #       epsilon = epsilon + 0.5
        #
        # - instead of the y_i - h_t(x_i) pair, we only care about wrong elements:
        #       indicator = +1
        #
        # rescale with the same method as the other learning methods, instead of the division of Z_t
        #
        # learning rule -> w(k+1) = w(k) * exp(indicator * (1/2) * ln ((1 - epsilon) / epsilon))
        elif typeOfLearning == 4:
            try:
                if iCanStep == 1 and oppCanStep == 1:
                    # p1 dest does not change, dec p1 pred
                    epsilon = self.getOppMatItem(myMove[1][0], myMove[1][1]) + self.getOppMatItem(oppMove[0][0], oppMove[0][1])
                    if epsilon < 0.5:
                        epsilon = 0.6
                    elif epsilon >= 1.0:
                        epsilon = 0.9
                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * math.exp((1.0/2.0) * math.log(((1.0 - epsilon) / epsilon)))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)
                    # rescale
                    actline = myMove[1][0]
                    self.rescaleOppMat(actline)

                elif iCanStep == 1 and oppCanStep == 0:
                    # p1 dest does not change, p1 pred does not change
                    pass

                elif iCanStep == 0 and oppCanStep == 1:
                    # dec p1 dest, dec p1 pred
                    weights = [self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1] - 1), \
                               self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1]), \
                               self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1] + 1)]
                    epsilon = sum(weights)
                    if epsilon < 0.5:
                        epsilon = 0.6
                    elif epsilon >= 1.0:
                        epsilon = 0.9
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * math.exp((1.0/2.0) * math.log(((1.0 - epsilon) / epsilon)))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)

                    epsilon = self.getOppMatItem(myMove[1][0], myMove[1][1]) + self.getOppMatItem(oppMove[0][0], oppMove[0][1])
                    if epsilon < 0.5:
                        epsilon = 0.6
                    elif epsilon >= 1.0:
                        epsilon = 0.9
                    temp = self.getOppMatItem(myMove[1][0], myMove[1][1]) * math.exp((1.0/2.0) * math.log(((1.0 - epsilon) / epsilon)))
                    self.setOppMatItem(myMove[1][0], myMove[1][1], temp)
                    # rescale
                    actline = myMove[0][0]
                    self.rescalePosMat(actline)
                    actline = myMove[1][0]
                    self.rescaleOppMat(actline)

                elif iCanStep == 0 and oppCanStep == 0:
                    # dec p1 dest, p1 pred does not change
                    weights = [self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1] - 1), \
                               self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1]), \
                               self.getPosMatItem(self.getOwnCoord()[0] + 1, self.getOwnCoord()[1] + 1)]
                    epsilon = sum(weights)
                    if epsilon < 0.5:
                        epsilon = 0.6
                    elif epsilon >= 1.0:
                        epsilon = 0.9
                    temp = self.getPosMatItem(myMove[0][0], myMove[0][1]) * math.exp((1.0/2.0) * math.log(((1.0 - epsilon) / epsilon)))
                    self.setPosMatItem(myMove[0][0], myMove[0][1], temp)
                    # rescale
                    actline = myMove[0][0]
                    self.rescalePosMat(actline)

            except:
                print myMove
                raise


        # - 5 -
        # Learning method v5
        # Naive Bayes method based method - Estimate the probabilities based on the observations. In the beginning we assume that
        # each line is a random variable which have 5 different value, and the probability of these values follows the universal
        # distribution. During the steps we observe the outcome of our decisions, and modify our assumption.
        #
        # Naive Bayes terminology:
        #   P = N_i / N
        #   N_i - number of occurence of the i^th value
        #   N   - number of the occurences of all values
        #
        # Implemented method:
        # Initial state:
        #   All of the N_i = 1
        #   Compute the probabilities for all of the values.
        #
        # After each step:
        #   Compute the N_i, N values for the actual lines from the probabilities:
        #       From every decimal, get the fractal values
        #       Get the least common multiple to get the common denominator (N)
        #       From common denominator, get the numerators (N_i)
        #
        #   If we can step:
        #       increase the N_i for the value, where we stepped to.
        #   If we predicted the opponent's step:
        #       increase the N_i for the value, which we predicted.
        #
        #   If we couldn't step:
        #       increase the N, but only for the value, where we stepped to.
        #   If we missed the opponent's step:
        #       increase the N, but only for the value, which we predicted.
        #
        # def learn(self, iCanStep, oppCanStep, myMove, oppMove, learningConstant, typeOfLearning)
        elif typeOfLearning == 5:
            try:

            # create lists
                # create a list for the possible steps
                steps = []
                steps_index = []
                # first element: actual step
                steps.append(self.getPosMatItem(myMove[0][0], myMove[0][1]))
                steps_index.append(0)
                # if existst, add the element on the left
                if not self.getPosMatItem(myMove[0][0], myMove[0][1] - 1) == 0.0:
                    steps.append(self.getPosMatItem(myMove[0][0], myMove[0][1] - 1))
                    steps_index.append(-1)
                # if exists, add the element on the right
                if not self.getPosMatItem(myMove[0][0], myMove[0][1] + 1) == 0.0:
                    steps.append(self.getPosMatItem(myMove[0][0], myMove[0][1] + 1))
                    steps_index.append(+1)

                # create a list for the possible preds
                preds = []
                preds_index = []
                # first element: actual pred
                preds.append(self.getOppMatItem(myMove[1][0], myMove[1][1]))
                preds_index.append(0)
                # if existst, add the element on the left
                if not self.getOppMatItem(myMove[1][0], myMove[1][1] - 1) == 0.0:
                    preds.append(self.getOppMatItem(myMove[1][0], myMove[1][1] - 1))
                    preds_index.append(-1)
                # if exists, add the element on the right
                if not self.getOppMatItem(myMove[1][0], myMove[1][1] + 1) == 0.0:
                    preds.append(self.getOppMatItem(myMove[1][0], myMove[1][1] + 1))
                    preds_index.append(+1)

            # get the fractal values
                # create two temporary list for steps and for pred
                temp_step = []
                temp_pred = []

                # get the fractions, and put them into the temp. lists
                for elem in steps:
                    temp_step.append(Fraction(elem))

                for elem in preds:
                    temp_pred.append(Fraction(elem))

                # get least common multiples
                lcm_step = temp_step[0].denominator
                if len(temp_step) == 3:
                    lcm_step = self.lcm(lcm_step, self.lcm(temp_step[1].denominator, temp_step[2].denominator))
                elif len(temp_step) == 2:
                    lcm_step = self.lcm(lcm_step, temp_step[1].denominator)

                lcm_pred = temp_pred[0].denominator
                if len(temp_pred) == 3:
                    lcm_pred = self.lcm(lcm_pred, self.lcm(temp_pred[1].denominator, temp_pred[2].denominator))
                elif len(temp_pred) == 2:
                    lcm_pred = self.lcm(lcm_pred, temp_pred[1].denominator)

            # modify values according the outcome
                if iCanStep == 1 and oppCanStep == 1:
                    # inc p1 step, dec p1 pred
                    temp_step[0] = Fraction(int(temp_step[0].numerator * 1.1), temp_step[0].denominator)
                    temp_pred[0] = Fraction(temp_pred[0].numerator, int(temp_pred[0].denominator * 1.1))

                elif iCanStep == 1 and oppCanStep == 0:
                    # inc p1 step, inc p1 pred
                    temp_step[0] = Fraction(int(temp_step[0].numerator * 1.1), temp_step[0].denominator)
                    temp_pred[0] = Fraction(int(temp_pred[0].numerator * 1.1), temp_pred[0].denominator)

                elif iCanStep == 0 and oppCanStep == 1:
                    # dec p1 step, dec p1 pred
                    temp_step[0] = Fraction(temp_step[0].numerator, int(temp_step[0].denominator * 1.1))
                    temp_pred[0] = Fraction(temp_pred[0].numerator, int(temp_pred[0].denominator * 1.1))

                elif iCanStep == 0 and oppCanStep == 0:
                    # dec p1 step, inc p1 pred
                    temp_step[0] = Fraction(temp_step[0].numerator, int(temp_step[0].denominator * 1.1))
                    temp_pred[0] = Fraction(int(temp_pred[0].numerator * 1.1), temp_pred[0].denominator)


            # convert fractions back
                steps = []
                for elem in temp_step:
                    steps.append((float(elem.numerator) * float(lcm_step)/float(elem.denominator))/float(lcm_step))

                preds = []
                for elem in temp_pred:
                    preds.append((float(elem.numerator) * float(lcm_pred)/float(elem.denominator))/float(lcm_pred))


                # setposmatitems
                for id, elem in enumerate(steps):
                    self.setPosMatItem(myMove[0][0], myMove[0][1] + steps_index[id], elem)
                # setoppmatitems
                for id, elem in enumerate(preds):
                    self.setOppMatItem(myMove[1][0], myMove[1][1] + preds_index[id], elem)

                # rescale
                actline = myMove[0][0]
                self.rescalePosMat(actline)
                actline = myMove[1][0]
                self.rescaleOppMat(actline)

            except:
                print myMove
                raise


        # - 6 -
        # Learning method v6
        # Gradient Descent method
        # based on KLDiv: KLDiv(P, Q) = p_i * ln(p_i / q_i)
        # from here we get: F(x) = x * ln(x / y)
        # so the learning rule is:
        #   w(k+1) = w(k) - gamma * (ln(w(k) / y) + 1)
        elif typeOfLearning == 6:
            try:
                raise NotImplementedError('Learning method not yet implemented!')
            except:
                print myMove
                raise

        else:
            print 'There\'s no such learning method!\nRead the documentation for details!'
            raise



# -----------------------------------------------------------------------------------------------------
# -------------------------------------------- Board class --------------------------------------------
# -----------------------------------------------------------------------------------------------------


class Board:
    """GameBoard - Plays the game."""


    # init the game
    def __init__(self, size_x = 5, size_y = 8, beta = 0.5, human = 0):
        self.beta = beta
        self.sizeX = size_x
        self.sizeY = size_y
        self.round = 0
        self.gameOver = 0
        self.player1 = Agent(0, self.sizeX / 2 + 1, 0, self.sizeX / 2 + 1, ProbMat(self.sizeX, self.sizeY), ProbMat(self.sizeX, self.sizeY))
        self.player2 = Agent(0, self.sizeX / 2 + 1, 0, self.sizeX / 2 + 1, ProbMat(self.sizeX, self.sizeY), ProbMat(self.sizeX, self.sizeY))
        self.human = human


# --------------------------------- Information methods ----------------------------------------------


    # show some info about the current round
    def showRound(self):
        """ Print out informations about the current round. """

        print self.round, ". round:\nplayer 1:\nx: ", self.player1.getOwnCoord()[0], "\ny: ", self.player1.getOwnCoord()[1], "\n\nplayer 2:\nx: ", \
              self.player2.getOwnCoord()[0], "\ny: ", self.player2.getOwnCoord()[1]


    # returns the players' matrices
    def getMatrices(self):
        return [self.player1.getPosMat(), self.player1.getOppMat(), self.player2.getPosMat(), self.player2.getOppMat()]



    # show some info about the game
    def showAll(self):
        """ Show all relevant info about the game(s). """

        # size of the board
        print self.sizeX, "x", self.sizeY
        # the current round's number
        print "#", self.round
        # the current coordinates of the players
        print "p1: ", self.player1.getOwnCoord()
        for act in self.player1.getPosMat():
            print act
        print "\n"
        print "p2: ", self.player1.getOppCoord()
        for act in self.player1.getOppMat():
            print act
        # the number of wins
        print "p1 Wins: ", self.player1.getWins()
        print "p2 Wins: ", self.player2.getWins()


    # Returns all important info in one string
    def getResults(self):
        result_list = []
        result_list.append('AI Step matrix:\n')
        for act in self.player1.getPosMat():
            result_list.append(str(act) + '\n')
        result_list.append('\nAI Prediction matrix:\n')
        for act in self.player1.getOppMat():
            result_list.append(str(act) + '\n')
        result_list.append('\nAI wins: ' + str(self.player1.getWins()) + '\nOpp wins: ' + str(self.player2.getWins()))
        return ''.join(result_list)



# --------------------------------- GamePlay methods ----------------------------------------------


    # Returns if it is game over
    def isGameOver(self):
        """ Is it game over already? """

        if self.gameOver == 1:
            return 1
        else:
            return 0



    # Ask for the next step. User should input the next step's coordinates and the prediction's coordinates
    # !!! For heritage purpose !!!
    def askForInput(self, options):
        """ Ask the user for input. """
        # implement your own input method!
        pass



    def avalaibleSteps(self, player):
        """ Returns the avalaible steps and predictions. """
        posX = player.getOwnCoord()[0]
        posY = player.getOwnCoord()[1]

        oppX = player.getOppCoord()[0]
        oppY = player.getOppCoord()[1]

        pos_list = []
        opp_list = []

        for y in [posY - 1, posY, posY + 1]:
            if y < (self.sizeX + 1) and y > 0:
                pos_list.append([posX + 1, y])

        for y in [oppY - 1, oppY, oppY + 1]:
            if y < self.sizeX + 1 and y > 0:
                opp_list.append([oppX + 1, y])

        return [pos_list, opp_list]



    # do one step in the game
    def doOneStep(self, learningType = 0, options = None):
        """
        Play one step.

        The method play one step of the game. Check if it's game over, then ask the players to decide their
        next step, then moves the players according their decisions. The player1 is learning from it's mis-
        takes. The type of learning can be modified.

        """

        if self.gameOver == 1:
            print "Already Game Over!"
            return

        # let the players decide on their own...
        player1move = self.player1.decide(AIPROBOFEXPLORE)
        # if there's a human player, ask for the next step...
        if self.human == 1:
            dec = self.askForInput(options)
            player2move = self.player2.setDecision(dec[0], dec[1])
        # if it's an artificial opponent, it should decide on its own...
        elif self.human == 0:
            player2move = self.player2.decide(SOPROBOFEXPLORE)
        playersmove = [1, 1]

        # let's see the results
        if player2move[1] == player1move[0]:
            playersmove[0] = 0
        if player1move[1] == player2move[0]:
            playersmove[1] = 0

        # both player steps
        if playersmove == [1, 1]:
            self.player1.learn(1, 1, player1move, player2move, LEARNINGCONSTANT, learningType)
            self.player1.setOwnCoord(player1move[0][0], player1move[0][1])
            self.player1.setOppCoord(player2move[0][0], player2move[0][1])
            self.player2.setOwnCoord(player2move[0][0], player2move[0][1])
            self.player2.setOppCoord(player1move[0][0], player1move[0][1])

        # only the first player steps
        elif playersmove == [1, 0]:
            self.player1.learn(1, 0, player1move, player2move, LEARNINGCONSTANT, learningType)
            self.player1.setOwnCoord(player1move[0][0], player1move[0][1])
            self.player2.setOppCoord(player1move[0][0], player1move[0][1])

        # only the second player steps
        elif playersmove == [0, 1]:
            self.player1.learn(0, 1, player1move, player2move, LEARNINGCONSTANT, learningType)
            self.player1.setOppCoord(player2move[0][0], player2move[0][1])
            self.player2.setOwnCoord(player2move[0][0], player2move[0][1])

        # nobody steps
        elif playersmove == [0, 0]:
            self.player1.learn(0, 0, player1move, player2move, LEARNINGCONSTANT, learningType)


        # next round!
        self.round = self.round + 1


        # Game Over?
        # player 1 wins!
        if self.player1.getOwnCoord()[0] == self.sizeY - 1 and not self.player2.getOwnCoord()[0] == self.sizeY - 1:
            self.player1.incWins()
            self.gameOver = 1

        # player 2 wins!
        elif not self.player1.getOwnCoord()[0] == self.sizeY - 1 and self.player2.getOwnCoord()[0] == self.sizeY - 1:
            self.player2.incWins()
            self.gameOver = 1

        # Draw!
        elif self.player1.getOwnCoord()[0] == self.sizeY - 1 and self.player2.getOwnCoord()[0] == self.sizeY - 1:
            self.gameOver = 1



    # reset game state
    def reset(self):
        """ Reset the game. """

        # set gameOver to 0
        self.round = 0
        self.gameOver = 0

        # set players to init positions
        self.player1.setOwnCoord(0, self.sizeX / 2 + 1)
        self.player1.setOppCoord(0, self.sizeX / 2 + 1)
        self.player2.setOwnCoord(0, self.sizeX / 2 + 1)
        self.player2.setOppCoord(0, self.sizeX / 2 + 1)





# stores and calculates error
class Error:
    """ Stores and calculates error between two MensIco player. """

    # init
    def __init__(self, P_Pos = None, P_Opp = None, Q_Pos = None, Q_Opp = None, typeOfError = 0):
        self.P_Pos = P_Pos
        self.P_Opp = P_Opp
        self.Q_Pos = Q_Pos
        self.Q_Opp = Q_Opp
        self.value = None
        self.typeOfError = typeOfError

# setters, getters

    def getError(self):
        return self.value

    def resetError(self):
        self.value = None

    def getTypeOfError(self):
        return self.typeOfError

    def setTypeOfError(self, value):
        if value >= 0 and value <= 2 and type(value) == type(1):
            self.typeOfError = value

# error calculation methods

    # measure the difference between the optimal and actual probabilities
    def getRMSE(self):
        """ Calculate RMSE between the optimal and actual probabilities. """

        rmse = 0.0

        # difference of the prediction's probability and the opponent's step's probability
        for p1, p2 in itertools.izip(self.P_Opp, self.Q_Pos):
            for elem1, elem2 in itertools.izip(p1, p2):
                rmse += math.sqrt((elem2 - elem1)**2)

        # help variable
        act = 0
        # difference of the step's probability and the opponent's prediction's probability
        for p1, p2 in itertools.izip(self.P_Pos, self.Q_Opp):
            # if it's not the first row:
            if not act == 0:
                # create a copy of the opponent's pred matrix's actual line
                temp = p2[:]
                # get the 1.0 - value, because we want to do the opposite
                # of the opponent's prediction
                for i in range(0, len(temp)):
                    if not temp[i] == 0.0:
                        temp[i] = 1.0 / temp[i]

                # rescale it back to sum = 1.0
                temp_summa = sum(temp)
                for i in range(0, len(temp)):
                    temp[i] = temp[i] / temp_summa

                # get the differences
                for elem1, elem2 in itertools.izip(p1, temp):
                    rmse += math.sqrt((elem2 - elem1)**2)

            # we're not in the first row anymore!
            act += 1

        return rmse / 2.0



    # measure the Kullback-Leibler divergence between the optimal and actual probabilities
    #
    # Kullback-Leibler divergence: div(p, q) = sum_i^N p_i * ln(p_i / q_i)
    #
    def getKLDiv(self):
        """ Calculate the Kullback-Leibler divergence between the optimal and actual probabilities. """

        kldiv = 0.0

        # difference of the prediction's probability and the opponent's step's probability
        for p1, p2 in itertools.izip(self.P_Opp, self.Q_Pos):
            for elem1, elem2 in itertools.izip(p1, p2):
                if not elem2 == 0.0 and not elem1 == 0.0:
                    kldiv += elem1 * math.log(elem1 / elem2)

        # help variable
        act = 0
        # difference of the step's probability and the opponent's prediction's probability
        for p1, p2 in itertools.izip(self.P_Pos, self.Q_Opp):
            # if it's not the first row:
            if not act == 0:
                # create a copy of the opponent's pred matrix's actual line
                temp = p2[:]
                # get the 1.0 - value, because we want to do the opposite
                # of the opponent's prediction
                for i in range(0, len(temp)):
                    if not temp[i] == 0.0:
                        temp[i] = 1.0 / temp[i]

                # rescale it back to sum = 1.0
                temp_summa = sum(temp)
                for i in range(0, len(temp)):
                    temp[i] = temp[i] / temp_summa

                # get the differences
                for elem1, elem2 in itertools.izip(p1, temp):
                    if not elem2 == 0.0 and not elem1 == 0.0:
                        kldiv += elem1 * math.log(elem1 / elem2)


            # we're not in the first row anymore!
            act += 1

        return kldiv / 2.0



    # measure the Kullback-Leibler divergence between the optimal and actual probabilities
    #
    # Chi-Square divergence: div(p, q) = sum_i^N (p_i - q_i)^2 / q_i
    #
    def getChiSquareDiv(self):
        """ Calculate the Chi square divergence between the optimal and actual probabilities. """

        chiSquareDiv = 0.0

        # difference of the prediction's probability and the opponent's step's probability
        for p1, p2 in itertools.izip(self.P_Opp, self.Q_Pos):
            for elem1, elem2 in itertools.izip(p1, p2):
                if not elem2 == 0.0:
                    chiSquareDiv += ((elem1 - elem2)**2) / elem2

        # help variable
        act = 0
        # difference of the step's probability and the opponent's prediction's probability
        for p1, p2 in itertools.izip(self.P_Pos, self.Q_Opp):
            # if it's not the first row:
            if not act == 0:
                # create a copy of the opponent's pred matrix's actual line
                temp = p2[:]
                # get the 1.0 - value, because we want to do the opposite
                # of the opponent's prediction
                for i in range(0, len(temp)):
                    if not temp[i] == 0.0:
                        temp[i] = 1.0 / temp[i]

                # rescale it back to sum = 1.0
                temp_summa = sum(temp)
                for i in range(0, len(temp)):
                    temp[i] = temp[i] / temp_summa

                # get the differences
                for elem1, elem2 in itertools.izip(p1, temp):
                    if not elem2 == 0.0:
                        chiSquareDiv += ((elem1 - elem2)**2) / elem2

            # we're not in the first row anymore!
            act += 1

        return chiSquareDiv / 2.0

    # Calculate the greatest difference between the opponent's and the player's matrices.
    #   a) (max_i(P_Opp(i)) - Q_Pos(i)) + (max_i(Q_Pos(i)) - P_Opp(i)) - because we want to minimize the difference
    #   b) 1 / ((max_i(P_Pos(i)) - Q_Opp(i)) + (max_i(Q_Opp(i)) - P_Pos(i))) - because we want to maximize the difference
    def getGreatestDifference(self):
        """ Returns the greatest difference between the two player's matrices. """

        error = 0.0

        # calculate the difference between maximum value of the player's maximum value
        # and the opponent's value on the same tile and vice versa
        for P_line, Q_line in itertools.izip(self.P_Opp, self.Q_Pos):
            error += float((max(P_line) - Q_line[P_line.index(max(P_line))]) + (max(Q_line) - P_line[Q_line.index(max(Q_line))]))

        # calculate the inverse of the difference between maximum value of the player's maximum value
        # and the opponent's value on the same tile and vice versa
        for P_line, Q_line in itertools.izip(self.P_Pos, self.Q_Opp):
            temp = float((max(P_line) - Q_line[P_line.index(max(P_line))]) + (max(Q_line) - P_line[Q_line.index(max(Q_line))]))
            if not temp == 0:
                error += temp

        return error / 2.0

    # calculates the error value
    def calculateError(self):
        """
        Set the error value to the error calculated by the selected type of divergence.

        Possible divergences:
        0 - Root Mean Squared Error
        1 - Kullback - Leibler Divergence
        2 - Chi-Squared Divergence.
        3 - Greatest Difference
        """
        if self.typeOfError == 0:
            self.value = self.getRMSE()
        elif self.typeOfError == 1:
            self.value = self.getKLDiv()
        elif self.typeOfError == 2:
            self.value = self.getChiSquareDiv()
        elif self.typeOfError == 3:
            self.value = self.getGreatestDifference()
        else:
            print 'Error calculation error!'
            raise




