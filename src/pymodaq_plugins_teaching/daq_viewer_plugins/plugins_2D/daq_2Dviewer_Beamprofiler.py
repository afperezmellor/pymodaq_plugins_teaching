import numpy as np
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins
from pymodaq_data import DataToExport
from pymodaq_plugins_mockexamples.daq_viewer_plugins.plugins_2D.daq_2Dviewer_BSCamera import DAQ_2DViewer_BSCamera

import laserbeamsize as lbs
from pyqtgraph.examples.SpinBox import labels


class DAQ_2DViewer_Beamprofiler(DAQ_2DViewer_BSCamera):

    live_mode_available = False

    params = DAQ_2DViewer_BSCamera.params + [
        {'title':'beam', 'name':'beam', 'type':'bool', 'value':True, 'visible':True, 'readonly':False},
        {'title': 'position', 'name': 'bpos', 'type': 'bool', 'value': True, 'visible': True, 'readonly': False},
        {'title': 'size', 'name': 'bsize', 'type': 'bool', 'value': True, 'visible': True, 'readonly': False},
        {'title': 'angle', 'name': 'bangle', 'type': 'bool', 'value': True, 'visible': True, 'readonly': False}
                ]

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following

        data = self.average_data(Naverage)
        beam = data[0].data[0]

        x, y, d_major, d_minor, phi = lbs.beam_size(beam)


        dte = DataToExport('Beamprofiler',
                           data=[
                               DataFromPlugins('Beam',
                                               data=[beam],
                                               labels=['Raw beam'],
                                               do_plot=self.settings['beam']),
                               DataFromPlugins('Position',
                                               data=[np.atleast_1d(x), np.atleast_1d(y)],
                                               labels=['x', 'y'],
                                               do_plot=self.settings['bpos'] ),
                               DataFromPlugins('Size',
                                               data=[np.atleast_1d(d_major), np.atleast_1d(d_minor)],
                                               labels=['Major', 'Minor'],
                                               do_plot=self.settings['bsize'] ),
                               DataFromPlugins('Angle',
                                               data=[np.atleast_1d(phi)],
                                               labels=['phi'],
                                               do_plot=self.settings['bangle'] ),
                           ]

                           )

        self.dte_signal.emit(dte)


if __name__ == '__main__':
    main(__file__)
