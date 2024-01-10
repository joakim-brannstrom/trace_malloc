#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import view
import data

class Controller:
    __allocDetail = []

    def __init__(self):
        self.commond = {
            'Open' : self.Open,
            'SelectCanvas' : self.SelectCanvas,
            'SelectTreeview' : self.SelectTreeview,
            'ShowDetail' : self.ShowDetail,
        }
        self.__dataSource = None

    def Open(self, app, **kwargs):
        print("Open", kwargs['FilePath'])
        dataSource = data.DataSource(kwargs['FilePath'])
        self.__dataSource = dataSource
        self.__allocSummary = self.__dataSource.getAllocSummary()
        app.updateCanvas(self.__allocSummary.keys(), self.__allocSummary.values())
        app.updateFrameList([])
        print(self.__dataSource.values())

    def SelectCanvas(self, app, **kwargs):
        timeStr = kwargs['TimeStr']
        size = view.format_bytes(self.__allocSummary[timeStr])
        app.updateStatusBar('{0} alloc {1}.'.format(timeStr, size))

        keyFrameData = self.__dataSource.getAllocFrame(timeStr)
        app.updateFrameList(keyFrameData)

    def SelectTreeview(self, app, **kwargs):
        print("hello")
        keyFrame = kwargs['KeyFrame']
        self.__allocDetail = self.__dataSource.getAllocDetail(app.LastSelectTimeStr, keyFrame)
        app.updateDetail(0, len(self.__allocDetail), self.__allocDetail[0])

    def ShowDetail(self, app, **kwargs):
        print("smurf ", self.__allocDetail)
        idx = kwargs['Index']
        if idx < len(self.__allocDetail):
            app.updateDetail(idx, len(self.__allocDetail), self.__allocDetail[idx])

if __name__ == '__main__':
    ctrl = Controller()
    app = view.Application()
    app.setCommondDispatcher(ctrl.commond)              
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            pass
