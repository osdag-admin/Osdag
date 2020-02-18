'''
Created on 18-Nov-2016

@author: deepa
'''


from cad.common_logic import CommonDesignLogic



class cadconnection(object):


    def commonfile(self, mainmodule, display, folder, module):
        self.display = display
        self.module = module
        self.mainmodule = mainmodule
        self.folder = folder

        if self.mainmodule == "Shear Connection":
            self.commLogicObj = CommonDesignLogic(self.display, self.folder,
                                                  self.module,self.mainmodule)
        elif self.mainmodule == "Moment Connection":
            self.commLogicObj = CommonDesignLogic(self.display, self.folder,
                                                  self.module,self.mainmodule)

        return self.commLogicObj
