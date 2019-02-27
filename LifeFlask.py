import Life
from my_module import buildwebpage
from flask import Flask
from flask import request

app = Flask(__name__)

area = []
Year = 0
GameStarted = False

def drawHtmlArea():
    
    global area
    out = "<table>"
    
    for x in range(0,Life.scr_res[0]):
        out+="<tr>"
        
        for y in range(0,Life.scr_res[1]):
            out+="<td>{}</td>".format(area[x][y])
        
        out+="</tr>"
    
    out += "</table>"
    
    return out


def genRandArea():
    
    global area
    
    empty = Life.create_empty_area(Life.scr_res)
    box = Life.draw_box(Life.scr_res, empty)
    area = Life.gen_rand_area(Life.scr_res, box, "o", 2)


def loadFileArea():
    
    global area
    area = Life.load_area(Life.scr_res, "area.txt")

def modArea():
    
    global area
    
    area = Life.thisIsLife(Life.scr_res, area)

@app.route("/", methods=['GET','POST'])
def GameOfLife():
    
    global Year
    global GameStarted
    
    
    title = "<h3>This a game of Life...</h3>"
    score = ""
    areahtml = ""
    game = '''
        <form method="POST">
            <input type="radio" name="mode" value="random">Radnom Area<br>
            <input type="radio" name="mode" value="file">Load Area from area.txt<br><br>
            <input type="submit" name="start" value="Start the Game">
        </form>'''
 
    if request.method == 'POST':

        try:
            if Year == 0:
                gamemode = request.form['mode']
                          
                if gamemode == "random":
                    genRandArea()
                elif gamemode == "file":
                    loadFileArea()
                                
        except Exception as E:
            print("Error 01: " + str(E))
            genRandArea()

        if "start" in request.form or GameStarted:

            GameStarted = True
            score = "<p3>Year: {}<br></p3>".format(Year)
            areahtml = drawHtmlArea()
            
            game = '''
                <form method="POST">
                    <input type="submit" name="next" value="Next">
                </form>'''
                        
            game += areahtml
        
        if "next" in request.form:
            Year += 1
            modArea()

    return buildwebpage(title + score + game)


def main():
    global app
    
    app.run()
    
    #Na wypadek problemów z portem 5000
    #app.run(port=4000)

if __name__ == "__main__":
    main()
