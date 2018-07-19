# -*- coding: utf-8 -*-

__author__ = 'Dymaxion Labs'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt4.QtCore import QSettings
from qgis.core import QgsVectorFileWriter

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterRaster, ParameterVector, ParameterBoolean, ParameterNumber, ParameterSelection
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector


class MassiveChangeDetectionAlgorithm(GeoAlgorithm):
    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LOTS_LAYER = 'INPUT_LOTS_LAYER'
    INPUT_A_LAYER = 'INPUT_A_LAYER'
    INPUT_B_LAYER = 'INPUT_B_LAYER'

    AUTO_THRESHOLD = 'AUTO_THRESHOLD'
    THRESHOLD = 'THRESHOLD'
    FILTER = 'FILTER'
    FILTER_TYPES = ['NONE', 'MEDIAN', 'GAUSSIAN']
    FILTER_KERNEL_SIZE = 'FILTER_KERNEL_SIZE'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        self.name = 'Multiband difference'

        # The branch of the toolbox under which the algorithm will appear
        self.group = 'Change Detection'

        # Main parameters
        self.addParameter(ParameterRaster(self.INPUT_LOTS_LAYER,
            self.tr('Input Lots vector layer'), [ParameterVector.VECTOR_TYPE_ANY], False))

        self.addParameter(ParameterRaster(self.INPUT_A_LAYER,
            self.tr('Input old layer'), [ParameterRaster], False))

        self.addParameter(ParameterRaster(self.INPUT_B_LAYER,
            self.tr('Input new layer'), [ParameterRaster], False))

        # Threshold parameters
        self.addParameter(ParameterBoolean(
            self.AUTO_THRESHOLD,
            self.tr('Use automatic thresholding'),
            True))
        self.addParameter(ParameterNumber(
            self.THRESHOLD,
            self.tr('Threshold value (if not automatic)'),
            0.0, 1.0, 0.5))

        # Filter parameters
        self.addParameter(ParameterSelection(
            self.FILTER,
            self.tr('Filter type'),
            self.FILTER_TYPES, 1))
        self.addParameter(ParameterNumber(self.FILTER_KERNEL_SIZE,
            self.tr('Filter kernel size'),
            2.0, None, 3.0))

        # We add a vector layer as output
        self.addOutput(OutputVector(self.OUTPUT_LAYER,
            self.tr('Output layer with selected features')))

    def processAlgorithm(self, progress):
        """Here is where the processing itself takes place."""

        # The first thing to do is retrieve the values of the parameters
        # entered by the user
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        output = self.getOutputValue(self.OUTPUT_LAYER)

        # Input layers vales are always a string with its location.
        # That string can be converted into a QGIS object (a
        # QgsVectorLayer in this case) using the
        # processing.getObjectFromUri() method.
        vectorLayer = dataobjects.getObjectFromUri(inputFilename)

        # And now we can process

        # First we create the output layer. The output value entered by
        # the user is a string containing a filename, so we can use it
        # directly
        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        provider = vectorLayer.dataProvider()
        writer = QgsVectorFileWriter(output, systemEncoding,
                                     provider.fields(),
                                     provider.geometryType(), provider.crs())

        # Now we take the features from input layer and add them to the
        # output. Method features() returns an iterator, considering the
        # selection that might exist in layer and the configuration that
        # indicates should algorithm use only selected features or all
        # of them
        features = vector.features(vectorLayer)
        for f in features:
            writer.addFeature(f)

        # There is nothing more to do here. We do not have to open the
        # layer that we have created. The framework will take care of
        # that, or will handle it if this algorithm is executed within
        # a complex model
