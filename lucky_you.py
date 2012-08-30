#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lucky-you.py
Author: huxuan
E-mail: i(at)huxuan.org
Created: 2012-08-30
Last modified: 2012-08-30
Description:
    Description for lucky-you.py

Copyrgiht (c) 2012 by huxuan. All rights reserved.
License GPLv3
"""

import os
import time
import threading

import wx

WIDTH = 400
TIME_SLEEP = 1/20
DIR_PIC = 'pic'
DIR_TEXT = 'text'

class MainWindow(wx.Frame):
    """Summary of MainWindow
    """
    def __init__(self, parent=None, title=None):
        """Init MainWindow"""
        self.mark = 0

        wx.Frame.__init__(self, parent, title=title, size=(WIDTH, -1))
        self.SetBackgroundColour('white')
        self.SetFocus()
        main_sizer = wx.FlexGridSizer(cols=2, vgap=2, hgap=2)

        self.static_text = wx.StaticText(self, label=u'Lucky You.',
                size=(WIDTH/2, -1),
                style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        self.static_text.SetFont(font)
        self.static_text.Wrap(WIDTH/2)
        self.static_bitmap = wx.StaticBitmap(self,
                size=(WIDTH/2, WIDTH/3*2),
                style=wx.ALIGN_CENTER)
        button_start = wx.Button(self, label=u'Start')
        button_stop = wx.Button(self, label=u'Stop')

        main_sizer.Add(self.static_text, flag=wx.ALIGN_CENTER|wx.EXPAND)
        main_sizer.Add(self.static_bitmap, flag=wx.ALIGN_CENTER)
        main_sizer.Add(button_start, flag=wx.ALIGN_RIGHT)
        main_sizer.Add(button_stop, flag=wx.ALIGN_LEFT)

        self.Bind(wx.EVT_BUTTON, self.start, button_start)
        self.Bind(wx.EVT_BUTTON, self.stop, button_stop)

        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)

        self.SetSizerAndFit(main_sizer)

    def start(self, event=None):
        """docstring for start"""
        if self.mark == 0:
            self.mark = 1
            thread = threading.Thread(target=self.forloop)
            thread.start()

    def forloop(self):
        """docstring for forloop"""
        while True:
            for item in os.listdir(DIR_PIC):
                if not self.mark:
                    return
                if item == 'README.md':
                    continue
                time.sleep(TIME_SLEEP)

                path_pic = os.path.join(DIR_PIC, item)
                img = img_scale(wx.Image(path_pic, wx.BITMAP_TYPE_ANY),
                        WIDTH/2, WIDTH/3*2)
                bitmap = wx.BitmapFromImage(img)
                bitmap.SetSize((WIDTH/2, WIDTH/3*2))

                text_name = item.split('.')[:-1]
                text_name.append('txt')
                text = text_name = '.'.join(text_name)
                path_text = os.path.join(DIR_TEXT, text_name)
                if os.path.exists(path_text) and os.path.isfile(path_text):
                    file_text = file(path_text, 'r')
                    text = file_text.read().strip()
                    file_text.close()

                wx.CallAfter(self.static_bitmap.SetBitmap, bitmap)
                wx.CallAfter(self.static_text.SetLabel, text)
                wx.CallAfter(self.static_text.Wrap, WIDTH/2)

    def stop(self, event=None):
        """docstring for stop"""
        self.mark = 0

    def onKeyUp(self, event):
        """docstring for onKeyUp"""
        if event.GetKeyCode() == wx.WXK_SPACE:
            if self.mark == 0:
                self.start()
            else:
                self.stop()

def img_scale(img, width, height):
    """docstring for img_scale"""
    org_width = img.GetWidth()
    org_height = img.GetHeight()
    if org_height * width < org_width * height:
        return img.Scale(width, org_height * width / org_width)
    else:
        return img.Scale(org_width * height / org_height, height)

def main():
    """docstring for main"""
    app = wx.App(False)
    frame = MainWindow(None, 'Lucky You')
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
