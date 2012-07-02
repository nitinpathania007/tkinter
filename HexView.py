#!/usr/bin/python3

# tkinter/ttk stuff
from tkinter import *
from tkinter.font import *
from tkinter.ttk import *

class HexView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.font = Font(family='monospace', size=12)

        (w, h) = (self.font.measure('X'), self.font.metrics('linespace'))
        self.charWidth = w
        self.charHeight = h

        self.marginX = 4
        self.marginY = 4
        self.linesDisplayed = 16

        # eg 'DEADBEEF: '
        self.xAddr = self.marginX
        self.lAddr = self.charWidth * 9
        self.xBytes = self.xAddr + self.lAddr + self.charWidth
        self.lBytes = self.charWidth * (16*2 + 15)
        self.xAscii = self.xBytes + self.lBytes + self.charWidth
        self.lAscii = 16*self.charWidth

        self.width = self.xAscii + self.lAscii + self.marginX
        self.height = self.marginY + self.charHeight*self.linesDisplayed + self.marginY

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.config(background='white')
        self.canvas.pack()

        self.addr = 0
        self.data = []

        self.hlRange = None

    def setHighlight(self, start, end):
        self.hlRange = [start, end]

    def setAddr(self, addr):
        self.addr = addr

    def setData(self, data):
        self.data = list(data)

    def draw(self):
        if not self.data:
            return

        self.canvas.delete(ALL)

        capacity = self.linesDisplayed * 16

        currAddr = self.addr
        currInd = 0
        currLine = 0
        for lineNum in range(self.linesDisplayed):
            yLine = self.marginY + lineNum*self.charHeight

            chunk = self.data[currInd:(currInd+16)]
            if not chunk:
                break

            # write the address
            self.canvas.create_text( \
                [self.xAddr, yLine], \
                text = '%08X: ' % currAddr, \
                fill = "blue", \
                anchor = NW, \
                font = self.font \
            )

            # write the bytes
            for byteNum in range(len(chunk)):
                textId = self.canvas.create_text( \
                    [self.xBytes + byteNum * self.charWidth * 3, yLine], \
                    text = '%02X' % chunk[byteNum], \
                    anchor = NW, \
                    font = self.font
                )

                if self.hlRange:
                    if currAddr >= self.hlRange[0] and currAddr <= self.hlRange[1]:
                        rectId = self.canvas.create_rectangle(self.canvas.bbox(textId), fill='yellow', outline='yellow')
                        self.canvas.tag_lower(rectId, textId)
                currAddr += 1

            # write the ascii
            for i, byte in enumerate(chunk):
                if byte > ord(' ') and byte < ord('~'):
                    chunk[i] = chr(byte)
                else:
                    chunk[i] = '.'

            self.canvas.create_text( \
                [self.xAscii, yLine], \
                text = ''.join(chunk), \
                fill = "#008000", \
                anchor = NW, \
                font = self.font \
            )
       
            currInd += 16
            currLine += 1

            # run out of bytes early? (display oversized?)
            if len(chunk) < 16:
                break

def doTest():
    # root window
    root = Tk()
    root.wm_title("HexView Test\n")

    # reserve board on root
    hvt = HexView(root)
    hvt.setAddr(0xDEADBEEF)

    data = [ \
        0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x02, 0x00, 0x3e, 0x00, 0x01, 0x00, 0x00, 0x00, 0x90, 0x24, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x96, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x38, 0x00, 0x09, 0x00, 0x40, 0x00, 0x1c, 0x00, 0x1b, 0x00, \
        0x06, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x40, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0xf8, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, \
        0x38, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x02, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x38, 0x02, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x8c, 0x89, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8c, 0x89, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, \
        0xf0, 0x8d, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x8d, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0xf0, 0x8d, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0xb0, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x02, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x18, 0x8e, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x18, 0x8e, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x8e, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0xc0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
        0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, \
        0x54, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x54, 0x02, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00 \
    ]
    hvt.setData(data)
    hvt.setHighlight(0xDEADBEF5, 0xDEADBEFF)
    hvt.pack()

    hvt.draw()
    # run
    root.mainloop() 

if __name__ == "__main__":
    doTest()


