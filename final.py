import requests
import json
import os
import io
import base64 # To hide secrets! :)
from tkinter import * # Import every function from Tkinter. When we do this, we don't need to prefix each function with 'tkinter.'
from tkinter import messagebox # This is a module, so it wasn't imported from the above line.
from tkinter import filedialog # Same with this.
from PIL import ImageTk, Image # Import two modules from Pillow.
from pathlib import Path # To ensure cross-platform support.

s = requests.Session() # This creates a Requests Session which will retain any cookies set during execution.

apiKey = "AIzaSyDC5Pvq63wgfHRqHunBM1OFgOO-arIK7Tw" # This is an API key from the #
                                                   # Google Cloud Platform. It   #
                                                   # enables the use of the      #
                                                   # Google Maps Geocode API.    #
top = Tk() # Create a Tkinter window.
top.geometry("300x300") # Set window size.
top.title(string="QuickMap") # Set window title.
top.resizable(width=False, height=False) # Don't allow the window to be resized.

def getMap():
    locText = l.get()
    if len(locText) == 0: # If the location box is empty...
        messagebox.showwarning("Warning", "Location is a required field.")
    if "b'{}'".format(locText) == str(base64.b64decode("MSBBcHBsZSBQYXJrIFdheQ==")) or "b'{}'".format(locText) == str(base64.b64decode("MSBJbmZpbml0ZSBMb29w")):
        messagebox.showinfo(base64.b64decode("RGVhciBLYXRlLA=="), base64.b64decode("SGVyZSdzIHRvIHRoZSBjcmF6eSBvbmVzLiBUaGUgbWlzZml0cy4gVGhlIHJlYmVscy4gVGhlIHRyb3VibGVtYWtlcnMuIFRoZSByb3VuZCBwZWdzIGluIHRoZSBzcXVhcmUgaG9sZXMuIFRoZSBvbmVzIHdobyBzZWUgdGhpbmdzIGRpZmZlcmVudGx5LiBUaGV5J3JlIG5vdCBmb25kIG9mIHJ1bGVzLiBBbmQgdGhleSBoYXZlIG5vIHJlc3BlY3QgZm9yIHRoZSBzdGF0dXMgcXVvLiBZb3UgY2FuIHF1b3RlIHRoZW0sIGRpc2FncmVlIHdpdGggdGhlbSwgZ2xvcmlmeSBvciB2aWxpZnkgdGhlbS4gQWJvdXQgdGhlIG9ubHkgdGhpbmcgeW91IGNhbid0IGRvIGlzIGlnbm9yZSB0aGVtLiBCZWNhdXNlIHRoZXkgY2hhbmdlIHRoaW5ncy4gVGhleSBwdXNoIHRoZSBodW1hbiByYWNlIGZvcndhcmQuIEFuZCB3aGlsZSBzb21lIG1heSBzZWUgdGhlbSBhcyB0aGUgY3Jhenkgb25lcywgd2Ugc2VlIGdlbml1cy4gQmVjYXVzZSB0aGUgcGVvcGxlIHdobyBhcmUgY3JhenkgZW5vdWdoIHRvIHRoaW5rIHRoZXkgY2FuIGNoYW5nZSB0aGUgd29ybGQsIGFyZSB0aGUgb25lcyB3aG8gZG8u"))
    width = str(w.get())
    height = str(h.get())
    rad = str(r.get())
    print("{}, {}, {}".format(width, height, rad))
    locQuery = locText.replace(" ", "+") # The API doesn't accept queries with spaces.
    params = {"address":locQuery, "key":apiKey}
    geocodeReq = s.get("https://maps.google.com/maps/api/geocode/json", params=params) # Make an API call to get geocode information.
    geocodeJSON = json.loads(geocodeReq.text) # Parse the resulting JSON text.
    try:
        geocode = geocodeJSON['results'][0]['geometry']['location']
        lat = str(geocode['lat'])
        lon = str(geocode['lng'])
        global mapReq # Make mapReq a global variable, so it can be accessed outside of getMap()
        mapReq = s.get('https://snapshot.apple-mapkit.com/v1/snapshot?center=' + lat + ',' + lon + '&size=' + width + 'x' + height + '&radius=' + rad)
        print(mapReq.url)
        try:
            mapImage = ImageTk.PhotoImage(Image.open(io.BytesIO(mapReq.content))) # Take the bytes of the map image   #
            mapWindow = Toplevel() # Create a new window.                         # and pack them into a file object. #
            mapWindow.title(geocodeJSON['results'][0]['formatted_address'])       # Then, open the file object with   #
            mapWindow.geometry("{}x{}".format(width, height))                     # the Pillow module and convert it  #
            mapWindow.resizable(width=False, height=False)                        # to a format that Tkinter can use. #
            generatedMap = Label(mapWindow, image=mapImage) # Oddly, you must use #
            generatedMap.photo = mapImage                   # a Label object to   #
            generatedMap.place(x=0, y=0)                    # place an image in   #
                                                            # window.             #

            downloadBtn = Button(mapWindow, text="Download...", command=download)
            downloadBtn.place(x=int(width) - 100, y=int(height) - 30) # The button will move based on the size of the image.
        except OSError:
            messagebox.showerror("Error", "There was an error processing the image file. Please try again.")
    except IndexError:
        if not len(locText) == 0: # Make sure the error doesn't show when there was no location in the first place.
            messagebox.showerror("Error", "No results were found for that location. Try again.")

def download():
    path = filedialog.asksaveasfilename(initialdir = str(Path.home()), title = "Save as...", filetypes = (("JPEG Images","*.jpg;*.jpeg"),("all files","*.*")))
    try:
        with open(path, 'wb') as mapFile: # This prevents us from needing to close the file when we're done writing to it.
            mapFile.write(mapReq.content) # Write every byte to the file, creating a fully functional image.
        messagebox.showinfo("Complete", 'Your snapshot was saved as "{}" in {}.'.format(path.split("/")[-1], path.replace(path.split("/")[-1], '')))
    except FileNotFoundError:
        pass # The save dialog was terminated without returning a valid path.
def updateWBox(newVal):
    if top.focus_get() != wbox:
        wid.set(str(newVal))

def updateHBox(newVal):
    if top.focus_get() != hbox:
        hgt.set(str(newVal))

def updateRBox(newVal):
    if top.focus_get() != rbox:
        rds.set(str(newVal))

def updateScales(a, b, c): # Even though these variables are unused, we still need to capture them to avoid exceptions.
    try:
        if int(wid.get()) >= 135 and int(wid.get()) <= 1280:
            w.set(int(wid.get()))
        elif int(wid.get()) < 135:
            w.set(135)
        elif int(wid.get()) > 1280:
            w.set(1280)
    except Exception:
        pass # A pass statement is the equivalent of doing nothing.
    try:
        if int(hgt.get()) >= 135 and int(hgt.get()) <= 1280:
            h.set(int(hgt.get()))
        elif int(hgt.get()) < 135:
            h.set(135)
        elif int(hgt.get()) > 1280:
            h.set(1280)
    except Exception:
        pass
    try:
        if float(rds.get()) >= 0.1 and float(rds.get()) <= 3000.0:
            r.set(float(rds.get()))
        elif float(rds.get()) < 0.1:
            r.set(0.1)
        elif float(rds.get()) > 3000.0:
            r.set(3000.0)
    except Exception:
        pass

def fixFocus(event): # This function makes objects in the window lose focus when clicked away from.
                     # It also updates the values in the text boxes next to the sliders.
    if event.widget != wbox or hbox or rbox:
        event.widget.focus_set()
        try:
            if int(wid.get()) >= 135 and int(wid.get()) <= 1280:
                w.set(int(wid.get()))
            elif int(wid.get()) < 135:
                w.set(135)
                wid.set("135")
            elif int(wid.get()) > 1280:
                w.set(1280)
                wid.set("1280")
        except Exception:
            wid.set("135")
            w.set(135)
        try:
            if int(hgt.get()) >= 135 and int(hgt.get()) <= 1280:
                h.set(int(hgt.get()))
            elif int(hgt.get()) < 135:
                h.set(135)
                hgt.set("135")
            elif int(hgt.get()) > 1280:
                h.set(1280)
                hgt.set("1280")
        except Exception:
            hgt.set("135")
            h.set(135)
        try:
            if float(rds.get()) >= 0.1 and float(rds.get()) <= 3000.0:
                r.set(float(rds.get()))
            elif float(rds.get()) < 0.1:
                r.set(0.1)
                rds.set("0.1")
            elif float(rds.get()) > 3000.0:
                r.set(3000.0)
                rds.set("3000.0")
        except Exception:
            rds.set("0.1")
            r.set(0.1)

# ===================================================================
# | From here downwards, all widgets in the windows are defined and |
# | placed. There is nothing very interesting that happens here.    |
# ===================================================================

loc = StringVar() # Tkinter requires special StringVar objects rather than strings to manage text content in windows.
wid = StringVar()
hgt = StringVar()
rds = StringVar()
l = Entry(top, textvariable=loc)
llabel = Label(top, text="Location")
w = Scale(top, from_=135, to=1280, orient=HORIZONTAL, length=118, width=25, showvalue=0, command=updateWBox)
wlabel = Label(top, text="Width")
wbox = Entry(top, textvariable=wid, width=5)
h = Scale(top, from_=135, to=1280, orient=HORIZONTAL, length=118, width=25, showvalue=0, command=updateHBox)
hlabel = Label(top, text="Height")
hbox = Entry(top, textvariable=hgt, width=5)
r = Scale(top, from_=0.1, to=3000, orient=HORIZONTAL, length=110, width=25, resolution=0.1, showvalue=0, command=updateRBox)
rlabel = Label(top, text="Radius")
rbox = Entry(top, textvariable=rds, width=6)

OKButton = Button(text="OK", command=getMap)

wbox.place(x=220, y=40)
hbox.place(x=220, y=70)
rbox.place(x=212, y=100)
l.place(x=100, y=10)
llabel.place(x=10, y=10)
w.place(x=101, y=40)
wlabel.place(x=10, y=40)
h.place(x=101, y=70)
hlabel.place(x=10, y=70)
r.place(x=101, y=100)
rlabel.place(x=10, y=100)
OKButton.place(x=150, y=170)

wid.trace('w', updateScales) # Monitor for any changes to the value of wid. When it changes, run updateScales().
hgt.trace('w', updateScales)
rds.trace('w', updateScales)
top.bind("<Button-1>", fixFocus) # When a left click is registered while top is in focus, run fixFocus().
top.bind("<Button-2>", fixFocus) # When a right click is registered while top is in focus, run fixFocus().

top.mainloop() # Don't close the window when all elements are placed.
