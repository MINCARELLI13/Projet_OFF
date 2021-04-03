""" File to launches the main controller file """
# coding: utf-8
from Controller.controller_main import Control


class Main:
    """ launches the main controller file """

    def __init__(self):
        self.control = Control()
        self.control.main_menu()


if __name__=='__main__':
    main = Main()
