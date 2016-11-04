import sys, os
import matplotlib
matplotlib.use('Qt5Agg') 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np
from analyze_datafile import generate_figs
sys.path.append('../common_libraries')
from IO.files_manip import get_files_with_given_ext
from graphs.my_graph import put_list_of_figs_to_svg_fig

def get_figure_list(DATA_FILE):
    return generate_figs(DATA_FILE)
    
def create_window(parent, FIG_LIST):

    # # get all figures with their size !
    width, height = 0, 0
    for fig in FIG_LIST[:3]:
        size = fig.get_size_inches()*fig.dpi*.9
        width += size[0]
    for fig in FIG_LIST[::3]:
        height += size[1]
    
    # Window size choosen appropriately
    window = QtWidgets.QDialog()
    window.setGeometry(100,150, width, height)
    
    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    CANVAS = []
    for fig in FIG_LIST:
        CANVAS.append(FigureCanvas(fig))

    # this is the Navigation widget
    # it takes the Canvas widget and a parent
    layout = QtWidgets.QGridLayout(window)
    for ic in range(len(CANVAS)):
        layout.addWidget(CANVAS[ic], int(ic/3), ic%3)
    # toolbar = NavigationToolbar(canvas, parent)
    # layout.addWidget(toolbar)
    window.setLayout(layout)
    return window

def get_list_of_files(cdir="/tmp", extensions=['npz', 'abf']):
    FILES = []
    for ext in extensions:
        FILES = FILES+get_files_with_given_ext(cdir, ext)
    return FILES
        
class Window(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None, DATA_LIST=None, KEYS=None):
        
        super(Window, self).__init__(parent)
        self.i_plot = 0
        self.FIG_LIST = []
        self.folder = '/tmp/'
        self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('.-* datavYZ *-.     Data vizualization software -')
        self.setGeometry(50,50,800,60)

        # buttons
        btnq = QtWidgets.QPushButton("Quit (q)", self)
        btnq.clicked.connect(self.close_app)
        btn1 = QtWidgets.QPushButton("Open File (o)", self)
        btn1.clicked.connect(self.file_open)
        btn11 = QtWidgets.QPushButton("Set Folder (f)", self)
        btn11.clicked.connect(self.folder_open)
        btn12 = QtWidgets.QPushButton("Analyze (a)", self)
        btn12.clicked.connect(self.analyze)
        btn2 = QtWidgets.QPushButton("Save as SVG", self)
        btn2.clicked.connect(self.save_as_svg)
        btn3 = QtWidgets.QPushButton("Save as PNG", self)
        btn3.clicked.connect(self.save_as_png)
        btn4 = QtWidgets.QPushButton("Prev. File (p)", self)
        btn4.clicked.connect(self.prev_plot)
        btn5 = QtWidgets.QPushButton("Next File (n)", self)
        btn5.clicked.connect(self.next_plot)
        BTNS = [btnq, btn1, btn11, btn12, btn2, btn3, btn4, btn5]
        for btn, shift in zip(BTNS, 100*np.arange(len(BTNS))):
            btn.move(shift, 0)

        # quit shortcut
        QuitAction = QtWidgets.QAction('Quit', self)
        QuitAction.setShortcut('q')
        QuitAction.setStatusTip('Close the app')
        QuitAction.triggered.connect(self.close_app)
        # next plot shortcut
        NextFile = QtWidgets.QAction('Next File', self)
        NextFile.setShortcut('n')
        NextFile.setStatusTip('Next File')
        NextFile.triggered.connect(self.next_plot)
        # previous plot shortcut
        PrevFile = QtWidgets.QAction('Prev. File', self)
        PrevFile.setShortcut('p')
        PrevFile.setStatusTip('Prev. File')
        PrevFile.triggered.connect(self.prev_plot)
        # update plot shortcut
        UpdatePlot = QtWidgets.QAction('Update', self)
        UpdatePlot.setShortcut('u')
        UpdatePlot.setStatusTip('Update')
        UpdatePlot.triggered.connect(self.update_plot)
        # update plot shortcut
        Analyze = QtWidgets.QAction('Analyze', self)
        Analyze.setShortcut('a')
        Analyze.setStatusTip('Analyze')
        Analyze.triggered.connect(self.analyze)
        # save plot shortcut
        SaveAsSvg = QtWidgets.QAction('Save as .svg', self)
        SaveAsSvg.setShortcut('s')
        SaveAsSvg.setStatusTip('Save as .svg')
        SaveAsSvg.triggered.connect(self.save_as_svg)
        # open folder
        OpenFile = QtWidgets.QAction('Open File', self)
        OpenFile.setShortcut('o') # 'b' for bitmap !!
        OpenFile.setStatusTip('Open File')
        OpenFile.triggered.connect(self.file_open)
        # open file
        OpenFolder = QtWidgets.QAction('Open Folder', self)
        OpenFolder.setShortcut('f') # 'b' for bitmap !!
        OpenFolder.setStatusTip('Open Folder')
        OpenFolder.triggered.connect(self.folder_open)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        
        for eA in [QuitAction, NextFile, PrevFile,\
                   UpdatePlot, Analyze, SaveAsSvg, OpenFile, OpenFolder]:
            fileMenu.addAction(eA)

        self.update_plot()    
        self.show()

    def analyze(self):
        return 0
    
    def update_plot(self):
        self.FIG_LIST = get_figure_list(self.filename)
        self.window = create_window(self, self.FIG_LIST)
        self.window.show()
        self.statusBar().showMessage('DATA file : '+self.filename)
        self.activateWindow()
        
    def close_app(self):
        sys.exit()

    def file_open(self):
        name=QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.filename = name[0]
        self.folder = os.path.split(self.filename)[0]+os.path.sep
        self.update_plot()    

    def folder_open(self):
        name=QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.folder = name+os.path.sep
        self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
        self.update_plot()    
        
    def save_as_svg(self):
        put_list_of_figs_to_svg_fig(self.FIG_LIST,\
                    fig_name='/Users/yzerlaut/Desktop/fig.svg')
        self.statusBar().showMessage(\
                'Figure saved as : /Users/yzerlaut/Desktop/fig.svg')

    def save_as_png(self):
        i=0
        for ii in range(len(self.FIG_LIST)):
            self.FIG_LIST[ii].savefig(\
                    '/Users/yzerlaut/Desktop/fig'+str(ii)+'.png')
        self.statusBar().showMessage(\
                'Figures saved as : ~/Desktop/figXX.png')
        
    def prev_plot(self):
        self.i_plot -=1
        if self.i_plot>=0:
            self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
            self.update_plot()    
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'<1 !!')
            self.i_plot +=1
    def next_plot(self, ii):
        self.i_plot +=1
        if (self.i_plot<len(get_list_of_files())):
            self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
            self.update_plot()    
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'>'+str(len(get_list_of_files())))
            self.i_plot -=1

if __name__ == '__main__':
    import time
    x = np.log(np.abs(np.random.randn(100)))
    y = np.log(np.abs(np.random.randn(100)))
    z = np.log(np.abs(np.random.randn(100)))
    args = {}
    np.savez('/tmp/'+time.strftime("%Y_%m_%d-%H:%M:%S")+'.npz',\
             args={'infos':'toy example'}, y=y, x=x, z=z,\
             plot="""
fig1, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['x'], bins=20, edgecolor='k', color='lightgray', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig2, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['y'], bins=20, edgecolor='b', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig3, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['z'], bins=20, edgecolor='r', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig4, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['z'], bins=20, edgecolor='r', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
""")
    
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
