# -*- coding:Utf-8 -*-

from mensico import gui


# -----------------------------------------------------------------------------------------------------
# ------------------------------------------- Main function -------------------------------------------
# -----------------------------------------------------------------------------------------------------


# main function
def main():
    """ Main function. """

    # let's start the program!
    program = gui.MainWindow()
    program.mainloop()

    # everything went well!
    print "ok"


# start of the program
if __name__ == '__main__':
    main()
