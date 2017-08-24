import tkinter
import threading

import rat


class Maze(object):
    color_map = rat.Rat.color_map
    def __init__(self):
        self.maze = []
        self.scale = 25
        self.root = tkinter.Tk()
        self.canvas = None
        self.width = 0
        self.height = 0

    def loadMaze(self, file_name):
        my_file = open(file_name, "r")
        i = 0
        for ln in my_file:
            #convert line into a list, minus the newline.
            self.maze.append(list(filter(lambda c: c!= "\n", ln)))
            i=i+1

        self.height = self.maze.__len__()
        self.width = self.maze[0].__len__()
        print (f" Maze with dimensions [{self.width} X {self.height}] loaded")
        self.canvas = tkinter.Canvas(self.root, bg="white", height = self.maze.__len__()*self.scale, width=self.maze[0].__len__()*self.scale)
        #self.drawMaze()
        self.dump()
        self.canvas.pack()


    def dump(self):
        for l in self.maze:
            print(l)

    def drawMaze(self):
        s= self.scale
        for y in range(0,self.height):
            for x in range(0,self.width):
                if self.maze[x][y] != "0":
                    self.canvas.create_rectangle(y*s, x*s, (y+1)*s, (x+1)*s, fill=Maze.color_map[self.maze[x][y]])



    def refresh(self):
        #self.maze[random.randint(0,9)][random.randint(0,9)] = "x"
        self.drawMaze()
        self.canvas.after(500, self.refresh)





    def start(self):
        # make first Rat and add it..
        first_rat = rat.Rat(self.maze, 0, 0)
        print ("Started rat..")
        first_rat.start_me()
        print ("Finished rat..")
        self.canvas.mainloop()
        print("done main loop")

m = Maze()
m.loadMaze("a_maze.txt")
m.refresh()
m.start()

