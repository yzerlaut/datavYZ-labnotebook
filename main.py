import sys, os
import matplotlib
matplotlib.use('Qt5Agg') 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np
from analyze_datafile import plot_data, initialize_quantities_given_datafile, save_as_npz
from IO.files_manip import get_files_with_given_exts, rename_files_for_easy_sorting
from graphs.my_graph import make_multipanel_fig
from automated_analysis import analysis_window

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
    window.setGeometry(100, 150, width, height)
    
    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    CANVAS = []
    for fig in FIG_LIST:
        CANVAS.append(FigureCanvas(fig))

    layout = QtWidgets.QGridLayout(window)
    for ic in range(len(CANVAS)):
        layout.addWidget(CANVAS[ic], int(ic/3), ic%3)
        
    window.setLayout(layout)
            
    if with_toolbar:
        window2 = QtWidgets.QDialog()
        window2.setGeometry(width+320, 320, 70, height/3.)
        layout2 = QtWidgets.QGridLayout(window2)
        for ic in range(len(CANVAS)):
            # this is the Navigation widget, it takes the Canvas widget and a parent
            layout2.addWidget(NavigationToolbar(CANVAS[ic], parent), ic, 0)
    else:
        window2 = None
    return window, window2

def get_list_of_files(cdir="/tmp"):
    return get_files_with_given_exts(cdir)
        
class Window(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None, DATA_LIST=None, KEYS=None):
        
        super(Window, self).__init__(parent)
        
        # buttons and functions
        LABELS = ["q) Quit", "o) Open File", "f) Set Folder", "a) Analyze",\
                  "SVG export", "s) save as PNG", "d) save as .npz", "p) Prev. File", "n) Next File"]
        FUNCTIONS = [self.close_app, self.file_open, self.folder_open, self.analyze,\
                     self.save_as_svg, self.save_as_png, self.save_as_data, self.prev_plot, self.next_plot]
        button_length = 113.
        self.setWindowIcon(QtGui.QIcon('graphs/logo.png'))
        self.setWindowTitle('.-* datavYZ *-.   Data analysis and vizualization software -')
        self.setGeometry(50, 50, button_length*(1+len(LABELS)), 60)

        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu('&File')
        
        for func, label, shift in zip(FUNCTIONS, LABELS,\
                                      button_length*np.arange(len(LABELS))):
            btn = QtWidgets.QPushButton(label, self)
            btn.clicked.connect(func)
            btn.setMinimumWidth(button_length)
            btn.move(shift, 0)
            action = QtWidgets.QAction(label, self)
            action.setShortcut(label.split(')')[0])
            action.triggered.connect(func)
            self.fileMenu.addAction(action)
        self.btn = QtWidgets.QCheckBox("    output \n on Desktop", self)
        self.btn.move(shift+button_length, 0)
        self.btn.stateChanged.connect(self.set_analysis_folder)
        self.btn.setChecked(True)
            
        self.i_plot, self.analysis_flag = 0, False
        self.FolderAnalysisMenu =  None
        self.FIG_LIST, self.args, self.window2, self.window3, self.params = [], {}, None, None, {}
        self.analysis_flag = False
        try:
            self.filename,self.folder,btn_state = np.load('program_data/last_datafile.npy')
            if btn_state=='False': self.btn.setChecked(False)
            self.FILE_LIST = get_list_of_files(self.folder)
            self.i_plot = np.argwhere(self.FILE_LIST==self.filename)[0][0]
            self.args = initialize_quantities_given_datafile(self)
            self.update_plot()    
        except (FileNotFoundError, ValueError, IndexError):
            # self.filename, self.folder = '', ''
            # self.statusBar().showMessage('Provide a datafile of a folder for analysis ')
            self.folder = '/tmp/' # TO be Changed for Cross-Platform implementation !!
            self.FILE_LIST = get_list_of_files(self.folder)
            self.filename = self.FILE_LIST[self.i_plot]
            self.update_plot()    
            
        self.show()

    def set_analysis_folder(self):
        if self.btn.isChecked():
            self.analysis_folder = os.path.join(os.path.expanduser("~"),'Desktop')
            try: self.FolderAnalysisMenu.hide()
            except AttributeError: pass
        else:
            self.analysis_folder = os.path.join(self.folder,'analysis')
            self.FolderAnalysisMenu =  analysis_window.FolderAnalysisMenu(self)
        if not os.path.exists(self.analysis_folder):
            os.makedirs(self.analysis_folder)
        print('analysis folder for now: ', self.analysis_folder)
            
    def analyze(self):
        self.analysis_flag = True
        self.statusBar().showMessage('Analyzing data [...]')
        self.update_plot()    
        return 0
    
    def update_plot(self):
        try:
            self.FIG_LIST = plot_data(self)
        except ValueError: self.statusBar().showMessage('PROBLEM with datafile : '+self.filename+', Check It Manually !!')
        self.window, self.window3 = create_window(self, self.FIG_LIST, with_toolbar=self.analysis_flag)
        self.window.show()
        if self.window3 is not None:
            self.window3.show()
        self.statusBar().showMessage('DATA file : '+self.filename)
        self.activateWindow()
        
    def update_params_and_windows(self):
        self.args = initialize_quantities_given_datafile(self)
        self.update_plot()
        
    def close_app(self):
        if self.filename!='':
            np.save('program_data/last_datafile.npy', [self.filename, self.folder, self.btn.isChecked()])
        sys.exit()

    def file_open(self):
        name=QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',\
                                                   self.folder)
        self.analysis_flag = False
        if self.FolderAnalysisMenu is not None:
            self.FolderAnalysisMenu.close()
        try:
            args = initialize_quantities_given_datafile(self, filename=name[0])
            self.filename = name[0]
            self.folder = os.path.dirname(self.filename)
            self.set_analysis_folder()
            self.FILE_LIST = get_list_of_files(self.folder)
            self.i_plot = np.argwhere(self.FILE_LIST==self.filename)[0][0]
            self.args = args
            self.update_params_and_windows()
        except (IndexError, FileNotFoundError, NoneType):
            self.statusBar().showMessage('/!\ No datafile found... ')

    def folder_open(self):
        name=QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', self.folder)
        if name!='':
            self.folder = name
        self.analysis_flag = False
        rename_files_for_easy_sorting(dir=self.folder)
        try:
            # we first rename the files (add 0, so that '23_01_13' instead of '23_1_13')
            self.set_analysis_folder()
            self.i_plot = 0
            self.FILE_LIST = get_list_of_files(self.folder)
            self.filename = self.FILE_LIST[self.i_plot]
            self.update_params_and_windows()
        except (IndexError, FileNotFoundError, NoneType):
            self.statusBar().showMessage('/!\ No datafile found... ')
            
        
    def save_as_svg(self):
        i=1
        while os.path.isfile(os.path.join(self.analysis_folder,'fig'+str(i)+'.svg')) or os.path.isfile(os.path.join(self.analysis_folder,'fig'+str(i)+'_bitmap.svg')):
            i+=1
        # multipanel figure
        make_multipanel_fig(self.FIG_LIST,\
                fig_name=os.path.join(self.analysis_folder,'fig'+str(i)+'.svg'))
        self.statusBar().showMessage(\
                'Figure saved as : '+os.path.join(self.analysis_folder,'fig'+str(i)+'.svg'))
        
    def save_as_png(self):
        figname=os.path.basename(get_list_of_files(self.folder)[self.i_plot]).split('.')[0]
        i=1
        while os.path.isfile(os.path.join(self.analysis_folder, figname+str(i)+'.png')):
            i+=1
        for ii in range(len(self.FIG_LIST)):
            if not self.analysis_flag:
                self.FIG_LIST[ii].suptitle(figname)
            self.FIG_LIST[ii].savefig(\
                    os.path.join(self.analysis_folder,figname+str(i+ii)+'.png'))
        self.statusBar().showMessage(\
                'Figures saved as : '+\
                    os.path.join(self.analysis_folder,figname+str(i+ii)+'.png'))
        
    def save_as_data(self):
        i=1
        while os.path.isfile(os.path.join(self.analysis_folder, 'data'+str(i)+'.npz')):
            i+=1
        save_as_npz(self, os.path.join(self.analysis_folder, 'data'+str(i)+'.npz'))
        self.statusBar().showMessage('Saving as : '+os.path.join(self.analysis_folder, 'data'+str(i)+'.npz'))
    
    def prev_plot(self):
        self.i_plot -=1
        self.analysis_flag = False
        if self.i_plot>=0:
            self.filename = self.FILE_LIST[self.i_plot]
            self.update_params_and_windows()
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot)+'<1 !!')
            self.i_plot +=1
    def next_plot(self, ii):
        self.i_plot +=1
        self.analysis_flag = False
        if self.i_plot<len(self.FILE_LIST):
            self.filename = self.FILE_LIST[self.i_plot]
            self.update_params_and_windows()
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot)+'>'+str(len(get_list_of_files())))
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
