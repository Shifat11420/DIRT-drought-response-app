#from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from droughtApp.serializers import testmodelSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import testdatamodel 
# drought calculator imports
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from droughtApp.functions import *
#

class testmodelViewSet(viewsets.ModelViewSet): 
    queryset = testdatamodel.objects.all().order_by('id') 
    serializer_class = testmodelSerializer   

# drought calculator 
####################################################################
class CalculateDroughtAPIView(APIView):
    def get(self, request, format=None):    
        # #Get the User inputs:
        # cropType = "Cotton"
        # soilType = "Sandy loam"
        # initMoistCond = "Really Wet"
        # hydroSoilGrp = "D"
        # plantCond = "Poor Drainage"

        # plantDate = "5/11/16"
        # fieldSize = 0.26018

        # #user override (default values are suggested)
        # seasonLength = 162
        # fieldCap = 0.46
        # permWiltPoint = 0.40
        # maxAllowDepl = ""
        # maxRootDepth = ""
        
        inputs = request.data 

        daps = {"Early":"", "Development":"","Mid":"",
                    "Late":"","Last Irrig. Event":""}
        cropCoeff = {"Early":0.34257447, "Mid":1.09349127,
                    "Last Irrig. Event": 0.89713052}


        ####################################################################

        ####################################################################
        #Calculations
        path = r"F:/drought-django-rest-api/drought-response/droughtProject/droughtApp/tables"  #path to the tables
        crop_info = pd.read_csv(path+"/crop_info.csv",index_col='Crops')
        crop_period = pd.read_csv(path+"/crop_period.csv",index_col='Period')
        growth_stage = pd.read_csv(path+"/growth_stage.csv",index_col='Crop')
        soil_condition = pd.read_csv(path+"/soil condition.csv",index_col='Soil Texture')
        soil_drainage_group = pd.read_csv(path+"/soil_drainage_group.csv",index_col='Description for CN')
        soil_moisture = pd.read_csv(path+"/soil_moisture.csv",index_col='Initial Conditions')
        unit_conversion = pd.read_csv(path+"/Unit_conversion.csv",index_col='Flow meter readings')

        planting_date = datetime.strptime(inputs["plantDate"], "%m/%d/%y")
        if inputs["seasonLength"] == "":
            inputs["seasonLength"] = crop_info.loc[inputs["cropType"],"Length of growing period (days)"]

        date_range = [(planting_date + timedelta(days=i)) for i in range(inputs["seasonLength"])]         
        days_after_planting = [i for i in range(0,inputs["seasonLength"])]      
        #plant_growth_stage = []  


        if inputs["maxRootDepth"] == "":
            max_root_depth = crop_info.loc[inputs["cropType"],"Maximum Root Depth (in)"]
        dap = crop_info.loc[inputs["cropType"],"DAP for Max Root Depth"]

        root_depth = []
        for no_days in days_after_planting:
            if no_days == 0:
                root_depth.append(1.0)
            elif no_days<dap:
                root_depth.append(round((root_depth[no_days-1]+((max_root_depth-1)/dap)),2))
            else:
                root_depth.append(max_root_depth)

        if inputs["permWiltPoint"] == "":
            inputs["permWiltPoint"] = soil_condition.loc[inputs["soilType"],"Permanent Wilting Point (in/in)"]

        if inputs["fieldCap"] == "":
            inputs["fieldCap"]  =inputs["permWiltPoint"] + soil_condition.loc[inputs["soilType"],"Average Plant Available Water  (in/in)"]
            
        field_capacity = [round(i*inputs["fieldCap"] ,2) for i in root_depth]    
        perm_wilt_point = [round(i*inputs["permWiltPoint"],2) for i in root_depth]    

        if inputs["maxAllowDepl"] == "":
            inputs["maxAllowDepl"] = crop_info.loc[inputs["cropType"],"Maximum Allowable Depletion (%)"]
        refill_point = [round(i-(inputs["maxAllowDepl"]/100)*(i-j),2) for i,j in zip(field_capacity,perm_wilt_point)]

        col_Kc = crop_info.loc[inputs["cropType"],"Column for Kc"]
        col_dap = crop_info.loc[inputs["cropType"],"Column for DAP"]

        for item in daps:
            if daps[item]=="":
                daps[item] = crop_period.loc[item,crop_period.columns[col_dap-2]]

        for item in cropCoeff:
            if cropCoeff[item]=="":
                cropCoeff[item] = float(crop_period.loc[item,crop_period.columns[col_Kc-2]])

        dev_slope = (cropCoeff['Mid'] - cropCoeff['Early'])/(daps['Mid'] - daps['Development'])
        late_slope = (cropCoeff['Last Irrig. Event'] - cropCoeff['Mid'])/(daps['Last Irrig. Event'] - daps['Late'])

        Kc = []
        for coeff in days_after_planting:
            if coeff< daps["Development"]:
                Kc.append(cropCoeff['Early'])
            elif coeff< daps["Mid"]:
                Kc.append(cropCoeff['Early'] + dev_slope * (coeff-daps["Development"]))
            elif coeff< daps["Late"]:
                Kc.append(cropCoeff['Mid'])
            elif coeff< daps["Last Irrig. Event"]:
                Kc.append(cropCoeff['Mid'] + late_slope * (coeff-daps["Late"]))
            else:
                Kc.append(cropCoeff['Last Irrig. Event'])

        storage = (1000/(soil_drainage_group.loc[inputs["plantCond"],inputs["hydroSoilGrp"]])) -10
        ratio = soil_moisture.loc[inputs["initMoistCond"],"Ratio"]
        ####################################################################
        #Run the calculation
        SWLs = []    #append starting water level
        EWLs = []    #append ending water level
        DPs = []     #append deep percolation
        SRs = []     #append surface runoff
        VWCs = []    #append volumetric water content
        effIrrig = []   #append effective irrigation
        irrigEffic = []      #append irrigation efficiency
        #######
        #at planting date, day = 0

        day = 0

        rain = 0.01 #API


        #julian day
        #J0 = int(format(planting_date, '%j'))
        tt = planting_date.timetuple()
        J0 = tt.tm_yday
        print("J0 = ", J0)
        #all other values will come from API
        ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J0)

        #if farmer provides irrigation value for a day
        grossIrrigation = 0    #farmer override
        grossIrrigUnit = "Acre-inch"  #dropdown if farmer provides a value in grossIrrigation
        grossIrrigFactor = unit_conversion.loc[grossIrrigUnit,"Conversion"]
        gross_irrig_inch = grossIrrigation * grossIrrigFactor

        ##############
        swl,crop_et,eff_rainfall, sr, dp,ewl,vwc = plantingDay(ET0,rain,field_capacity[day],ratio,perm_wilt_point[day],
                                                                        refill_point[day],Kc[day],storage,root_depth[day],gross_irrig_inch)

        if (((swl-crop_et+eff_rainfall<refill_point[day] and day>=daps['Development'] and day<daps['Last Irrig. Event']) or
            (day>=daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[day]) or
            (day<daps['Development'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[day]) or
            (field_capacity[day]-swl>3 and day>=daps['Development'] and day<daps['Last Irrig. Event'])) and(field_capacity[day]-swl>1)):   
            eff_irrigation = field_capacity[day]- swl
        else:
            eff_irrigation = 0

        if gross_irrig_inch>0:
            irrigation_eff =  eff_irrigation/gross_irrig_inch
        else:
            irrigation_eff = "nan"#np.nan
        ##############
        SWLs.append(swl)
        EWLs.append(ewl)
        DPs.append(dp)
        SRs.append(sr)
        VWCs.append(vwc)
        effIrrig.append(eff_irrigation)
        irrigEffic.append(irrigation_eff)

        #######
        #increase day incrementally
        day= 1
        rain = 0        #API

        #ET
        J = J0+day
        #all other values will come from API
        ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J)
        print("ET0 : ", ET0)


        #if farmer provides irrigation value for a day
        grossIrrigation = 0    #farmer override
        grossIrrigUnit = "Acre-inch"  #dropdown if farmer provides a value in grossIrrigation
        grossIrrigFactor = unit_conversion.loc[grossIrrigUnit,"Conversion"]
        gross_irrig_inch = grossIrrigation * grossIrrigFactor

        #########
        swl,crop_et,eff_rainfall, sr, dp,ewl,vwc = growthDay(ET0,rain,EWLs[day-1],root_depth[day-1],root_depth[day],field_capacity[day],inputs["fieldCap"] ,
                                                                    refill_point[day],perm_wilt_point[day],Kc[day],storage,gross_irrig_inch=0) 
                                                
        if (((swl-crop_et+eff_rainfall<refill_point[day] and day>=daps['Development'] and day<daps['Last Irrig. Event']) or
            (day>=daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[day]) or
            (day<daps['Development'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[day]) or
            (field_capacity[day]-swl>3 and day>=daps['Development'] and day<daps['Last Irrig. Event'])) and(field_capacity[day]-swl>1)):   
            eff_irrigation = field_capacity[day]- swl
        else:
            eff_irrigation = 0

        if gross_irrig_inch>0:
            irrigation_eff =  eff_irrigation/gross_irrig_inch
        else:
            irrigation_eff = "nan"#np.nan
        ###############  

        SWLs.append(swl)
        EWLs.append(ewl)
        DPs.append(dp)
        SRs.append(sr)
        VWCs.append(vwc)
        effIrrig.append(eff_irrigation)
        irrigEffic.append(irrigation_eff)



        # #-----------------------FOR LOOP-------------------------------------------------------------------------------------
        # #######
        # #increase day incrementally
        # day= 5
        # rain = 0        #API

        # for dayI in range(1,day+1):

        #     #ET
        #     J = J0+dayI
        #     #all other values will come from API
        #     ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J)
        #     print("ET0 : ", ET0)


        #     #if farmer provides irrigation value for a day
        #     grossIrrigation = 0    #farmer override
        #     grossIrrigUnit = "Acre-inch"  #dropdown if farmer provides a value in grossIrrigation
        #     grossIrrigFactor = unit_conversion.loc[grossIrrigUnit,"Conversion"]
        #     gross_irrig_inch = grossIrrigation * grossIrrigFactor

        #     #########
        #     swl,crop_et,eff_rainfall, sr, dp,ewl,vwc = growthDay(ET0,rain,EWLs[dayI-1],root_depth[dayI-1],root_depth[dayI],field_capacity[dayI],fieldCap,
        #                                                                 refill_point[dayI],perm_wilt_point[dayI],Kc[dayI],storage,gross_irrig_inch=0) 
                                                    
        #     if (((swl-crop_et+eff_rainfall<refill_point[dayI] and dayI>=daps['Development'] and dayI<daps['Last Irrig. Event']) or
        #         (dayI>=daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[dayI]) or
        #         (dayI<daps['Development'] and swl-crop_et+eff_rainfall<1.25*perm_wilt_point[dayI]) or
        #         (field_capacity[dayI]-swl>3 and dayI>=daps['Development'] and dayI<daps['Last Irrig. Event'])) and(field_capacity[dayI]-swl>1)):   
        #         eff_irrigation = field_capacity[dayI]- swl
        #     else:
        #         eff_irrigation = 0

        #     if gross_irrig_inch>0:
        #         irrigation_eff =  eff_irrigation/gross_irrig_inch
        #     else:
        #         irrigation_eff = np.nan
        #     ###############  

        #     SWLs.append(swl)
        #     EWLs.append(ewl)
        #     DPs.append(dp)
        #     SRs.append(sr)
        #     VWCs.append(vwc)
        #     effIrrig.append(eff_irrigation)
        #     irrigEffic.append(irrigation_eff)


        print("SWLs : ", SWLs)
        print("EWLs : ", EWLs)
        print("DPs : ", DPs)
        print("SRs : ", SRs)
        print("VWCs : ", VWCs)
        print("effIrrig : ", effIrrig)
        print("irrigEffic : ", irrigEffic)

        results = {'SWLs': SWLs, 'EWLs': EWLs, 'DPs': DPs, 'SRs': SRs, 'VWCs': VWCs, 'effIrrig': effIrrig, 'irrigEffic': irrigEffic}
        return Response({'results': results})#, {'EWLs': EWLs}, {'DPs': DPs}, {'SRs': SRs}, {'VWCs': VWCs}, {'effIrrig': effIrrig}, {'irrigEffic': irrigEffic})