from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np

class FocusMenu(QtWidgets.QDialog):
    
    def __init__(self, parent):
        
        super(FocusMenu, self).__init__(parent)
        self.parent = parent
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('Window Focus')
        self.setGeometry(parent.screen_width-300,150,120,170)

        self.ACTIONS = []
        self.set_grid_and_actions()
        
        self.show()

    def set_grid_and_actions(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        names = ['', '', '(i) ^ ', '',
                 '', '(j) <', '(k) v', '(l) >',
                 '', '', '', '',
                 '(z) X-Out', '(x) Y-Out', '(c) Y-In ', '(v) X-In ']
        shortcuts = ['', '', 'i', '',
                     '', 'j', 'k', 'l',
                     '', '', '', '',
                     'z', 'x', 'c', 'v']
        FUNCS = ['', '', self.yshift_up, '',\
                 '', self.xshift_left, self.yshift_bottom, self.xshift_right,
                 '', '', '', '',
                 self.xzoom_out, self.yzoom_out, self.yzoom_in, self.xzoom_in]
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

        self.sl = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.sl.setGeometry(60, 150, 320, 20)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(0)
        self.sl.setTickInterval(1)
        self.sl.valueChanged.connect(self.valuechange)
        
    def remove_actions(self):
        for action in self.ACTIONS:
            self.parent.fileMenu.removeAction(action)

    def valuechange(self):
        size = self.sl.value()
        self.parent.args['x1'] = self.parent.params['tstart']+\
                                 size/100.*(self.parent.params['tstop']-self.parent.params['tstart'])
        self.parent.args['x2'] = self.parent.args['x1']+self.parent.args['dx']
        self.parent.update_plot()
      
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
        print('to be re-implemented, broken')
        # self.parent.args['dy1'] /=2.
        # self.parent.args['y1_min'] = self.parent.args['y1_min']+self.parent.args['dy1']/2.
        # self.parent.args['y1_max'] = self.parent.args['y1_min']+self.parent.args['dy1']
        self.parent.update_plot()
    def yzoom_out(self):
        print('to be re-implemented, broken')
        # self.parent.args['dy1'] *=2.
        # self.parent.args['y1_min'] = self.parent.args['y1_min']-self.parent.args['dy1']/4.
        # self.parent.args['y1_max'] = self.parent.args['y1_min']+self.parent.args['dy1']
        self.parent.update_plot()
    def xshift_right(self):
        self.parent.args['x1'] += self.parent.args['dx']/3.
        self.parent.args['x2'] += self.parent.args['dx']/3.
        self.parent.update_plot()
    def xshift_left(self):
        self.parent.args['x1'] -= self.parent.args['dx']/3.
        self.parent.args['x2'] -= self.parent.args['dx']/3.
        self.parent.update_plot()
    def yshift_up(self):
        print('to be re-implemented, broken')
        # self.parent.args['y1_min'] += self.parent.args['dy1']/3.
        # self.parent.args['y1_max'] += self.parent.args['dy1']/3.
        self.parent.update_plot()
    def yshift_bottom(self):
        print('to be re-implemented, broken')
        # self.parent.args['y1_min'] -= self.parent.args['dy1']/3.
        # self.parent.args['y1_max'] -= self.parent.args['dy1']/3.
        self.parent.update_plot()
