# -*- coding: utf-8 -*-

__author__ = 'Damián Silvani'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from PyQt4.QtCore import QSettings, QTranslator, QCoreApplication
from processing.core.Processing import Processing
from .provider import MassiveChangeDetectionProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class MassiveChangeDetectionPlugin:
    def __init__(self):
        self.provider = MassiveChangeDetectionProvider()
        self.pluginDir = os.path.dirname(os.path.realpath(__file__))
        self._load_translations()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)

    def _load_translations(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.pluginDir, 'i18n', '{}.qm'.format(locale))
        if os.path.exists(localePath):
            translator = QTranslator()
            translator.load(localePath)
            QCoreApplication.installTranslator(translator)
