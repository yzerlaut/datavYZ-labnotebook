from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import svgutils.compose as sg
import svgutils.transform as sgt
import os, string
import numpy as np
mpl.rcParams.update({'font.size': 14})
import sys
sys.path.append('../')
from IO.files_manip import get_files_with_given_exts

def set_plot(ax, spines=['left', 'bottom'],\
                num_xticks=5, num_yticks=5,\
                xlabel='', ylabel='', tck_outward=5,\
                xticks=None, yticks=None,\
                xticks_labels=None, yticks_labels=None,\
                xticks_rotation=0, yticks_rotation=0,\
                xlim_enhancment=2, ylim_enhancment=2,\
                xlim=None, ylim=None):
    
    # drawing spines
    adjust_spines(ax, spines, tck_outward=tck_outward)
    
    # Boundaries
    if xlim is None:
        xmin, xmax = ax.get_xaxis().get_view_interval()
        dx = xmax-xmin
        xlim = [xmin-xlim_enhancment*dx/100.,xmax+xlim_enhancment*dx/100.]
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(xlim)
    if ylim is None:
        ymin, ymax = ax.get_yaxis().get_view_interval()
        dy = ymax-ymin
        ylim = [ymin-ylim_enhancment*dy/100.,ymax+ylim_enhancment*dy/100.]
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(ylim)
    ax.plot(xlim, ylim, 'w.', alpha=0.)

    if (xticks is None) and ('bottom' or 'top' in spines):
        ax.xaxis.set_major_locator( MaxNLocator(nbins = num_xticks) )
    else:
        ax.set_xticks(xticks)
        
    if xticks_labels is not None:
        ax.set_xticklabels(xticks_labels, rotation=xticks_rotation)

    if (yticks is None) and ('left' or 'right' in spines):
        ax.yaxis.set_major_locator( MaxNLocator(nbins = num_yticks) )
    else:
        ax.set_yticks(yticks)
        
    if yticks_labels is not None:
        ax.set_yticklabels(yticks_labels, rotation=yticks_rotation)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def ticks_number(ax, xticks=3, yticks=3):
    if xticks>1:
        ax.xaxis.set_major_locator( MaxNLocator(nbins = xticks) )
    if yticks>1:
        ax.yaxis.set_major_locator( MaxNLocator(nbins = yticks) )


def adjust_spines(ax, spines, tck_outward=3):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', tck_outward)) # outward by 10 points by default
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])

def set_subplot_safe_for_labels(fig, FIGSIZE=None, FONTSIZE=16,
                                    hspace=0.1, vspace=0.1):
    if FIGSIZE is None:
        FIGSIZE = [fig.get_figwidth(), fig.get_figheight()]
    x0, y0 = .15*FONTSIZE/FIGSIZE[0], .15*FONTSIZE/FIGSIZE[0]
    fig.subplots_adjust(\
                bottom=x0, left=y0,\
                right=max([1.-0.02*FONTSIZE/FIGSIZE[0],x0*1.1]),
                top=max([1.-0.02*FONTSIZE/FIGSIZE[1],y0*1.1]),
                hspace=hspace)

def inch_to_cm(x):
    inch = 2.54 # one inch is 2.54cm
    return inch*x

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)    

    

def build_bar_legend(X, ax, mymap, label='$\\nu$ (Hz)',\
                     bounds=None,ticks_labels=None,
                     orientation='vertical', scale='linear',\
                     color_discretization=None):
    """ X -> ticks """
    if color_discretization is None:
        color_discretization = len(X)
        
    # scale : 'linear' / 'log' / 'custom'
    if scale is 'linear':
        if bounds is None:
            bounds = [X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2.]
        bounds = np.linspace(bounds[0], bounds[1], color_discretization)
    elif scale is 'log10':
        if bounds is None:
            bounds = [int(np.log(X[0])/np.log(10))-.1*int(np.log(X[0])/np.log(10)),\
                      int(np.log(X[-1])/np.log(10))+1+.1*int(np.log(X[-1])/np.log(10))]
        else:
            bounds = [np.log(bounds[0])/np.log(10), np.log(bounds[1])/np.log(10)]
        bounds = np.logspace(bounds[0], bounds[1], color_discretization)
    elif scale is 'custom':
        bounds = np.linspace(X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2., color_discretization)
        
    norm = mpl.colors.BoundaryNorm(bounds, mymap.N)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=mymap, norm=norm,\
                                   orientation=orientation)
    cb.set_ticks(X)
    if ticks_labels is not None:
        cb.set_ticklabels(ticks_labels)
    cb.set_label(label)
    return cb

def get_linear_colormap(color1='blue', color2='red'):
    return mpl.colors.LinearSegmentedColormap.from_list(\
                        'mycolors',[color1, color2])

def translate_to_bitmap_if_too_big(fig, svgfig,\
                                   size_limit_for_svg=500000., DPI=100.):
    if os.path.getsize(svgfig)>size_limit_for_svg:
        print(svgfig+' is of size:',os.path.getsize(svgfig))
        pngfig = svgfig.replace('.svg', '.png')
        fig.savefig(pngfig, format='png', dpi=DPI, transparent=True)
        os.system('convert '+pngfig+' '+svgfig)
        print('NEW '+svgfig+' is of size:',os.path.getsize(svgfig))
        return True
    else:
        return False
    
def make_multipanel_fig(FIGS, CAP_SIZE=14,\
                                fig_name="fig.svg",\
                                size_limit_for_svg=500000.,
                                transparent=True, correc_factor=70., DPI=100.):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]

    SIZE = []
    for fig in FIGS:
        SIZE.append(fig.get_size_inches())
    width = np.max([s[0] for s in SIZE])
    height = np.max([s[1] for s in SIZE])

    LABELS, XCOORD, YCOORD, SCALE = [], [], [], []
        
    for i in range(len(FIGS)):
        ff = 'f.svg'
        FIGS[i].savefig('/tmp/'+str(i)+'.svg', format='svg', transparent=transparent)
        if translate_to_bitmap_if_too_big(FIGS[i], '/tmp/'+str(i)+'.svg'):
            SCALE.append(.7)
        else:
            SCALE.append(1.)
        LABELS.append(label[i])
        XCOORD.append((i%3)*width*correc_factor)
        YCOORD.append(int(i/3)*height*correc_factor)

    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG('/tmp/'+str(i)+'.svg').move(XCOORD[i],YCOORD[i]).scale(SCALE[i]),\
            sg.Text(LABELS[i], 25, 20, size=22, weight='bold').move(\
                                                XCOORD[i]-15,YCOORD[i]))\
        )
    sg.Figure(str((min(len(FIGS)%3,3))*inch_to_cm(width))+"cm",\
              str(inch_to_cm(height)*(int(len(FIGS)/3.01)+1))+"cm",\
              *PANELS).save(fig_name)

