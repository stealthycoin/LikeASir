import sys, math
from Tkinter import *
import tkMessageBox
import colorsys

def transform(text, sirLevel):
    return "Level " + str(sirLevel) + ": " + text

def main():
    top = Tk()
    #text input
    textIn = Text(top,bg="#FCF5D8")

    #dial code
    dialAngle = [math.pi]
    ds = 30
    cx = ds
    cy = ds
    r = ds*2/3
    regions = 5
    dial = Canvas(top, width=ds*2, height=ds)
    startColor = colorsys.rgb_to_hsv(255,0,0)
    endColor = colorsys.rgb_to_hsv(0,255,0)
    color = list(startColor)

    #backdrop arc
    dial.create_arc(cx-r,cy-r,cx+r,cy+r, start=0, extent=180, outline="#DDD", fill="#DDD", style="chord")
    #colored arc
    for angle in [x*180/regions for x in range(regions)]:
        dial.create_arc(cx-r,cy-r,cx+r,cy+r, start=angle, extent=180/regions, outline=('#%02x%02x%02x' % colorsys.hsv_to_rgb(color[0],color[1],color[2])), width=15, style="arc")
        for i in range(len(color)):#interpolate
            color[i] += (endColor[i] - startColor[i]) / regions

    #indicator
    indicator = [dial.create_line(cx,cy,cx+r*math.cos(dialAngle[0]), cy+r*math.sin(dialAngle[0]),width=1)]

    #move the indicator when a click happens
    def dialMouseDown(event, indicator, dialAngle):
        x,y = event.x,event.y
        dx = x-cx
        dy = -(y-cy)
        if dy < 0:
            if dx >= 0:
                dialAngle[0] = 0
            elif dx < 0:
                dialAngle[0] = math.pi
        elif dx == 0:
            dialAngle[0] = math.pi / 2
        else:
            dialAngle[0] = math.atan2(dy,dx)
        dial.delete(indicator[0])
        indicator[0] = dial.create_line(cx,cy,cx+r*math.cos(dialAngle[0]), cy+r*-math.sin(dialAngle[0]),width=1)        
    dial.bind("<ButtonRelease-1>", lambda x: dialMouseDown(x, indicator, dialAngle))

    #text output
    textOut = Text(top,bg="#FCF5D8")


    #sir it button
    def sirButtonCallback():
        likeAPleb = textIn.get(1.0,END)
        likeASir = transform(likeAPleb, int(regions - (dialAngle[0] * regions / math.pi)))
        textOut.insert(END, likeASir)
    sirIt = Button(top, text="Like a Sir!", command = sirButtonCallback)

    #package the widgets
    textIn.pack()
    sirIt.pack()
    dial.pack()
    textOut.pack()
    
    top.wm_title("Diction, Like a Sir!!!")
    top.mainloop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        #command mode
        pass
    else:
        #GUI mode
        main()
