from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np
from PIL import Image
import sys, os
sys.path.append('../')
import IO

def pngs_to_one_pdf_page(images, RESOLUTION=300, N=8):
    """
    images is a list of strings ['file1.png', 'files2.png', ...]
    is has to be of size 8 maximum !!! (to fit on a pdf page)
    this function creates a file called 'page.pdf'
    --------------- options 
    RESOLUTION =300 Dot Per Inches
    figure_proportion = 5./7. height over width, set in matplotlib.figure.figsize
    """
    if len(images)>N:
        print("Error, images should be of size "+str(N)+"8 maximum")
    # A4 at resolution
    width, height = int(8.27 *RESOLUTION), int(11.7 *RESOLUTION) 
    # IMAGESIZE = int(4.5*figure_proportion*RESOLUTION), int(4.5*RESOLUTION)
    fig_width = 3.5
    fig_height = 2.2
    IMAGESIZE0 = int(fig_width*RESOLUTION), int(fig_height*RESOLUTION)
    x0 = 0.5
    x1 = x0+fig_width+.1
    y0 = .8
    y1, y2, y3 = y0+fig_height+.2,y0+2*fig_height+2*.2, y0+3*fig_height+3*.2
    coords = [\
              [int(x0*RESOLUTION), int(y0*RESOLUTION)],
              [int(x0*RESOLUTION), int(y1*RESOLUTION)],
              [int(x0*RESOLUTION), int(y2*RESOLUTION)],
              [int(x0*RESOLUTION), int(y3*RESOLUTION)],
              [int(x1*RESOLUTION), int(y0*RESOLUTION)],
              [int(x1*RESOLUTION), int(y1*RESOLUTION)],
              [int(x1*RESOLUTION), int(y2*RESOLUTION)],
              [int(x1*RESOLUTION), int(y3*RESOLUTION)]]
    page = Image.new('RGB', (width, height), 'white')
    for i in range(len(images)):
        # im = Image.open(images[i]).rotate(90)
        im = Image.open(images[i])
        width, height = im.size
        if width/height>fig_width/fig_height:
            # width is the largest, so limiting one !
            IMAGESIZE = IMAGESIZE0[0], int(IMAGESIZE0[0]*height/width)
        else:
            IMAGESIZE = int(IMAGESIZE0[1]*width/height), IMAGESIZE0[1] 
        im = im.resize((IMAGESIZE))
        page.paste(im, box=(coords[i][0],coords[i][1]))
    page.save('page.pdf')
    
def loop_over_pngs_and_generate_pdf(folder, N=8):
    """
    loop over all the png files in a folder and create a multipages
    pdf that plot them 12 by 12 !!
    """
    list_of_figs = []
    first_one = True
    PNG_list = IO.files_manip.get_files_with_given_exts(folder, EXTS=['png'])
    for fn in PNG_list:
        list_of_figs.append(fn)
        if len(list_of_figs)==N:
            pngs_to_one_pdf_page(list_of_figs)
            if first_one:
                os.system('mv page.pdf full_figures.pdf')
                first_one=False
            else:
                os.system('pdftk full_figures.pdf page.pdf cat output full_figures2.pdf')
                os.system('mv full_figures2.pdf full_figures.pdf')
            list_of_figs = []
    if len(list_of_figs)>0: # need to plot the last figures
        pngs_to_one_pdf_page(list_of_figs)
        if not first_one:
            os.system('pdftk full_figures.pdf page.pdf cat output full_figures2.pdf')
            os.system('mv full_figures2.pdf full_figures.pdf')
            # now let's clean up a bit
            os.system('rm page.pdf')
        else:
            os.system('mv page.pdf full_figures.pdf')
    os.system('mv full_figures.pdf '+folder+os.path.sep+'full_figures.pdf')
    
class FolderAnalysisMenu(QtWidgets.QDialog):
    
    def __init__(self, parent):
        
        super(FolderAnalysisMenu, self).__init__(parent)
        self.parent = parent
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('Folder Analysis')
        self.setGeometry(920,400,200,70)

        # buttons and functions
        LABELS = ["Merge Figures on PDF", "** -- View Pdf -- **"]
        FUNCTIONS = [self.make_pdf, self.open]
        button_height = 25.

        for func, label, shift in zip(FUNCTIONS, LABELS, button_height*np.arange(len(LABELS))):
            btn = QtWidgets.QPushButton(label, self)
            btn.clicked.connect(func)
            btn.setMinimumHeight(button_height)
            btn.setMinimumWidth(100.)
            btn.move(3, shift)

        self.show()

    def open(self):
        os.system('open '+self.parent.analysis_folder+os.path.sep+'full_figures.pdf')

    def make_pdf(self):
        loop_over_pngs_and_generate_pdf(self.parent.analysis_folder)



    
        
