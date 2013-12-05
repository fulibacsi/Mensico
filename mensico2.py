# -*- coding:Utf-8 -*-
## ----- mensico2_v1.5.py -----
##
##  The program plays the game MensIco, and try to learn the opponent's
##  strategy.
##
##
##  How to run:
##      python mensico2_v1.5.py 
##
##
##  Dependencies:
##      python-2.7.2, python-tk
##
##  Optional dependencies:
##      pygame
##
##
##  Install dependencies in debian distributions:
##      sudo apt-get install python2.7 python-tk python-pygame
##
##  Install dependencies in Windows:
##      - download python 2.7 (for 32bit) from here:
##          http://python.org/ftp/python/2.7.2/python-2.7.2.msi
##      - download pygame from here (optional):
##          http://pygame.org/ftp/pygame-1.9.2a0.win32-py2.7.msi
##      - install the downloaded programs in the same order
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



from data.mensico_gui_v15 import *




# -----------------------------------------------------------------------------------------------------  
# ------------------------------------------- Main function -------------------------------------------
# -----------------------------------------------------------------------------------------------------
    

# main function  
def main():
    """ Main function. """
    
    # let's start the program!
    program = MainWindow()
    program.mainloop()

    # everything went well!
    print "ok"


# start of the program
if __name__ == '__main__':
    main()
    
