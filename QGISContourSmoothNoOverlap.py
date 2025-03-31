import glob, shutil, time, os
from pathlib import Path
startTime = time.time()


"""
##########################################################
User options
"""

#Variable assignment
contourLayer     = "C:/Temp/TestContours.gpkg"

#Options for compressing the images, ZSTD has the best speed but LZW is the most compatible
compressOptions  = 'COMPRESS=ZSTD|NUM_THREADS=ALL_CPUS|PREDICTOR=1|ZSTD_LEVEL=1|BIGTIFF=IF_SAFER|TILED=YES'


"""
##########################################################
Variable assignment for processing
"""

#Get the location of the initial image for storage of processing files
rootProcessDirectory = str(Path(contourLayer).parent.absolute()).replace('\\','/') + '/'

contourName = contourLayer.split("/")
contourName = contourName[-1]
contourName = contourName[:len(contourName)-5]


#Making a folder for processing each time, to avoid issues with locks
processDirectory = rootProcessDirectory + contourName + 'Process' + '/'
if not os.path.exists(processDirectory): os.mkdir(processDirectory)


"""
##########################################################
Processing
"""

processing.run("native:multiparttosingleparts", {'INPUT':contourLayer,'OUTPUT':processDirectory + 'ContourSingle.gpkg'})

processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourSingle.gpkg','FIELD_NAME':'ContNum','FIELD_TYPE':1,'FIELD_LENGTH':0,'FIELD_PRECISION':0,'FORMULA':'@id','OUTPUT':processDirectory + 'ContourWithID.gpkg'})

processing.run("native:simplifygeometries", {'INPUT':processDirectory + 'ContourWithID.gpkg','METHOD':0,'TOLERANCE':0.25,'OUTPUT':processDirectory + 'ContourWithIDSimp.gpkg'})

processing.run("grass7:v.generalize", {'input':processDirectory + 'ContourWithIDSimp.gpkg','type':[0],'cats':'','where':'','method':7,'threshold':1,'look_ahead':7,'reduction':50,'slide':1,'angle_thresh':0,
    'degree_thresh':0,'closeness_thresh':0,'betweeness_thresh':0,'alpha':1,'beta':1,'iterations':1,'-t':False,'-l':True,'output':processDirectory + 'ContourWithIDSimpSmooth.gpkg','error':'TEMPORARY_OUTPUT','GRASS_REGION_PARAMETER':None,
    'GRASS_SNAP_TOLERANCE_PARAMETER':-1,'GRASS_MIN_AREA_PARAMETER':0.0001,'GRASS_OUTPUT_TYPE_PARAMETER':0,'GRASS_VECTOR_DSCO':'','GRASS_VECTOR_LCO':'','GRASS_VECTOR_EXPORT_NOCAT':False})
        
processing.run("native:extractvertices", {'INPUT':processDirectory + 'ContourWithIDSimpSmooth.gpkg','OUTPUT':processDirectory + 'ContourWithIDSimpSmoothVertices.gpkg'})

processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpSmoothVertices.gpkg','FIELD_NAME':'VertexID','FIELD_TYPE':2,'FIELD_LENGTH':0,'FIELD_PRECISION':0,
    'FORMULA':' to_string("ContNum")  + \'_\' +  to_string("vertex_index") ','OUTPUT':processDirectory + 'ContourWithIDSimpSmoothVerticesID.gpkg'})
    
processing.run("qgis:exportaddgeometrycolumns", {'INPUT':processDirectory + 'ContourWithIDSimpSmoothVerticesID.gpkg','CALC_METHOD':0,'OUTPUT':processDirectory + 'ContourWithIDSimpSmoothVerticesIDGeom.gpkg'})
    
    
    
processing.run("native:extractvertices", {'INPUT':processDirectory + 'ContourWithIDSimp.gpkg','OUTPUT':processDirectory + 'ContourWithIDSimpVertices.gpkg'})

processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpVertices.gpkg','FIELD_NAME':'VertexID','FIELD_TYPE':2,'FIELD_LENGTH':0,'FIELD_PRECISION':0,
    'FORMULA':' to_string("ContNum")  + \'_\' +  to_string("vertex_index") ','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesID.gpkg'})
    


processing.run("native:joinattributestable", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesID.gpkg','FIELD':'VertexID','INPUT_2':processDirectory + 'ContourWithIDSimpSmoothVerticesIDGeom.gpkg',
    'FIELD_2':'VertexID','FIELDS_TO_COPY':['xcoord','ycoord'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'Sm','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoined.gpkg'})


processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoined.gpkg','FIELD_NAME':'XDiff','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,'FORMULA':' "Smxcoord" - $x','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiff.gpkg'})

processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiff.gpkg','FIELD_NAME':'YDiff','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,'FORMULA':' "Smycoord" - $y','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiff.gpkg'})


processing.run("native:buffer", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiff.gpkg','DISTANCE':5,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,
    'SEPARATE_DISJOINT':False,'OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5.gpkg'})
    
processing.run("native:joinbylocationsummary", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5.gpkg','PREDICATE':[0],'JOIN':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiff.gpkg',
    'JOIN_FIELDS':['XDiff','YDiff'],'SUMMARIES':[6],'DISCARD_NONMATCHING':False,'OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5Join.gpkg'})

processing.run("native:buffer", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5Join.gpkg','DISTANCE':5,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,
    'SEPARATE_DISJOINT':False,'OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5.gpkg'})

processing.run("native:joinbylocationsummary", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5.gpkg','PREDICATE':[0],'JOIN':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiff.gpkg',
    'JOIN_FIELDS':['XDiff','YDiff'],'SUMMARIES':[6],'DISCARD_NONMATCHING':False,'OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5Join.gpkg'})
    
processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5Join.gpkg','FIELD_NAME':'AveXShift','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,
    'FORMULA':'("XDiff_mean" +  "XDiff_mean_2" )/2','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5JoinAveX.gpkg'})
    
processing.run("native:fieldcalculator", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5JoinAveX.gpkg','FIELD_NAME':'AveYShift','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,
    'FORMULA':'("YDiff_mean" +  "YDiff_mean_2" )/2','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5JoinAveXAveY.gpkg'})
    
    
    
processing.run("native:joinattributestable", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesID.gpkg','FIELD':'VertexID','INPUT_2':processDirectory + 'ContourWithIDSimpVerticesIDJoinedXDiffYDiffBuff5JoinBuff5JoinAveXAveY.gpkg',
    'FIELD_2':'VertexID','FIELDS_TO_COPY':['AveXShift','AveYShift'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'Av','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDAve.gpkg'})
    
    
processing.run("native:affinetransform", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDAve.gpkg','DELTA_X':QgsProperty.fromExpression('"AvAveXShift"'),'DELTA_Y':QgsProperty.fromExpression('"AvAveYShift"'),'DELTA_Z':0,'DELTA_M':0,'SCALE_X':1,'SCALE_Y':1,'SCALE_Z':1,'SCALE_M':1,'ROTATION_Z':0,
    'OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDAveShifted.gpkg'})
    
processing.run("native:pointstopath", {'INPUT':processDirectory + 'ContourWithIDSimpVerticesIDAveShifted.gpkg','CLOSE_PATH':False,'ORDER_EXPRESSION':'"vertex_index"',
    'NATURAL_SORT':False,'GROUP_EXPRESSION':'"ContNum"','OUTPUT':processDirectory + 'ContourWithIDSimpVerticesIDAveShiftedLines.gpkg'})


"""
##########################################################
Final time message
"""

endTime = time.time()
totalTime = endTime - startTime
print("Done, this took " + str(int(totalTime)) + " seconds")
