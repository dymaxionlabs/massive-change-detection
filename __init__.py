# -*- coding: utf-8 -*-

__author__ = 'Damián Silvani'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MassiveChangeDetection class from file MassiveChangeDetection.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .massive_change_detection import MassiveChangeDetectionPlugin
    return MassiveChangeDetectionPlugin()
