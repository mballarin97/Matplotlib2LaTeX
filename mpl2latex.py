import matplotlib
import matplotlib.pyplot as plt

class mpl2latex():
    """ Plot matplotlib figure in pgf for perfect LaTeX reports
    
        Context to plot matplotlib figures using the pgf backend, swapping easily between
        the two. Simply put your plotting commands inside the context, and enable the pgf with
        the *back_flag*

        Attributes
        ----------
        back_flag: bool
            If True use the backend *backend* with all the details
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
        original_backend: string
            Original backend when the class is initialized
        original_rcParams: matplotlib.RcParams
            Original rcParams when the class is initialized
        backend : string, optional
            Matplotlib backend to use. Default is pgf


        Methods
        -------
        def __init__(self, back_flag, packages = None, backend='pgf'):
            Initialize the class.
            
            Parameters
            ----------
            back_flag: bool
            If True use the backend *backend* with all the details
            packages: list of strings, optional
                LaTeX packages to use, in the form "\\usepackage[options]{package}". If None
                only "\\usepackage[utf8]{inputenc}" is used.
            original_backend: string
                Original backend when the class is initialized
            original_rcParams: matplotlib.RcParams
                Original rcParams when the class is initialized
            backend : string, optional
                Matplotlib backend to use. Default is pgf
                
        __enter__(self)
            enter in the context

        __exit__(self)
            exit from the context
            
        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> x = np.linspace(0, 100, 1000)
        >>> flag = True
        >>> # Write the usual plotting instruction inside the context
        >>> with mpl2ltx(flag):
        >>>     plt.plot(x, x**2)
        >>>     plt.savefig('trial.pgf')
        >>> # produces the plots and save it in pgf as intended

                             
    """
    
    def __init__(self, back_flag, packages = None, backend='pgf'):

        self.back_flag = back_flag
        self.original_backend = matplotlib.pyplot.get_backend()
        self.original_rcParams = matplotlib.rcParams
        self.backend = backend

        if packages == None:
            packages = [ "\\usepackage[utf8]{inputenc}" ]
        self.packages = packages
        

    def __enter__(self):
        """ If *self.back_flag* is True set all the rc parameters and the correct backend. If False only sets the fontsizes.
        """
        if self.back_flag:
            # Set LaTeX params
            matplotlib.rcParams.update({ 
                "pgf.texsystem": "pdflatex",
                'font.family': 'serif',
                'text.usetex': True,
                'pgf.rcfonts': False,
                "pgf.preamble": "\n".join( self.packages ),
            })
            matplotlib.use( self.backend )


    def __exit__(self, etype, value, traceback):
        """ When exiting the context return to usual parameters, i.e. to original backend and original rcparams
        """
        # --- reset rcParams ---
        matplotlib.rcParams.update( self.original_rcParams )
        # --- reset backend ---
        matplotlib.use( self.original_backend )
        
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