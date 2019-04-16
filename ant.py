from graphics import *
from time import *
import random
import math
import threading

nb_ants = 10
x , y= 500,500
space_x = 3*x/28

turn = 10
j = ["Soldier","Farmer","Caretaker","Forager"]
job_colors = {j[0]:"#d60c20",j[1]:"#409621",j[2]:"#1ebca2",j[3]:"#bcbc1d"}

class ant():
    
    x , y= 500,500
    radius = 6
    step = 5
    
    job_count = {j[0]:0,j[1]:0,j[2]:0,j[3]:0}
    
    def __init__(self,win,pos_x,pos_y,job):

        if(pos_x<self.radius):
            self.current_x = 0 + 2*self.radius
        elif (pos_x > self.x-self.radius):
            self.current_x = self.x - 2*self.radius
        else:
            self.current_x = pos_x

        if(pos_y<3*self.y/8+self.radius):
            self.current_y = 3*y/8 + 2*self.radius
        elif (pos_y > self.y-self.radius):
            self.current_y = self.y - 2*self.radius
        else:
            self.current_y = pos_y

        self.job=job
        self.draw = Circle(Point(self.current_x,self.current_y),self.radius)
        self.draw.draw(win)
        self.draw.setFill(job_colors[self.job])

    def __eq__(self,other):
        return (self.current_x == other.current_x and
                self.current_y == other.current_y)

    def around_me(self,other):
        dx = abs(self.current_x - other.current_x)
        dy = abs(self.current_y - other.current_y)
        return ( dx <= 2*self.radius or dy <= 2*self.radius)

    def count(self,colony):
        for a in colony:
            if(self.around_me(a)):
                job_count[a.job] = job_count[a.job] + 1

    def move(self):
        dir_x = math.ceil(random.uniform(-2,1)) * self.step
        dir_y = math.ceil(random.uniform(-2,1)) * self.step
        if(dir_x+self.current_x < self.radius
           or dir_x+self.current_x > x):
            dir_x = dir_x*(-1)
        if(dir_y+self.current_y < 3*self.y/8 + self.radius
           or dir_y+self.current_y > y):
            dir_y = dir_y*(-1)
        self.draw.move(dir_x,dir_y)
        self.current_x = self.current_x + dir_x
        self.current_y = self.current_y + dir_y

class Colony():

    wait = 1

    global_job_count = {j[0]:0,j[1]:0,j[2]:0,j[3]:0}

    pos_y1 , pos_y2 = y/16 , y/4
    pos_soldier_x1,pos_soldier_x2 = x/8,x/8+space_x
    pos_farmer_x1,pos_farmer_x2 = x/8+space_x*2,x/8+space_x*3
    pos_caretaker_x1,pos_caretaker_x2 = x/8+space_x*4,x/8+space_x*5
    pos_forager_x1,pos_forager_x2 = x/8+space_x*6,x/8+space_x*7

    def build(self):
        win = GraphWin("Bouncing Ants",x,y)
        l = Line(Point(0,3*y/8),Point(x,3*y/8))
        l.setWidth(3)
        l.draw(win)

        Text(Point((self.pos_soldier_x1+self.pos_soldier_x2)/2,
                       self.pos_y1/2),j[0]).draw(win)
        Text(Point((self.pos_farmer_x1+self.pos_farmer_x2)/2,
                       self.pos_y1/2),j[1]).draw(win)
        Text(Point((self.pos_caretaker_x1+self.pos_caretaker_x2)/2,
                       self.pos_y1/2),j[2]).draw(win)
        Text(Point((self.pos_forager_x1+self.pos_forager_x2)/2,
                       self.pos_y1/2),j[3]).draw(win)

        self.soldier_t = Text(Point((self.pos_soldier_x1+self.pos_soldier_x2)/2,
                       3*self.pos_y1),str(self.global_job_count[j[0]]))
        soldier = Rectangle(Point(self.pos_soldier_x1,self.pos_y1),
                            Point(self.pos_soldier_x2,self.pos_y2))
        soldier.setFill(job_colors[j[0]])
        soldier.draw(win)

        self.farmer_t = Text(Point((self.pos_farmer_x1+self.pos_farmer_x2)/2,
                       3*self.pos_y1),self.global_job_count[j[1]])
        farmer = Rectangle(Point(self.pos_farmer_x1,self.pos_y1),
                            Point(self.pos_farmer_x2,self.pos_y2))
        farmer.setFill(job_colors[j[1]])
        farmer.draw(win)

        self.caretaker_t = Text(Point((self.pos_caretaker_x1+self.pos_caretaker_x2)/2,
                       3*self.pos_y1),self.global_job_count[j[2]])
        caretaker = Rectangle(Point(self.pos_caretaker_x1,self.pos_y1),
                            Point(self.pos_caretaker_x2,self.pos_y2))
        caretaker.setFill(job_colors[j[2]])
        caretaker.draw(win)

        self.forager_t = Text(Point((self.pos_forager_x1+self.pos_forager_x2)/2,
                       3*self.pos_y1),self.global_job_count[j[3]])
        forager = Rectangle(Point(self.pos_forager_x1,self.pos_y1),
                            Point(self.pos_forager_x2,self.pos_y2))
        forager.setFill(job_colors[j[3]])
        forager.draw(win)

        self.soldier_t.draw(win)
        self.farmer_t.draw(win)
        self.caretaker_t.draw(win)
        self.forager_t.draw(win)
        return win

    def destroy(self):
        self.win.getMouse()
        self.win.close()
        
    def __init__(self,nb_ants):
        
        self.win = self.build()
        self.nb_ants = nb_ants
        self.ants = list()
        for i in range(self.nb_ants):
            px = int(random.uniform(0,x))
            py = int(random.uniform(0,y))
            ind = int(random.uniform(0,4))
            self.ants.append(ant(self.win,px,py,j[ind]))

    def move(self,nb):
        for i in range(nb):
            for a in self.ants:
                a.move()
                sleep(self.wait/4)

    def get_count(self):
        
        for i in self.global_job_count.keys():
            self.global_job_count[i] = 0
        for a in self.ants:
            self.global_job_count[a.job] = self.global_job_count[a.job] +1 
        
    def update_count(self):
        
        self.get_count()
        
        self.soldier_t.setText(self.global_job_count[j[0]])
        self.soldier_t.undraw()
        sleep(0.1*self.wait)
        self.soldier_t.draw(self.win)

        self.farmer_t.setText(self.global_job_count[j[1]])
        self.farmer_t.undraw()
        sleep(0.1*self.wait)
        self.farmer_t.draw(self.win)

        self.caretaker_t.setText(self.global_job_count[j[2]])
        self.caretaker_t.undraw()
        sleep(0.1*self.wait)
        self.caretaker_t.draw(self.win)

        self.forager_t.setText(self.global_job_count[j[3]])
        self.forager_t.undraw()
        sleep(0.1*self.wait)
        self.forager_t.draw(self.win)


colony = Colony(nb_ants)
threading.Thread(target=colony.update_count()).start()
colony.move(10)
colony.destroy()
