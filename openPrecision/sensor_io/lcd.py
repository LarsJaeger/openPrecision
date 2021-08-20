import time

import qwiic_serlcd


class LCD(qwiic_serlcd.QwiicSerlcd):

    def __init__(self):
        super().__init__()
        if not super().connected:
            raise IOError("The Qwiic SerLCD device isn't connected to the system. Please check your connection")
        self.begin()
        # new default settings
        self.disableSystemMessages()
        self.noautoscroll()
        self.disableSplash()
        self.setBacklight(110, 240, 100)
        self.noCursor()
        self.setContrast(0)
        self.clearScreen()
