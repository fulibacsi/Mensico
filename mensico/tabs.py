###################################################
# Tabbed interface script
# www.sunjay-varma.com
###################################################

__doc__ = info = '''
This script was written by Sunjay Varma - www.sunjay-varma.com

This script has two main classes:
Tab - Basic tab used by TabBar for main functionality
TabBar - The tab bar that is placed above tab bodies (Tabs)

It uses a pretty basic structure:
root
-->TabBar(root, init_name) (For switching tabs)
-->Tab    (Place holder for content)
    \t-->content (content of the tab; parent=Tab)
-->Tab    (Place holder for content)
    \t-->content (content of the tab; parent=Tab)
-->Tab    (Place holder for content)
    \t-->content (content of the tab; parent=Tab)
etc.
'''

from Tkinter import *

BASE = RAISED
SELECTED = FLAT


class Tab(Frame):
    """base tab class"""

    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


class TabBar(Frame):
    """the bulk of the logic is in the actual tab bar"""

    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name

    def show(self):
        self.pack(side=TOP, expand=YES, fill=X)
        # switch the tab to the first tab
        self.switch_tab(self.init_name or self.tabs.keys()[-1])

    def add(self, tab):
        # hide the tab on init
        tab.pack_forget()

        # add it to the list of tabs
        self.tabs[tab.tab_name] = tab
        # basic button stuff
        b = Button(self, text=tab.tab_name, relief=BASE,
                   # set the command to switch tabs
                   command=(lambda name=tab.tab_name: self.switch_tab(name)))
        # pack the buttont to the left mose of self
        b.pack(side=LEFT)
        # add it to the list of buttons
        self.buttons[tab.tab_name] = b

    def delete(self, tabname):
        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])
        else:
            del self.tabs[tabname]

        self.buttons[tabname].pack_forget()
        del self.buttons[tabname]

    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=BASE)
            # hide the current tab
            self.tabs[self.current_tab].pack_forget()
        # add the new tab to the display
        self.tabs[name].pack(side=BOTTOM)
        # set the current tab to itself
        self.current_tab = name
        # set it to the selected style
        self.buttons[name].config(relief=SELECTED)
