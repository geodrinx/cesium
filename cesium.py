# -*- coding: utf-8 -*-
"""
/***************************************************************************
 cesium
                                 A QGIS plugin
 cesium
                              -------------------
        begin                : 2014-05-14
        copyright            : (C) 2014 by geodrinx
        email                : geodrinx@gmail.com
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from cesiumdialog import cesiumDialog
import os.path

import qgis
import codecs

import webbrowser


class cesium:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'cesium_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = cesiumDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/cesium/icon.png"),
            u"cesium", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&cesium", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&cesium", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):

				tempdir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/cesium/_WebServer/temp"
				

#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
				layer = self.iface.mapCanvas().currentLayer()
				if layer:
				  if layer.type() == layer.VectorLayer:				

				    name = layer.source();
				    nomeLayer = layer.name()
				    nomeLay   = nomeLayer.replace(" ","_")

				    numFeatures = layer.featureCount()
				    print ("numFeatures %d") %(numFeatures)
    				          
      				    
				    crsSrc = layer.crs();

				    crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				    xform = QgsCoordinateTransform(crsSrc, crsDest)

#----------------------------------------------------------------------------
#  Trasformo la finestra video in coordinate layer, 
#     per estrarre solo gli elementi visibili
#----------------------------------------------------------------------------
				    iface = qgis.utils.iface
				    
				    boundBox = iface.mapCanvas().extent() 
                
				    xMin = float(boundBox.xMinimum())
				    yMin = float(boundBox.yMinimum())

				    xMax = float(boundBox.xMaximum())                
				    yMax = float(boundBox.yMaximum())
				    
				    
				    crs2 = self.iface.mapCanvas().mapRenderer().destinationCrs()
				    crsSrc2  = QgsCoordinateReferenceSystem(crs2.authid())   
				    crsDest2 = QgsCoordinateReferenceSystem(layer.crs())   
				    xform2   = QgsCoordinateTransform(crsSrc2, crsDest2)
                              
				    pt0 = xform2.transform(QgsPoint(xMin, yMin))
				    pt1 = xform2.transform(QgsPoint(xMax, yMax))
				    
				    rect = QgsRectangle(pt0, pt1)
				    
#----------------------------------------------------------------------------

				    rq = QgsFeatureRequest(rect)

				    iter = layer.getFeatures(rq)
            
#  CONTEGGIO gli elementi da esportare -----------------------

				    nele = 0
				    for feat in iter:
				        nele = nele + 1

#  RICARICO la geometria ---------------------------------------		    
				    iter = layer.getFeatures(rq)

# ---------------------------------------------------------------------------
#    INIZIO scrittura  geoJSON 
# ---------------------------------------------------------------------------

				    out_folder = tempdir
				
				    kml = codecs.open(out_folder + '/CesiumDoc.geojson', 'w', encoding='utf-8')

				    #Write the geoJson header

				    kml.write('{\n')
				    kml.write('"type": "FeatureCollection",\n')
				    kml.write('"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },\n') 
				    kml.write('\n')

				    kml.write('"features": [')
				    
				    numE = 0
				    for feat in iter:

				        numE = numE + 1
                				        		      
				        # Leggo la geometria dell'elemento
				      
				        geom = feat.geometry()
				      
				        kml.write ('\n{ "type": "Feature", ')
                 
# DESCRIPTION DATA-----------
				        			        
				        kml.write ('"properties": {')

 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()
				        print num
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1			           
				           stringazza = (' "%s": "%s"') %(f.name(),feat[iii]) # QUA c'è una virgola di troppo
				           kml.write (stringazza)
				           if(iii < num-1):
				              kml.write (',')
				        kml.write (' }, ')

#  Scrivo la geometria dell'elemento corrente ------------
				        kml.write ('"geometry": ')		        
				        stringazza =  geom.exportToGeoJSON()
				        kml.write (stringazza)
				        
				        kml.write (' } ')

				        if (numE < nele):
				              kml.write (',')

				        
				    #----- Fine Ciclo Elementi da esportare
				    

				    kml.write (']\n')
				    kml.write ('}\n')

				    kml.close()
# ---------------------------------------------------------------------------				
#    FINE scrittura  geoJSON 
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------				
#    INIZIO scrittura  czml 
# ---------------------------------------------------------------------------


#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
				layer = self.iface.mapCanvas().currentLayer()
				if layer:
				  if layer.type() == layer.VectorLayer:				

				    out_folder = tempdir
				
				    kml = codecs.open(out_folder + '/CesiumDoc.czml', 'w', encoding='utf-8')

				    #Write the czml header

				    kml.write('[{\n')
				    kml.write('        "id" : "document",\n')
				    kml.write('        "version" : "1.0"\n')
				    kml.write('    }, {\n\n')

				    rq = QgsFeatureRequest(rect)

				    iter = layer.getFeatures(rq)
            
#  CICLO per ogni elemento da esportare -----------------------
				    
				    for feat in iter:
				    
				      nele = feat.id()
              				      
				      # fetch geometry
				      geom = feat.geometry()
				       # show some information about the feature
				      
				      if geom.type() == QGis.Point:

				        kml.write ('    "point":{	\n')			        


				      elif geom.type() == QGis.Line:

				        kml.write ('    "line":{\n')



				      elif geom.type() == QGis.Polygon:

				        kml.write ('    "polygon":{\n')
				        kml.write ('      "positions":{\n')
				        kml.write ('        "cartographicDegrees":[\n          ')
				        
				        elem = geom.asPolygon()

				        for iii in range (len(elem)):

#				          if (iii == 1):				          
#				            kml.write ('         </coordinates>\n')
#				            kml.write ('         </LinearRing>\n')
#				            kml.write ('         </outerBoundaryIs>\n')
#				            kml.write ('         <innerBoundaryIs>\n')
#				            kml.write ('         <LinearRing>\n')
#				            kml.write ('         <coordinates>\n')
#
#				          if (iii > 1):				          
#				            kml.write ('         </coordinates>\n')
#				            kml.write ('         </LinearRing>\n')
#				            kml.write ('         </innerBoundaryIs>\n')
#				            kml.write ('         <innerBoundaryIs>\n')
#				            kml.write ('         <LinearRing>\n')
#				            kml.write ('         <coordinates>\n')
	
				          npunti = len(elem[iii])

				          np = -1
				          
				          for jjj in range (len(elem[iii])):
				                         
				            x1,y1 = elem[iii][jjj][0], elem[iii][jjj][1]
				            
				            pt1 = xform.transform(QgsPoint(x1, y1))
                           
				            stringazza =   ('%.9lf,%.9lf,0') % (pt1.x(), pt1.y())
				            kml.write (stringazza)
				            
				            np = np + 1
				            
				            if (np < npunti-1):
				              kml.write (',')				            

#				        if (iii == 0):
#				           kml.write ('         </coordinates>\n')
#				           kml.write ('        </LinearRing>\n')
#				           kml.write ('     </outerBoundaryIs>\n')
#				           kml.write ('   </Polygon>\n')
#
#				        if (iii > 0):
#				           kml.write ('         </coordinates>\n')
#				           kml.write ('        </LinearRing>\n')
#				           kml.write ('     </innerBoundaryIs>\n')
#				           kml.write ('   </Polygon>\n')
	
				        kml.write ('\n        ]\n')

				        kml.write ('      },\n')
				        kml.write ('      "material":{\n')
				        kml.write ('        "solidColor":{\n')
				        kml.write ('          "color":{\n')
				        kml.write ('            "rgba":[\n')
				        kml.write ('              255,0,0,77\n')
				        kml.write ('            ]\n')
				        kml.write ('          }\n')
				        kml.write ('        }\n')
				        kml.write ('      },\n')
				        kml.write ('      "fill":true,\n')
				        kml.write ('      "outline":true,\n')
				        kml.write ('      "outlineColor":{\n')
				        kml.write ('        "rgba":[\n')
				        kml.write ('          255,0,0,255\n')
				        kml.write ('        ]\n')
				        kml.write ('      }\n')
				        kml.write ('    }\n')
				        
				    #----- Fine Ciclo Elementi da esportare
				    

				    kml.write ('  }]\n')

				    kml.close()




				webbrowser.open_new("http://localhost:8000")
