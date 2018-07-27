# -*- coding: utf-8 -*-
"""
/***************************************************************************
 tile_plus
                                 A QGIS plugin
 tile plus
                              -------------------
        begin                : 2018-07-15
        git sha              : $Format:%H$
        copyright            : (C) 2018 by geodose
        email                : ideagora.geomatics@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qgis.core import QgsRasterLayer
from qgis.core import QgsProject
import time
from xml.dom import minidom

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .tile_plus_dialog import tile_plusDialog
import os.path

map_list=["Select Map"]
url_list=[""]
desc_list=[""]
zmin_list=[""]
zmax_list=[""]
data=open(os.path.join(os.path.dirname(__file__), "basemap.xml"))
xmldoc = minidom.parse(data)
map = xmldoc.getElementsByTagName('map')
url=xmldoc.getElementsByTagName('url')
zoom=xmldoc.getElementsByTagName('zoom')
type=xmldoc.getElementsByTagName('type')
desc=xmldoc.getElementsByTagName('description')
n_map=len(map)

for i in range(n_map):
    map_name=map[i].attributes['name'].value
    url_name=url[i].firstChild.nodeValue
    desc_val=desc[i].firstChild.nodeValue
    zmin_val=zoom[i].attributes['min'].value
    zmax_val=zoom[i].attributes['max'].value
    map_list.append(map_name)
    url_list.append(url_name)
    desc_list.append(desc_val)
    zmin_list.append(zmin_val)
    zmax_list.append(zmax_val)

map_list_sorted=sorted(map_list)
start_text="This plugin enable you to add some popular basemap and tile services. Select a map in the list and click <b>OK</b> to add the map to QGIS map canvas...<a href='http://www.geodose.com'>Help</a>"
data.close()

class tile_plus:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'tile_plus_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = tile_plusDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Tile+')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Tile+')
        self.toolbar.setObjectName(u'Tile+')
        self.dlg.comboBox.currentIndexChanged.connect(self.info)

    def info(self):
        combo_name=self.dlg.comboBox.currentText()
        map_index=map_list.index(combo_name)
        combo_url=url_list[map_index]
        text_desc=desc_list[map_index]
        info_link='http://www.geodose.com/p/tile-plus-plugin.html#'+combo_name.replace(" ","%20")
        if combo_name=="Select Map":
            self.dlg.textBrowser.setText(start_text)
        else:
            self.dlg.textBrowser.setText(text_desc+"<br>"+combo_url+"<br><a href="+info_link+">More detail</a>")
        self.dlg.textBrowser.show()
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('tile_plus', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.add_action(
            icon_path,
            text=self.tr(u'Tile+'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        self.dlg.comboBox.addItem("Select Map")
        combo_list=sorted(map_list[1::])
        for s in range(n_map):
            self.dlg.comboBox.addItem(combo_list[s])        
        self.dlg.textBrowser.setText(start_text)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Tile+'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

	    
    def run(self):
        """Run method that performs all the real work"""

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            combo_name=self.dlg.comboBox.currentText()
            map_index=map_list.index(combo_name)
            url_name=url_list[map_index]
            zmin=zmin_list[map_index]
            zmax=zmax_list[map_index]
            #uri="url="+url_name+"&zmax="+"19"+"&zmin="+"0"+"&type="+"xyz"
            uri="url="+url_name+"&zmax="+zmax+"&zmin="+zmin+"&type="+"xyz"
            rlayer=QgsRasterLayer(uri,combo_name,'wms')
            QgsProject.instance().addMapLayer(rlayer)
        
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #pass
