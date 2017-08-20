import threading
import time

class Rat(threading.Thread):
    lock = threading.Lock()
    rat_counter = 0
    def __init__(self, maze, x, y):
        threading.Thread.__init__(self)
        self.maze = maze
        self.x = x
        self.y = y
        self.height = maze.__len__()
        self.width = maze[0].__len__()
        maze[x][y] = "r"

    def run(self):
        print(f"Creating rat at [{self.x},{self.y}]")
        Rat.rat_counter += 1
        rat_alive = True
        while rat_alive:
            time.sleep(2)
            #avoid race condition
            with Rat.lock:
                #check above, below
                available_directions = 0
                #check all directions
                my_x = 0
                my_y = 0
                for p in [[1,0],[0,1],[-1,0],[0,-1]]:
                    if (self.x + p[0] in range(0,self.width) and
                      self.y + p[1] in range(0,self.height) and
                      self.maze[self.x+ p[0]][self.y+ p[1]] == '0'):
                        available_directions +=1      # we can go in at least one direction.
                        if available_directions == 1: # this rat will take the first direction
                            self.maze[self.x + p[0]][self.y + p[1]] = 'r'
                            my_x = self.x + p[0]
                            my_y = self.y + p[1]
                        if available_directions > 1:
                            # there is more than one direction. Make a new Rat.
                            rat = Rat(self.maze, self.x+ p[0], self.y+ p[1])
                            rat.start()
                self.x = my_x
                self.y = my_y
                if available_directions == 0:
                    #nowhere to go, we have to kill the rat.
                    rat_alive = False


    def startMe(self):
        t1 = threading.Thread(target=self.run())
        t1.start()

mz = [['0','x','x','0'],['0','0','0','0'],['0','0','0','x'],['0','0','0','0']]
rt = Rat(mz,0,0)
#print("Starting.")
#t1 = threading.Thread(target=rt.run())
rt.start()
print("done.")