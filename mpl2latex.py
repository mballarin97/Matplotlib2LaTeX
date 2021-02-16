import matplotlib

class Matplotlib2LaTeX():
    """ Plot matplotlib figure in pgf for perfect LaTeX reports
    
        Class to plot matplotlib figures using the pgf backend, swapping easily between
        the two. All the commands that you would use with matplotlib to plot on axes can be
        used with this class, using self.ax

        Attributes
        ----------
        fig: matplotlib.figure.Figure
            Figure that we want to work with
        ax: matplotlib.axes
            Axes of the Figure
        SMALL_SIZE : float, optional
            Size of the font for default text sizes and tick labels. Default 8.
        MEDIUM_SIZE : float, optional
            Font size for x-y labels and legend. Default 10.
        BIGGER_SIZE: float, optional
            Font size for axes title. Default 11.
        BIGGEST_SIZE: float, optional
            Font size fot the figure title. Default 12.
        packages: list of strings, optional
            LaTeX packages to use, in the form "\\usepackage[options]{package}". If None
            only "\\usepackage[utf8]{inputenc}" is used.
        all_backends: list of string
            All possible backends for matplotlib
        original_backend: string
            Original backend when the class is initialized
        original_rcParams: matplotlib.RcParams
            Original rcParams when the class is initialized

        Methods
        -------
        reset(rcparams = None, backend = None)
            Reset matplotlib rcParams and backend to default ones.
            
            Parameters
            ----------
            rcparams : matplotlib.RcParams, optional
                matplotlib rc params. Default is original RcParams
            backend : string
                matplotlib new backend
                
        reset_backend(self, backend=None)
            Reset matplotlib backend
            
            Parameters
            ----------
            backend : string, optional
                Matplotlib backend to reset. Default is original_backend
                
        save_fig(PATH, backend='pgf', tight=True)
            Save the figure with the backend *backend*, coming back to the backend *original_backend* afterwards.
            
            Parameters
            ----------
            PATH: string
                PATH where to save the image
            backend: sting, optional
                backend to use to save the figure. Default pgf
            tight: bool
                If True, use tightlayout
                
       show()
           Show the figure
    """
    
    def __init__(self, fig, SMALL_SIZE=8, MEDIUM_SIZE=10, BIGGER_SIZE=11, BIGGEST_SIZE=12, 
                packages = None):
        
        self.fig = fig
        self.ax = self.fig.axes
        self.SMALL_SIZE = SMALL_SIZE
        self.MEDIUM_SIZE = MEDIUM_SIZE
        self.BIGGER_SIZE = BIGGER_SIZE
        self.BIGGEST_SIZE = BIGGEST_SIZE
        self.all_backends = matplotlib.rcsetup.all_backends
        self.original_backend = matplotlib.pyplot.get_backend()
        self.original_rcParams = matplotlib.rcParams
        
        if packages == None:
            packages = [ "\\usepackage[utf8]{inputenc}" ]
        
        self.packages = packages
        # Set LaTeX params
        matplotlib.rcParams.update({ 
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
            "pgf.preamble": "\n".join( self.packages )
        })
        
        # Set rc params
        matplotlib.pyplot.rc('font', size = self.SMALL_SIZE)          # controls default text sizes
        matplotlib.pyplot.rc('axes', titlesize = self.BIGGER_SIZE)   # fontsize of the axes title
        matplotlib.pyplot.rc('axes', labelsize = self.MEDIUM_SIZE)    # fontsize of the x and y labels
        matplotlib.pyplot.rc('xtick', labelsize = self.SMALL_SIZE)    # fontsize of the tick labels
        matplotlib.pyplot.rc('ytick', labelsize = self.SMALL_SIZE)    # fontsize of the tick labels
        matplotlib.pyplot.rc('legend', fontsize = self.MEDIUM_SIZE)    # legend fontsize
        matplotlib.pyplot.rc('figure', titlesize = self.BIGGEST_SIZE)  # fontsize of the figure title
        
    def reset(self, rcparams = None, backend = None):
        """
            Reset matplotlib rcParams and backend to default ones.
            
            Parameters
            ----------
            rcparams : matplotlib.RcParams, optional
                matplotlib rc params. Default is original RcParams
            backend : string
                matplotlib new backend
        """
        if backend == None:
            backend = self.original_backend
        if rcparams == None:
            rcparams = self.original_rcParams
        # --- reset rcParams ---
        matplotlib.rcParams.update( matplotlib.rcParamsDefault)
        # --- reset backend ---
        self.reset_backend(backend=backend)
        
    def reset_backend(self, backend=None):
        """
            Reset matplotlib backend
            
            Parameters
            ----------
            backend : string, optional
                Matplotlib backend to reset. Default is original_backend
        """
        if backend == None:
            backend = self.original_backend
        matplotlib.use(backend)
            
    def save_fig(self, PATH, backend='pgf', tight=True):
        """Save the figure
        
        Save the figure with the backend *backend*, coming back to the backend *original_backend* afterwards.
        
        Parameters
        ----------
        PATH: string
            PATH where to save the image
        backend: sting, optional
            backend to use to save the figure. Default pgf
        tight: bool
            If True, use tightlayout
        """
        
        matplotlib.use(backend)
        if tight:
            self.fig.tight_layout()
        self.fig.savefig(PATH)
        self.reset()
    
    def show(self):
        matplotlib.pyplot.show()
        
def latex_figsize(wf=0.5, hf=(5.**0.5-1.0)/2.0, columnwidth=510):
    """
        Get the correct figure size to be displayed in a latex report/publication
    
    Parameters
    ----------
    wf : float, optional
        width fraction in columnwidth units. Default to 0.5
    hf : float, optional
        height fraction in columnwidth units. Set by default to golden ratio.
    columnwidth: float 
        width of the column in latex. Get this from LaTeX using \showthe\columnwidth
        Default to 510
        
    Returns
    -------
    fig_size: list of float
        fig_size [width, height] that should be given to matplotlib
    """
    
    fig_width_pt = columnwidth*wf 
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*hf      # height in inches
    return [fig_width, fig_height]