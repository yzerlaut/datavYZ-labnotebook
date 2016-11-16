from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np

class FocusMenu(QtWidgets.QDialog):
    
    def __init__(self, parent):
        
        super(FocusMenu, self).__init__(parent)
        self.parent = parent
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('Window Focus')
        # self.setGeometry(900,150,300,500)
        self.setGeometry(880,150,120,150)

        self.ACTIONS = []
        self.set_grid_and_actions()
        
        self.show()

    def set_grid_and_actions(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
 
        FUNCS = [self.xzoom_in, self.xzoom_out, '', '',\
                 self.yzoom_in, '', '', '',\
                 self.yzoom_out, '', self.yshift_up, '',\
                 '', self.xshift_left, self.yshift_bottom, self.xshift_right]
        
        names = ['(r) X-In', '(t) X-Out', '', '',
                 '(d) Y-In', '', '', '',
                 '(x) Y-Out', '', '(i) ^ ', '',
                 '', '(j) <', '(k) v', '(l) >']
        shortcuts = ['r', 't', '', '',
                     'd', '', '', '',
                     'x', '', 'i', '',
                     '', 'j', 'k', 'l']
        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name, func, shortcut in zip(positions, names, FUNCS, shortcuts):
            
            if name == '':
                continue
            button = QtWidgets.QPushButton(name)
            grid.addWidget(button, *position)
            # btn6 = QtWidgets.QPushButton("c) X-Shift Right", self)
            button.clicked.connect(func)
            if shortcut!='':
                action = QtWidgets.QAction(name, self)
                action.setShortcut(shortcut)
                action.triggered.connect(func)
                self.ACTIONS.append(action)
                self.parent.fileMenu.addAction(action)

    def remove_actions(self):
        for action in self.ACTIONS:
            self.parent.fileMenu.removeAction(action)

    def xzoom_in(self):
        self.parent.args['dx'] /=2.
        self.parent.args['x1'] = self.parent.args['x1']+self.parent.args['dx']/2.
        self.parent.args['x2'] = self.parent.args['x1']+self.parent.args['dx']
        self.parent.update_plot()
    def xzoom_out(self):
        self.parent.args['dx'] *=2.
        self.parent.args['x1'] = self.parent.args['x1']-self.parent.args['dx']/4.
        self.parent.args['x2'] = self.parent.args['x1']+self.parent.args['dx']
        self.parent.update_plot()
    def yzoom_in(self):
        self.parent.args['dy1'] /=2.
        self.parent.args['y1_min'] = self.parent.args['y1_min']+self.parent.args['dy1']/2.
        self.parent.args['y1_max'] = self.parent.args['y1_min']+self.parent.args['dy1']
        self.parent.update_plot()
    def yzoom_out(self):
        self.parent.args['dy1'] *=2.
        self.parent.args['y1_min'] = self.parent.args['y1_min']-self.parent.args['dy1']/4.
        self.parent.args['y1_max'] = self.parent.args['y1_min']+self.parent.args['dy1']
        self.parent.update_plot()
    def xshift_right(self):
        self.parent.args['x1'] += self.parent.args['dx']/2.
        self.parent.args['x2'] += self.parent.args['dx']/2.
        self.parent.update_plot()
    def xshift_left(self):
        self.parent.args['x1'] -= self.parent.args['dx']/2.
        self.parent.args['x2'] -= self.parent.args['dx']/2.
        self.parent.update_plot()
    def yshift_up(self):
        self.parent.args['y1_min'] += self.parent.args['dy1']/2.
        self.parent.args['y1_max'] += self.parent.args['dy1']/2.
        self.parent.update_plot()
    def yshift_bottom(self):
        self.parent.args['y1_min'] -= self.parent.args['dy1']/2.
        self.parent.args['y1_max'] -= self.parent.args['dy1']/2.
        self.parent.update_plot()
