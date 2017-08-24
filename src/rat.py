import threading
import time
import collections


class Rat(object):
    lock = threading.Lock()
    rats_alive_count = 0
    rat_counter = 0
    color_map = {'x':'black','a':'red','b':'green','c':'blue','d':'yellow',
                 'e':'turquoise','f':'orange','g':'pink','h':'violet','i':'brown'}
    color_keys = collections.deque(color_map.keys()) #We will rotate through these colors when creating new Rats
    color_keys.remove('x') # rats shouldn't be the same color as the walls
    print(f"Keys now have value:{color_keys} ")
    def __init__(self, maze, x, y):
        threading.Thread.__init__(self)
        self.maze = maze
        self.x = x
        self.y = y
        self.height = maze.__len__()
        self.width = maze[0].__len__()
        self.color_key = Rat.color_keys.pop()
        self.maze[x][y] = self.color_key
        Rat.color_keys.insert(0,self.color_key)  #rotate color in list

    def run(self):
        print(f"Creating rat at [{self.x},{self.y}]")
        Rat.rat_counter += 1
        rat_alive = True
        while rat_alive:
            time.sleep(1)
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
                        if available_directions == 1: # this rat continues here
                            self.maze[self.x + p[0]][self.y + p[1]] = self.color_key
                            my_x = self.x + p[0]
                            my_y = self.y + p[1]
                        if available_directions > 1:
                            # there is more than one direction. Make a new Rat.
                            rat = Rat(self.maze, self.x+ p[0], self.y+ p[1])
                            rat.start_me()
                self.x = my_x
                self.y = my_y
                if available_directions == 0:
                    #nowhere to go, the rat dies.
                    rat_alive = False
                    Rat.rats_alive_count = threading.active_count()-2
                    print(f"Rat dying, current rat count = {threading.active_count()-2}")


    def start_me(self):
        t1 = threading.Thread(target=self.run)
        t1.start()

mz = [['0','x','x','0'],['0','0','0','0'],['0','0','0','x'],['0','0','0','0']]
rt = Rat(mz,0,0)
rt.start_me()
print("done.")