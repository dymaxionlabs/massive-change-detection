# -*- coding: utf-8 -*-

__author__ = 'Damián Silvani'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt4.QtCore import QSettings
from qgis.core import QgsVectorFileWriter, QgsMessageLog, QgsMapLayerRegistry
from qgis.utils import iface

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.ProcessingLog import ProcessingLog
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterRaster, ParameterVector, ParameterBoolean, ParameterNumber, ParameterSelection, ParameterTableField
from processing.core.outputs import OutputRaster, OutputVector, OutputTable
from processing.tools import dataobjects, vector

from osgeo import gdal
from osgeo.gdalconst import *
import numpy as np
import cv2
import rasterio
import rasterio.mask
import fiona
from shapely.geometry import shape, box


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

    OUTPUT_RASTER_LAYER = 'OUTPUT_RASTER_LAYER'
    OUTPUT_VECTOR_LAYER = 'OUTPUT_VECTOR_LAYER'
    OUTPUT_TABLE_LAYER = 'OUTPUT_TABLE_LAYER'
    INPUT_LOTS_LAYER = 'INPUT_LOTS_LAYER'
    INPUT_LOT_ID_FIELD = 'INPUT_LOT_ID_FIELD'
    INPUT_A_LAYER = 'INPUT_A_LAYER'
    INPUT_B_LAYER = 'INPUT_B_LAYER'

    AUTO_THRESHOLD = 'AUTO_THRESHOLD'
    THRESHOLD = 'THRESHOLD'
    FILTER = 'FILTER'
    FILTER_TYPES = ['NONE', 'MEDIAN', 'GAUSSIAN']
    FILTER_KERNEL_SIZE = 'FILTER_KERNEL_SIZE'
    GENERATE_CD_VECTOR = 'GENERATE_CD_VECTOR'
    SELECTION_THRESHOLD = 'SELECTION_THRESHOLD'

    def defineCharacteristics(self):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # The name that the user will see in the toolbox
        self.name = 'Multiband difference'

        # The branch of the toolbox under which the algorithm will appear
        self.group = 'Change Detection'

        # Main parameters
        self.addParameter(ParameterVector(self.INPUT_LOTS_LAYER,
            self.tr('Input Lots vector layer'), [ParameterVector.VECTOR_TYPE_ANY], False))

        self.addParameter(ParameterRaster(self.INPUT_A_LAYER,
            self.tr('Input old layer'), [ParameterRaster], False))

        self.addParameter(ParameterRaster(self.INPUT_B_LAYER,
            self.tr('Input new layer'), [ParameterRaster], False))

        self.addParameter(ParameterTableField(self.INPUT_LOT_ID_FIELD,
            self.tr('Lot id field'), self.INPUT_LOTS_LAYER))

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

        self.addParameter(ParameterNumber(
            self.SELECTION_THRESHOLD,
            self.tr('Lot selection threshold value'),
            0.0, 1.0, 0.5))

        # Outputs raster and table
        self.addOutput(OutputRaster(self.OUTPUT_RASTER_LAYER,
            self.tr('CD raster')))
        self.addOutput(OutputVector(self.OUTPUT_VECTOR_LAYER,
            self.tr('CD vector')))
        self.addOutput(OutputTable(self.OUTPUT_TABLE_LAYER,
            self.tr('CD table')))

    def processAlgorithm(self, progress):
        self.generateChangeDetectionRaster(progress)
        self.writeVectorAndTable(progress)

        self.log('Done!')

    def generateChangeDetectionRaster(self, progress):
        # The first thing to do is retrieve the values of the parameters
        # entered by the user
        inputAFilename = self.getParameterValue(self.INPUT_A_LAYER)
        inputBFilename = self.getParameterValue(self.INPUT_B_LAYER)
        outputFilename = self.getOutputValue(self.OUTPUT_RASTER_LAYER)

        if inputAFilename == inputBFilename:
            raise GeoAlgorithmExecutionException(self.tr('You must use two different raster images for inputs A and B'))

        threshold = self.getParameterValue(self.THRESHOLD)
        autoThreshold = self.getParameterValue(self.AUTO_THRESHOLD)
        if autoThreshold:
            threshold = None

        filterType = self.FILTER_TYPES[self.getParameterValue(self.FILTER)]
        if filterType == 'NONE':
            filterType = None
        kernelSize = self.getParameterValue(self.FILTER_KERNEL_SIZE)

        # Open and assign the contents of the raster file to a dataset
        datasetA = gdal.Open(inputAFilename, GA_ReadOnly)
        datasetB = gdal.Open(inputBFilename, GA_ReadOnly)

        # For now only operate on the first band only
        self.log('Read rasters into arrays')
        arrayA = self._readIntoArray(datasetA)[0]
        arrayB = self._readIntoArray(datasetB)[0]

        self.log('arrayA shape: {}'.format(arrayA.shape))
        self.log('arrayB shape: {}'.format(arrayB.shape))

        # And now we can process...
        out = self._detectChanges(arrayA, arrayB,
                threshold=threshold,
                filterType=filterType,
                kernelSize=kernelSize)
        self.log('Output shape: {}'.format(out.shape))

        if not np.any(out):
            raise GeoAlgorithmExecutionException(self.tr('No changed detected. Try to use a lower threshold value or different images'))

        # Create output raster dataset
        driver = gdal.GetDriverByName('GTiff')
        outDataset = driver.Create(outputFilename,
                datasetA.RasterXSize,
                datasetA.RasterYSize,
                1,
                gdal.GDT_Byte)

        # Write output band
        outband = outDataset.GetRasterBand(1)
        outband.WriteArray(out)
        outband.SetNoDataValue(0)
        outband.FlushCache()

        # Check if there is geotransformation or geoprojection
        # in the input raster and set them in the resulting dataset
        if datasetA.GetGeoTransform() != None:
            outDataset.SetGeoTransform(datasetA.GetGeoTransform())

        if datasetA.GetProjection() != None:
            outDataset.SetProjection(datasetA.GetProjection())

        # Clean resources
        datasetA = datasetB = None
        outDataset = None

    def writeVectorAndTable(self, progress):
        cdFilename = self.getOutputValue(self.OUTPUT_RASTER_LAYER)
        imgFilename = self.getParameterValue(self.INPUT_B_LAYER)
        lotsFilename = self.getParameterValue(self.INPUT_LOTS_LAYER)
        lotIdFieldName = self.getParameterValue(self.INPUT_LOT_ID_FIELD)
        selectionThreshold = self.getParameterValue(self.SELECTION_THRESHOLD)

        outputTable = self.getOutputFromName(self.OUTPUT_TABLE_LAYER)
        columns = ['lot_id', 'change', 'area', 'changed_area', 'change_perc']
        writer = outputTable.getTableWriter(columns)

        outputVector = self.getOutputValue(self.OUTPUT_VECTOR_LAYER)

        with fiona.open(lotsFilename) as lotsDs, rasterio.open(cdFilename) as cdDs, rasterio.open(imgFilename) as imgDs:
            if lotsDs.crs != cdDs.crs:
                raise GeoAlgorithmExecutionException(self.tr('Lots vector file has different CRS than rasters: {} != {}').format(lotsDs.crs, cdDs.crs))

            total = 100.0 / len(lotsDs) if len(lotsDs) > 0 else 1
            progress.setInfo(self.tr('Processing lot features...'))

            invalidGeomCount = 0

            newSchema = lotsDs.schema.copy()
            newSchema['properties']['changed_area'] = 'float'
            newSchema['properties']['change_perc'] = 'float'
            kwargs = dict(driver=lotsDs.driver,
                    crs=lotsDs.crs,
                    schema=newSchema)
            bbox = box(*cdDs.bounds)
            with fiona.open(outputVector, 'w', **kwargs) as dst:
                for i, feat in enumerate(lotsDs):
                    progress.setPercentage(int(i * total))
                    lotId = feat['properties'][lotIdFieldName]

                    # Skip features with invalid geometries
                    if not feat['geometry']:
                        continue

                    # Skip features that are not inside rasters bounds
                    poly = shape(feat['geometry'])
                    if not bbox.contains(poly):
                        continue

                    # Calculate change percentage
                    try:
                        cdImg, _ = rasterio.mask.mask(cdDs, [feat['geometry']], crop=True)
                        img, _ = rasterio.mask.mask(imgDs, [feat['geometry']], crop=True)
                    except ValueError as err:
                        self.log(self.tr("Error on lot id {}: {}. Skipping").format(lotId, err))
                        continue

                    # Skip features with no pixels in raster (too low resolution?)
                    totalPixels = np.sum(img[0] > 0)
                    if totalPixels == 0:
                        self.log(self.tr("Lot {} has no pixels? Skipping...").format(lotId))
                        continue

                    count = np.sum(cdImg[0] > 0)
                    perc = count / float(totalPixels)
                    changeDetected = perc >= selectionThreshold

                    # Calculate areas
                    poly = shape(feat['geometry'])
                    area = poly.area
                    changedArea = poly.area * perc

                    # Build row for table
                    row = {}
                    row['lot_id'] = lotId
                    if changeDetected:
                        row['change'] = 'Y'
                    else:
                        row['change'] = 'N'
                    row['area'] = float(area)
                    row['changed_area'] = float(changedArea)
                    row['change_perc'] = float(perc)

                    writer.addRecord([row[k] for k in columns])

                    # Add feature in output vector file on change
                    if changeDetected:
                        newFeat = feat.copy()
                        newFeat['properties'] = newFeat['properties'].copy()
                        newFeat['properties']['changed_area'] = float(changedArea)
                        newFeat['properties']['change_perc'] = float(perc)
                        dst.write(newFeat)

        del writer


    def _readIntoArray(self, dataset):
        """Return a numpy array from a GDAL dataset"""
        bands = []
        for i in xrange(dataset.RasterCount):
            band = dataset.GetRasterBand(i+1).ReadAsArray(0, 0,
                    dataset.RasterXSize,
                    dataset.RasterYSize)
            bands.append(band)
        return np.array(bands)

    def _normalize(self, img):
        vmin, vmax = img.min(), img.max()
        norm_img = (img - vmin) / (vmax - vmin)
        return norm_img

    def _difference(self, a, b):
        a = a.astype(np.int32)
        b = b.astype(np.int32)
        mean_a, mean_b = a.mean(), b.mean()
        std_a, std_b = a.std(), b.std()

        b_norm = ((std_a / std_b) * (b - np.ones(b.shape) * mean_b)) + mean_a
        return np.abs(a - b_norm)

    def log(self, message):
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO,
                self.tr(message))


    def _threshold(self, src, tau):
        return (((src > 0) * (src >= tau)) * 255).astype(np.uint8)

    def _otsuThreshold(self, src):
        src = (src * 255).astype(np.uint8)
        _, dst = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return dst

    def _medianFilter(self, src, kernel_size=3):
        if kernel_size % 2 == 0:
            raise GeoAlgorithmExecutionException(self.tr('Kernel size for median filter must be an odd number'))
        return cv2.medianBlur(src, kernel_size)

    def _gaussFilter(self, src, kernel_size=3):
        return cv2.GaussianBlur(src, (kernel_size, kernel_size), 1, 1)

    def _detectChanges(self, img1, img2, threshold=None, filterType=None, kernelSize=3):
        res = self._difference(img1, img2)
        res = self._normalize(res)

        if threshold:
            res = self._threshold(res, threshold)
            self.log('Applied manual threshold of value {}'.format(threshold))
        else:
            res = self._otsuThreshold(res)
            self.log('Applied Otsu threshold')

        if filterType == 'GAUSSIAN':
            res = self._gaussFilter(res, kernelSize)
        elif filterType == 'MEDIAN':
            res = self._medianFilter(res, kernelSize)
        else:
            raise GeoAlgorithmExecutionException(self.tr('Unhandled filter type: {}').format(filterType))

        if filterType:
            self.log('Applied {} filter with kernel size {}'.format(filterType, kernelSize))

        return res
