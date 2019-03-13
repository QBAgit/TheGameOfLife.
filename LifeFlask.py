from urllib import request

import Life
from my_module import buildwebpage
from flask import Flask
from flask import request

app = Flask(__name__)

area = []
Year = 0
GameStarted = False


def draw_html_area(year):
    
    global area
    out = "<table>"

    if year >= len(area):
        mod_area()
    elif year < 0:
        raise ValueError("Year < 0 => ListIndex Out of Range")

    for x in range(0, Life.scr_res[0]):
        out += "<tr>"
        
        for y in range(0, Life.scr_res[1]):
            out += "<td>{}</td>".format(area[year][x][y])
        
        out += "</tr>"
    
    out += "</table>"
    
    return out


def gen_rand_area():

    print("DupoDebug: gen_rand_area()")
    
    global area

    if len(area) == 0:

        empty = Life.create_empty_area(Life.scr_res)
        box = Life.draw_box(Life.scr_res, empty)
        area.append(Life.gen_rand_area(Life.scr_res, box, "o", 2))
        print("DupoDebug: Line 48")


def load_file_area():

    global area
    if len(area) == 0:
        area.append(Life.load_area(Life.scr_res, "area.txt"))


def mod_area():
    
    global area

    # Currnet years in the area
    curr_year = len(area) - 1
    # print("Debug: mod_area(): curr_year={}".format(curr_year))

    area.append(Life.thisIsLife(Life.scr_res, area[curr_year]))


@app.route("/", methods=['GET', 'POST'])
def game_of_life():
    
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

        if "next" in request.form:
            Year += 1

        if "prev" in request.form and Year > 0:
            Year -= 1

        if Year == 0:

            if "mode" in request.form:

                gamemode = request.form['mode']

                if gamemode == "random":
                    gen_rand_area()
                elif gamemode == "file":
                    load_file_area()
            else:
                gen_rand_area()

        if "start" in request.form or GameStarted:

            GameStarted = True
            score = "<p3>Year: {}<br></p3>".format(Year)
            areahtml = draw_html_area(Year)
            
            game = '''
                <form method="POST">
                    <input type="submit" name="prev" value="Prev">
                    <input type="submit" name="next" value="Next">
                </form>'''
                        
            game += areahtml

    return buildwebpage(title + score + game, "The game of life")


def main():
    global app

    app.run()
    
    # Na wypadek problemów z portem 5000
    # app.run(port=4000)


if __name__ == "__main__":
    main()
