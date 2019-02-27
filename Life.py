from os import system
from random import randint
from time import sleep
from sys import exit

#Screen Resolution: x,y
scr_res = (25,75)
#SampleTime
sTime = 0.1

def print_area(res, area):

    system("clear")
    print("Area: {}x{} : Ctrl-C -> Quit".format(scr_res[0],scr_res[1]))
    screen_out = ""
    
    for i in range(0,res[0]):
        for j in range(0,res[1]):
            screen_out += area[i][j]
        screen_out += "\n"

    print(screen_out)

def save_area(res, area, myfile):
    
    f= open(myfile,"w")
    
    for i in range(0,res[0]):
        line = ""
        for j in range(0,res[1]):
            line += area[i][j]
        f.write(line + "\n")

    f.close()

def file_as_string(file_path):
    buff=""
    file_to_read = open(file_path,'r')
    
    while True:
        line = file_to_read.readline()
        if line == "":
            break
        buff+=line
    
    file_to_read.close()
    return buff

def load_area(res, myfile):
    
    text = file_as_string(myfile)
    
    textrows = text.split("\n")
    
    empty_area = create_empty_area(res)
    
    for i in range(len(empty_area)):
        empty_area[i] = textrows[i]
    
    return empty_area

    
def create_empty_area(res,char=" "):
    # x = res[0]
    # y = res[1]
    return [ [char for x0 in range(res[1]) ] for y0 in range(res[0]) ]

def draw_box(res, area):
    #print("xmax={}".format(res[0]))
    #print("ymax={}".format(res[1]))
    #go by rows
    for i in range(0,res[0]):
        #go by collumn
        for j in range(0,res[1]):
            #print("x={},y={}".format(i,j))
            if i==0 or i==res[0]-1:
                area[i][j]=">"
            if j==0 or j==res[1]-1:
                area[i][j]="|"
    return area

def gen_rand_area(res, area,char="o",div=1):

    randomrow = []
    
    #go by rows <1,x-2> !!!DO NOT TOUCH BOX
    for i in range(1,res[0]-2):
        #go by collumn <1,y-2> !!!DO NOT TOUCH BOX
        
        #gen n randoms
        n_in_row = int(randint(0,res[1])/div)

        #gen random lifes in row
        for n in range(n_in_row):
            randomrow.append(randint(1,res[1]-2))

        for j in range(1,res[1]-2):
            #print("x={},y={}".format(i,j))

            if j in randomrow:
                area[i][j]=char
        
        randomrow.clear()
        
    return area

def find_lifeneighbors(area,my_x,my_y,alife):
    
    ctr=0
    
    if area[my_x-1][my_y-1]==alife:
        ctr+=1
    
    if area[my_x-1][my_y]==alife:
        ctr+=1
    
    if area[my_x-1][my_y+1]==alife:
        ctr+=1
    
    if area[my_x+1][my_y-1]==alife:
        ctr+=1
    
    if area[my_x+1][my_y]==alife:
        ctr+=1
    
    if area[my_x+1][my_y+1]==alife:
        ctr+=1

    if area[my_x][my_y-1]==alife:
        ctr+=1

    if area[my_x][my_y+1]==alife:
        ctr+=1
    
    return ctr

def cpy_area(res,area):
    
    clear = create_empty_area(res)
    
    #go by rows
    for i in range(0,res[0]):
        #go by collumns
        for j in range(0,res[1]):
            clear[i][j] = area[i][j]
    
    return clear


def thisIsLife(res,area,dead=" ",alife="o"):
    
    #copy area
    out = cpy_area(res,area)
    
    #go by rows <1,x-2> !!!DO NOT TOUCH BOX
    for i in range(1,res[0]-2):
        #go by collumn <1,y-2> !!!DO NOT TOUCH BOX
        for j in range(1,res[1]-2):
            #DEAD Body look for 3 life neighbors
            if area[i][j]==dead:
                #FIND Neighbors
                alife_neighbors = find_lifeneighbors(area,i,j,alife)
                                
                if alife_neighbors==3:
                    #print("DEAD -> life :: x={},y={}, neig={}".format(i,j,alife_neighbors))
                    #GIVE ME life!!!
                    out[i][j] = alife
                    
            elif area[i][j]==alife:
                #life Body stays alife if have 2 or 3 neighbors or it will die
                alife_neighbors=0

                alife_neighbors = find_lifeneighbors(area,i,j,alife)
                
                if alife_neighbors==2 or alife_neighbors==3:
                    #print("life -> life :: x={},y={}, neig={}".format(i,j,alife_neighbors))
                    pass
                else:
                    #print("life -> DEAD :: x={}y={}, neig={}".format(i,j,alife_neighbors))
                    #KILL ME!!!
                    out[i][j] = dead
    return out
    

if __name__ == "__main__":
    
    print("OPTIONS:")
    print("1.Load Random Area -> Save to File")
    print("2.Load Random -> Start life")
    print("3.Init from area.txt -> Start life")

    mode = int(input("> "))
    
    if mode == 1:
        
        empty = create_empty_area(scr_res)
        box = draw_box(scr_res, empty)
        area = gen_rand_area(scr_res, box, "o", 2)
        print_area(scr_res, area)
   
        save_area(scr_res, area, "randarea{}x{}.txt".format(scr_res[0],scr_res[1]))

    elif mode == 2:
        
        empty = create_empty_area(scr_res)
        box = draw_box(scr_res, empty)
        area = gen_rand_area(scr_res, box, "o", 2)
   
        #save_area(scr_res, area, "area.txt")

    elif mode == 3:
        area = load_area(scr_res, "area.txt")
        
    if mode == 2 or mode == 3:
        while(True):
            try:
                print_area(scr_res, area)
                area = thisIsLife(scr_res, area)
                sleep(sTime)
            except KeyboardInterrupt:
                print("THE END")
                exit(0)

