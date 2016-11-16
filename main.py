import sys, os
import matplotlib
matplotlib.use('Qt5Agg') 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np
from analyze_datafile import plot_data, initialize_quantities_given_datafile
from IO.files_manip import get_files_with_given_ext
from my_graph import put_list_of_figs_to_svg_fig

def create_window(parent, FIG_LIST, with_toolbar=False):

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
        
    # == # adding the matplotlib toolbar ??
    if with_toolbar:
        TOOLBARS = [NavigationToolbar(canva, parent) for canva in CANVAS]
    
    window.setLayout(layout)
    if with_toolbar:
        return window, TOOLBARS
    else:
        return window

def get_list_of_files(cdir="/tmp", extensions=['npz', 'abf']):
    FILES = []
    for ext in extensions:
        FILES = FILES+get_files_with_given_ext(cdir, ext)
    return FILES
        
class Window(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None, DATA_LIST=None, KEYS=None):
        
        super(Window, self).__init__(parent)
        
        self.setWindowIcon(QtGui.QIcon('graphs/logo.png'))
        self.setWindowTitle('.-* datavYZ *-.     Data vizualization software -')
        self.setGeometry(50, 50, 800, 60)

        # buttons and functions
        LABELS = ["q) Quit", "o) Open File", "f) Set Folder", "a) Analyze",\
                  "s) Save SVG", "Save as PNG", "p) Prev. File", "n) Next File"]
        FUNCTIONS = [self.close_app, self.file_open, self.folder_open, self.analyze,\
                     self.save_as_svg, self.save_as_png, self.prev_plot, self.next_plot]

        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu('&File')
        
        for func, label, shift in zip(FUNCTIONS, LABELS, 98*np.arange(len(LABELS))):
            btn = QtWidgets.QPushButton(label, self)
            btn.clicked.connect(func)
            btn.move(shift, 0)
            action = QtWidgets.QAction(label, self)
            action.setShortcut(label.split(')')[0])
            action.triggered.connect(func)
            self.fileMenu.addAction(action)

        self.i_plot = 0
        self.FIG_LIST, self.args, self.window2 = [], {}, None
        try:
            self.filename, self.folder=np.load('__pycache__/last_datafile.npy')
            self.args = initialize_quantities_given_datafile(self)
        except FileNotFoundError:
            self.folder = '/tmp/' # TO be Changed for Cross-Platform implementation !!
            self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
            
        self.update_plot()    
        self.show()
 
    def analyze(self):
        return 0
    
    def update_plot(self):
        self.FIG_LIST = plot_data(self)
        self.window = create_window(self, self.FIG_LIST)
        self.window.show()
        self.statusBar().showMessage('DATA file : '+self.filename)
        self.activateWindow()
        
    def update_params_and_windows(self):
        self.folder = os.path.split(self.filename)[0]+os.path.sep
        # if self.window2 is not None:
        #     initialize_quantities_given_datafile(self)
        #     self.window2.show()
        self.update_plot()
        
    def close_app(self):
        np.save('__pycache__/last_datafile.npy', [self.filename, self.folder])
        sys.exit()

    def file_open(self):
        name=QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        args = initialize_quantities_given_datafile(self, filename=name[0])
        if args is not None:
            self.filename = name[0]
            self.args = args
            self.update_params_and_windows()
        else:
            self.statusBar().showMessage('/!\ UNRECOGNIZED /!\ Datafile : ')

    def folder_open(self):
        name=QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.folder = name+os.path.sep
        self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
        self.update_params_and_windows()
        
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
            self.update_params_and_windows()
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'<1 !!')
            self.i_plot +=1
    def next_plot(self, ii):
        self.i_plot +=1
        if (self.i_plot<len(get_list_of_files())):
            self.filename = self.folder+\
                get_list_of_files(self.folder)[self.i_plot]
            self.update_params_and_windows()
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'>'+str(len(get_list_of_files())))
            self.i_plot -=1

if __name__ == '__main__':
    import time
    x = np.log(np.abs(np.random.randn(100)))
    y = np.log(np.abs(np.random.randn(100)))
    z = np.log(np.abs(np.random.randn(100)))
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
