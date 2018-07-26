# coding=utf-8
"""MultibandDifferenceAlgorithm Test

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'Damián Silvani'
__date__ = '2018-07-25'
__copyright__ = '(C) 2018 by Dymaxion Labs'

import unittest
import os

from PyQt4 import QtGui, QtTest
from qgis.core import (
    QgsMapLayerRegistry,
    QgsRasterLayer)
from qgis.gui import QgsMapCanvasLayer

import sys
print("*** {}".format(sys.path))

from utilities import get_qgis_app
APP, CANVAS, IFACE, _ = get_qgis_app()


class MultibandDifferenceAlgorithmTest(unittest.TestCase):
    """Test multiband difference algorithm."""

    def _setUp(self):
        """Runs before each test."""

        # create a map canvas widget
        CANVAS.setCanvasColor(QtGui.QColor('white'))
        CANVAS.enableAntiAliasing(True)

        # load a shapefile
        self.beforePath = os.path.join('data', 'before.tif')
        beforeLayer = QgsRasterLayer(self.beforePath, 'before', 'ogr')

        # add the layer to the canvas and zoom to it
        QgsMapLayerRegistry.instance().addMapLayer(beforeLayer)
        CANVAS.setLayerSet([QgsMapCanvasLayer(beforeLayer)])
        CANVAS.setExtent(beforeLayer.extent())

        # import the plugin to be tested
        import massive_change_detection
        self.plugin = massive_change_detection.classFactory(IFACE)
        self.plugin.initGui()
        self.dlg = self.plugin.dlg

    def _test_populated(self):
        '''Are the combo boxes populated correctly?'''
        self.assertEqual(self.dlg.ui.comboBox_raster.currentText(), '')
        self.assertEqual(self.dlg.ui.comboBox_vector.currentText(), 'MasterMap')
        self.assertEqual(self.dlg.ui.comboBox_all1.currentText(), '')
        self.dlg.ui.comboBox_all1.setCurrentIndex(1)
        self.assertEqual(self.dlg.ui.comboBox_all1.currentText(), 'MasterMap')

    def _test_dlg_name(self):
        self.assertEqual(self.dlg.windowTitle(), 'Testing')

    def _test_click_widget(self):
        '''The OK button should close the dialog'''
        self.dlg.show()
        self.assertEqual(self.dlg.isVisible(), True)
        okWidget = self.dlg.ui.buttonBox.button(self.dlg.ui.buttonBox.Ok)
        QtTest.QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(self.dlg.isVisible(), False)

    def _tearDown(self):
        """Runs after each test."""
        self.plugin.unload()
        del(self.plugin)


if __name__ == "__main__":
    suite = unittest.makeSuite(MultibandDifferenceAlgorithmTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
