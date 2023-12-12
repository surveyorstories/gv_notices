"""
surveyor stories
Name : ground validation notice 
Group : 
With QGIS : 32603
"""

from qgis.core import QgsProcessingParameterFeatureSink
import processing
import inspect
from qgis.PyQt.QtGui import QIcon
import os
from qgis.core import (QgsProcessing,
                       QgsProject, QgsVectorLayer,
                       QgsProcessingAlgorithm, QgsExpressionContextUtils,
                       QgsExpression,
                       QgsProcessingParameterFile, QgsFillSymbol,
                       QgsProcessingParameterString,
                       QgsProcessingParameterField,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterBoolean,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterVectorLayer)


# Get the path to the current project folder
project = QgsProject.instance()
project_folder = project.readPath("./")



class Gv_notice(QgsProcessingAlgorithm):
   
    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def initAlgorithm(self, config=None):
        if QgsExpressionContextUtils.globalScope().variable('district_eng'):
            options = ['Alluri Sitharama Raju', 'Anakapalli',  'Anantapuram',  'Annamayya',  'Bapatla',  'Chittoor',  'East Godavari',  'Eluru',  'Guntur',  'Kakinada',  'Dr. B. R. Ambedkar Konaseema',  'Krishna', 'Kurnool',
                       'Nandyal',  'NTR',  'Palnadu',  'Parvathipuram Manyam',  'Prakasam',  'Sri Potti Sriramulu Nellore',  'Sri Sathya Sai',  'Srikakulam',  'Tirupati',  'Visakhapatnam',  'Vizianagaram',  'West Godavari',  'YSR Kadapa']
            dname = QgsExpressionContextUtils.globalScope().variable('district_eng')
            dname = options.index(dname)
        else:
            dname = None

        self.addParameter(QgsProcessingParameterString('village_name_please_enter_your_village_name_in_telugu',
                          'Village Name (Please enter your Village Name in Telugu)', multiLine=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterString('mandal_name_please_enter_mandal_name_in_telugu',
                          'Mandal Name (Please enter Mandal Name in Telugu)', multiLine=False, defaultValue=None))

        self.addParameter(QgsProcessingParameterEnum('district_name_eng', 'Choose Your District', options=['Alluri Sitharama Raju', 'Anakapalli',  'Anantapuram',  'Annamayya',  'Bapatla',  'Chittoor',  'East Godavari',  'Eluru',  'Guntur',  'Kakinada',  'Dr. B. R. Ambedkar Konaseema',  'Krishna', 'Kurnool',
                          'Nandyal',  'NTR',  'Palnadu',  'Parvathipuram Manyam',  'Prakasam',  'Sri Potti Sriramulu Nellore',  'Sri Sathya Sai',  'Srikakulam',  'Tirupati',  'Visakhapatnam',  'Vizianagaram',  'West Godavari',  'YSR Kadapa'], allowMultiple=False, usesStaticStrings=False, defaultValue=dname))
        self.addParameter(QgsProcessingParameterVectorLayer(
            'choose_your_data', 'Choose your data', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('mode_of_generation', 'Mode of Generation ', options=[
                          'Khata Number Wise ', 'Land Parcel Wise'], allowMultiple=False, usesStaticStrings=False, defaultValue=None))

        self.addParameter(QgsProcessingParameterField('choose_land_parcel_column', 'Choose Land Parcel Column',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_khata_number_column', 'Choose Khata Number Column',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_sysubdivision_number', 'Choose Sy-Subdivision Number',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))

        self.addParameter(QgsProcessingParameterField('choose_acres_column_as_per_resurvey', 'Choose Acres Column as per Resurvey',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_hectres_column_as_per_resurvey', 'Choose Hectres Column as per Resurvey',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_acres_as_per_old_data', 'Choose Acres as per Old data', optional=True,
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_hectres_as_per_old_data', 'Choose Hectres as per Old data', optional=True,
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_pattadarname_column', 'Choose Pattadar Name Column',
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue='k*'))
        self.addParameter(QgsProcessingParameterField('choose_pattadarrelationname_column', 'Choose Pattadar Relation Name Column',
                          optional=True, type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('choose_remarks_column', 'Choose Remarks Column', optional=True,
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('choose_classification_column', 'Choose your Classification Column',         optional=True,
                          type=QgsProcessingParameterField.Any, parentLayerParameterName='choose_your_data', allowMultiple=False, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        QgsProject.instance().write()

        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        project = QgsProject.instance()
        project_folder = project.readPath("./")
        param_value = parameters['choose_your_data']
        layer_names = ['Notices_Data', 'Khata_Data']

        layers = project.mapLayers().values()
        root = project.layerTreeRoot()
        for name in layer_names:

            layers_to_remove = project.mapLayersByName(name)
            for layer in layers_to_remove:
                root.removeLayer(layer)

        layer = project.mapLayer(param_value)
        if layer:
            layer_name = layer.name()
        else:
            print('lpm layer is not loaded to project')
            print(param_value)

            # Save vector features to file
            alg_params = {
                'DATASOURCE_OPTIONS': '',
                'INPUT':  parameters['choose_your_data'],
                'LAYER_NAME': 'Village_Data',
                'LAYER_OPTIONS': '',
                'OUTPUT': project_folder + '/Village_Data.json'
            }
            saved_outputs = processing.run(
                'native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            layer = QgsVectorLayer(
                saved_outputs['OUTPUT'], 'Village_Data', 'delimitedtext')
            project.addMapLayer(layer, True)
            layer_name = layer.name()
            print(layer_name)
            param_value = layer.id()

        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model

        # Set district project variable variable
        district_list = {'Alluri Sitharama Raju': 'అల్లూరి సీతారామ రాజు', 'Anakapalli': 'అనకాపల్లి',  'Anantapuram': 'అనంతపురం',  'Annamayya': 'అన్నమయ్య',  'Bapatla': 'బాపట్ల',  'Chittoor': 'చిత్తూరు',  'East Godavari': 'తూర్పు గోదావరి',  'Eluru': 'ఏలూరు',  'Guntur': 'గుంటూరు ',  'Kakinada': 'కాకినాడ',  'Dr. B. R. Ambedkar Konaseema': 'కోనసీమ',  'Krishna': 'కృష్ణా', 'Kurnool': 'కర్నూలు',
                         'Nandyal': 'నంద్యాల',  'NTR': 'యన్.టి.ఆర్',  'Palnadu': 'పల్నాడు',  'Parvathipuram Manyam': 'పార్వతీపురం మన్యం',  'Prakasam': 'ప్రకాశం ',  'Sri Potti Sriramulu Nellore': 'నెల్లూరు',  'Sri Sathya Sai': 'శ్రీ సత్య సాయి',  'Srikakulam': 'శ్రీకాకుళం ',  'Tirupati': 'తిరుపతి',  'Visakhapatnam': 'విశాఖపట్నం ',  'Vizianagaram': 'విజయనగరం ',  'West Godavari': 'పశ్చిమ గోదావరి',  'YSR Kadapa': 'వై.యస్.ర్ కడప'}

        # Convert dictionary items to a list
        items_list = list(district_list.items())
        index = parameters['district_name_eng']
        if index < len(items_list):
            key, value = items_list[index]
            print("Key:", key)
            print("Value:", value)

            # District_Name enlish
            QgsExpressionContextUtils.setGlobalVariable(
                'district_eng', key.title())
            # QgsExpressionContextUtils.setProjectVariable(
            #         project, 'district_eng', key)

            # District_Name telugu
            QgsExpressionContextUtils.setGlobalVariable('District_Name', value)

        # Village_Name
        alg_params = {
            'NAME': 'notice_village',
            'VALUE': parameters['village_name_please_enter_your_village_name_in_telugu']
        }
        outputs['Village_name'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(1)
       # '😎💥Oohoo! YOU and I just started Our journey together, hopping for better end.' + '\n')
        if feedback.isCanceled():
            return {}

        # Mandal_Name
        alg_params = {
            'NAME': 'notice_mandal',
            'VALUE': parameters['mandal_name_please_enter_mandal_name_in_telugu']
        }
        outputs['Mandal_name'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(parameters['choose_khata_number_column']), 'length': 0, 'name': 'khata_no', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                               {'expression': '\"{}\"'.format(parameters['choose_land_parcel_column']), 'length': 0,
                                'name': 'lpm_no', 'precision': 0, 'sub_type': 0, 'type': 2, 'type_name': 'integer'},
                               {'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(parameters['choose_sysubdivision_number']), 'length': 0, 'name': 'sy_sdno', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'}, {
                                   'expression': '\"{}\"'.format(parameters['choose_hectres_as_per_old_data']), 'length': 0, 'name': 'old_hect', 'precision': 4, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'}, {'expression': '\"{}\"'.format(parameters['choose_acres_as_per_old_data']), 'length': 0, 'name': 'old_acre', 'precision': 3, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'},
                               {'expression': '\"{}\"'.format(parameters['choose_hectres_column_as_per_resurvey']), 'length': 0, 'name': 'new_hect', 'precision': 4,
                                   'sub_type': 0, 'type': 6, 'type_name': 'double precision'},
                               {'expression': '\"{}\"'.format(parameters['choose_acres_column_as_per_resurvey']), 'length': 0, 'name': 'new_acre', 'precision': 3,
                                'sub_type': 0, 'type': 6, 'type_name': 'double precision'},
                               {'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(parameters['choose_pattadarname_column']), 'length': 0,
                                'name': 'pattadar', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                               {'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(parameters['choose_pattadarrelationname_column']), 'length': 0,
                                'name': 'pattadarrelation', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                               {'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(parameters['choose_classification_column']), 'length': 0,
                                'name': 'classf', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                               {'expression': ' regexp_replace(\"{}\", \'\\\\s+\', \' \')\r\n'.format(
                                   parameters['choose_remarks_column']), 'length': 0, 'name': 'remarks_c', 'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                               ],
            'INPUT': parameters['choose_your_data'],
            'OUTPUT': (project_folder + '/Notices_Data.gpkg')

        }
        refactorFields = processing.run(
            'native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        if parameters['mode_of_generation'] == 0:
            atlas_pg_var = '''"khata_no"'''

            lpm_var = '''aggregate('Notices_Data','concatenate',to_string("lpm_no"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            sy_no_var = '''aggregate('Notices_Data','concatenate',to_string("sy_sdno"), "khata_no" = @atlas_pagename , concatenator:='$%*<>^~@')'''
            old_ac_var = '''aggregate('Notices_Data','concatenate',to_string("old_acre"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            old_hect_var = '''aggregate('Notices_Data','concatenate',to_string("old_hect"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            new_ac_var = '''aggregate('Notices_Data','concatenate',to_string("new_acre"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            new_hect_var = '''aggregate('Notices_Data','concatenate',to_string("new_hect"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            remarks_var = '''aggregate('Notices_Data','concatenate',to_string("remarks_c"), "khata_no" = @atlas_pagename , 
            concatenator:='$%*<>^~@')'''
            classfication_var = '''aggregate('Notices_Data','concatenate',to_string("classf"), "khata_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            lpm_var_r = '''array_to_string(aggregate('Notices_Data','array_agg',to_string("lpm_no"), "khata_no" = @atlas_pagename,concatenator:=','))'''

            # Delete duplicates by attribute
            alg_params = {
                'FIELDS':  'khata_no',
                'INPUT':  refactorFields['OUTPUT'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            DeleteDuplicatesByAttribute = processing.run(
                'native:removeduplicatesbyattribute', alg_params, context=context, is_child_algorithm=True)
            # Retain fields In KHATA
            alg_params = {
                'FIELDS': ['khata_no', 'pattadar', 'pattadarrelation'],

                'INPUT': DeleteDuplicatesByAttribute['OUTPUT'],
                'OUTPUT': project_folder + '/Khata_Data.gpkg'
            }
            RetainFieldsInKHATA = processing.run(
                'native:retainfields', alg_params, context=context,  is_child_algorithm=True)

            feedback.setCurrentStep(4)
            if feedback.isCanceled():
                return {}

            khata_layer = QgsVectorLayer(
                RetainFieldsInKHATA['OUTPUT'], 'Khata_Data', 'ogr')
            project.addMapLayer(khata_layer, True)

            atlas_coverlayer = 'Khata_Data'

        if parameters['mode_of_generation'] == 1:

            atlas_pg_var = '''"lpm_no"'''

            lpm_var = '''aggregate('Notices_Data','concatenate',to_string("lpm_no"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            sy_no_var = '''aggregate('Notices_Data','concatenate',to_string("sy_sdno"), "lpm_no" = @atlas_pagename , concatenator:='$%*<>^~@')'''
            old_ac_var = '''aggregate('Notices_Data','concatenate',to_string("old_acre"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            old_hect_var = '''aggregate('Notices_Data','concatenate',to_string("old_hect"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            new_ac_var = '''aggregate('Notices_Data','concatenate',to_string("new_acre"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            new_hect_var = '''aggregate('Notices_Data','concatenate',to_string("new_hect"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            remarks_var = '''aggregate('Notices_Data','concatenate',to_string("remarks_c"), "lpm_no" = @atlas_pagename , 
            concatenator:='$%*<>^~@')'''
            classfication_var = '''aggregate('Notices_Data','concatenate',to_string("classf"), "lpm_no" = @atlas_pagename,concatenator:='$%*<>^~@')'''
            lpm_var_r = '''array_to_string(aggregate('Notices_Data','array_agg',to_string("lpm_no"), "lpm_no" = @atlas_pagename,concatenator:=','))'''

            atlas_coverlayer = 'Notices_Data'

        # Set ATLASPG variable
        alg_params = {
            'NAME': 'atlaspgname',
            'VALUE': atlas_pg_var
        }
        outputs['SETATLASPGVARIABLE'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Set lpm_variable variable
        alg_params = {
            'NAME': 'lpm_variable',
            'VALUE': lpm_var
        }
        outputs['Setlpm_variable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        alg_params = {
            'NAME': 'lpm_variable_r',
            'VALUE': lpm_var_r
        }
        outputs['Setlpm_variable_r'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
            # Set synos variable
        alg_params = {
            'NAME': 'synosvariable',
            'VALUE': sy_no_var
        }
        outputs['Setsynosvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
        # Set old_ac variable
        alg_params = {
            'NAME': 'old_acvariable',
            'VALUE': old_ac_var
        }
        outputs['Setold_acvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Set old_hectvariable
        alg_params = {
            'NAME': 'old_hectvariable',
            'VALUE': old_hect_var
        }
        outputs['setold_hectvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Set new_ac variable
        alg_params = {
            'NAME': 'new_acvariable',
            'VALUE': new_ac_var
        }
        outputs['Setnew_acvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

            # Set new_hectvariable
        alg_params = {
            'NAME': 'new_hectvariable',
            'VALUE': new_hect_var
        }
        outputs['setnew_hectvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Set remarksvariable
        alg_params = {
            'NAME': 'remarksvariable',
            'VALUE': remarks_var
        }
        outputs['setremarksvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

            # Set classification variable
        alg_params = {
            'NAME': 'classfication',
            'VALUE': classfication_var
        }
        outputs['Setclasvariable'] = processing.run(
            'native:setprojectvariable', alg_params, context=context,  is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Save log to file
        alg_params = {
            'OUTPUT': project_folder + '/gv_notice.html',
            'USE_HTML': True,

        }
        outputs['SaveLogToFile'] = processing.run(
            'native:savelog', alg_params, context=context, is_child_algorithm=True)

        if feedback.isCanceled():
            return {}

        notice_layer = QgsVectorLayer(
            refactorFields['OUTPUT'], 'Notices_Data', 'ogr')
        project.addMapLayer(notice_layer, True)

        feedback.pushWarning(
            '\n Hey there! Are you ready to celebrate? 🤩🤩🎉 You are just a step away of adding beautiful templates.')
        
        QgsProject.instance().write()

        return results

    def name(self):
        return 'gv_notice'

    def displayName(self):
        return 'Ground Validation Notice'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Gv_notice()
