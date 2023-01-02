from direct.gui.DirectGui import DirectFrame, OnscreenText
from panda3d.core import *

from panda3d.core import LVector3
from direct.showbase.ShowBase import ShowBase

import random

class Wrapper:
    def __init__(self):
        self.b = ShowBase()
        self.x_pos=0
        self.direction=0
        self.lost=False
        self.moving_frame=None
        
    def main(self):
        fac=0.02
        fac2=0.05
        w_value=0.5
        
        if self.x_pos==0:
            r=random.random()-0.5
            self.x_pos=fac*r
        diff=self.x_pos
        
        self.x_pos*=1.01 #increase
        
        self.x_pos+=fac2*self.direction # move back
        if self.x_pos > w_value:
            self.lost=True
            self.clean()
            print(self.x_pos)
            print("you lost")
            
        if self.x_pos < -w_value:
            self.lost=True
            self.clean()
            print(self.x_pos)
            print("you lost")
        if self.moving_frame!=None:
            self.moving_frame.setPos((self.x_pos,0,0))
    
    def clean(self):
        for x in self.elements:
            x.removeNode()
        self.elements=[]
        self.moving_frame=None
    
    def build(self):
        self.elements=[]
        color=(0.8,0.8,0.8,1)
        
        fac=1/5
        fsfloat=0.05
                
        frame_size=(-0.5,0.5,-fsfloat,fsfloat)
        print(frame_size)
        basic={"frameColor":color,"frameSize":frame_size,"pos":(0,0,0),"color":LVector3(0,0,255)}
        f1=DirectFrame(**basic)
        
        frame_size=(-fsfloat,fsfloat,-fsfloat*2,fsfloat*2)
        basic={"frameColor":color,"frameSize":frame_size,"pos":(0,0,0)}
        self.moving_frame=DirectFrame(**basic)
        
        self.elements=[f1,self.moving_frame]
        
        self.b.taskMgr.add(self.key_watch_task,"keywatchstask",extraArgs=[self],appendTask=True)
        
    def key_watch_task(self,*args):
        Task=args[1]
        is_down = self.b.mouseWatcherNode.is_button_down
        my_d={"a":-1,"d":1}
        any_down=False
        for key in ["a","d"]:
            nkey=key.encode()
            check_this=KeyboardButton.ascii_key(nkey)
            if is_down(check_this):
                self.direction=my_d[key]
                any_down=True
        if not any_down:
            self.direction=0
            
        return Task.cont
    
def main():
    W = Wrapper()
    W.build()
    while True:
        if not W.lost:
            W.main()
            
        W.b.taskMgr.step()
        if W.lost and W.elements==[]:
            pos=(0,0,0)
            T=OnscreenText(text="you lost", 
                            scale=0.2,
                            pos=pos,
                            fg=(0,0,0, 1),
                            shadow=(1,1,1, 0.5))
            T.reparent_to(W.b.render2d)

if __name__ == "__main__":
    main()
