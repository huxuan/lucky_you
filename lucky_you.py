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
import datetime
import threading
import random

import wx

WIDTH = 500
TIME_SLEEP = 1.0/20

DIR_PIC = 'pic'
DIR_TEXT = 'text'
DIR_LOG = 'log'

RESULT_SET = set([])
FILTER_SET = set(['README.md', 'Thumbs.db'])

class MainWindow(wx.Frame):
    """Summary of MainWindow
    """
    def __init__(self, parent=None, title=None):
        """Init MainWindow"""
        self.mark = 0
        random.seed(time.time())

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

        if not os.path.exists(DIR_LOG):
            os.makedirs(DIR_LOG)
        date = datetime.datetime.now().strftime('%Y%m%d')
        self.log_file_path = os.path.join(DIR_LOG, '%s.log' % date)

    def start(self, event=None):
        """docstring for start"""
        if self.mark == 0:
            self.mark = 1
            thread = threading.Thread(target=self.forloop)
            thread.start()
        self.SetFocus()

    def forloop(self):
        """docstring for forloop"""
        if os.path.isdir(DIR_PIC):
            files = os.listdir(DIR_PIC)
            files = list(set(files).difference(FILTER_SET))
            random.shuffle(files)
            while True:
                for item in files:
                    if item in RESULT_SET:
                        continue
                    time.sleep(TIME_SLEEP)

                    path_pic = os.path.join(DIR_PIC, item)
                    img = img_scale(wx.Image(path_pic, wx.BITMAP_TYPE_ANY),
                            WIDTH/2, WIDTH/3*2)
                    bitmap = wx.BitmapFromImage(img)
                    bitmap.SetSize((WIDTH/2, WIDTH/3*2))

                    text_name = item.split('.')[:-1]
                    text = '.'.join(text_name)
                    text_name.append('txt')
                    text_name = '.'.join(text_name)
                    path_text = os.path.join(DIR_TEXT, text_name)
                    if os.path.exists(path_text) and os.path.isfile(path_text):
                        file_text = file(path_text, 'r')
                        text = file_text.read().strip()
                        file_text.close()

                    # Decode the text whether in gbk or utf8
                    try:
                        text = text.decode('gbk')
                    except:
                        text = text.decode('utf8')

                    wx.CallAfter(self.static_bitmap.SetBitmap, bitmap)
                    wx.CallAfter(self.static_text.SetLabel, text)
                    wx.CallAfter(self.static_text.Wrap, WIDTH/2)

                    if not self.mark:
                        log_file = file(self.log_file_path, 'a')
                        print >>log_file, text.encode('utf8')
                        print >>log_file
                        log_file.close()
                        RESULT_SET.add(item)
                        return
        else:
            msg_dialog = wx.MessageDialog(self, u"No pic Directory Found!", "Error", wx.OK)
            msg_dialog.ShowModal()
            msg_dialog.Destroy()
            self.Destroy()

    def stop(self, event=None):
        """docstring for stop"""
        self.mark = 0
        self.SetFocus()

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
