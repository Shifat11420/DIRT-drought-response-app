#from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from droughtApp.serializers import testmodelSerializer, cropInfoSerializer, cropPeriodSerializer, growthStageSerializer, soilConditionSerializer, soilMoistureSerializer, soilDrainageGroupSerializer, unitConversionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import testdatamodel, cropInfo, cropPeriod, growthStage, soilMoisture, soilCondition, soilDrainageGroup, unitConversion
# drought calculator imports
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from droughtApp.functions import *
from droughtApp.functionAPI import *
# AERISweatherAPI
import requests
import json
from jsonpath_ng import jsonpath, parse





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

        # plantDate = "01/15/2023"
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
        ## For planting day
        print("\n\n")
        print("inputs[plantDate] = ", inputs["plantDate"])
        plantingDate = datetime.strptime(inputs["plantDate"], "%m/%d/%Y")
        print("plantingDate = ", plantingDate)
           
        ## API request 
        rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(plantingDate)
        #print("first---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)
        #########################################################


        #Calculations
        ##____________________CORP INFO____________________
        crop_info = cropInfo.objects.all()
        print("crop_info : \n", crop_info)
        cropInfoSerializerClass = cropInfoSerializer
        
        queryCropInfo = crop_info.filter(crops=inputs["cropType"]).values()  
        
        for q in queryCropInfo:
            lengthOfGrowingPeriodQUERY = q['lengthOfGrowingPeriodDays']
            maxRootDepthQUERY = q['maxRootDepthInches']
            maxAlllowableDeplitionQUERY = q['maxAlllowableDeplitionPercentage']
            columnForKcQUERY = q['columnForKc']
            columnForDAPQUERY = q['columnForDAP']
            dAPforMaxRootDepthQUERY = q['dAPforMaxRootDepth']

        # print("for crops _",inputs["cropType"],"_ \n","length Of Growing Period Days = ",lengthOfGrowingPeriodQUERY,"\n", "maxRootDepthQUERY=", maxRootDepthQUERY,"\n", 
        # "maxAlllowableDeplitionQUERY =", maxAlllowableDeplitionQUERY,"\n", "columnForKcQUERY =", columnForKcQUERY ,"\n", "columnForDAPQUERY= ", columnForDAPQUERY,"\n",
        # "dAPforMaxRootDepthQUERY =",dAPforMaxRootDepthQUERY )
        
        ##
              
        ##____________________CORP PERIOD____________________
        crop_period = cropPeriod.objects.all()
        print("crop_period : \n", crop_period)
        cropPeriodSerializerClass = cropPeriodSerializer

        ##
        ##____________________GROWTH STAGE____________________
        growth_stage = growthStage.objects.all()
        print("growth_stage : \n", growth_stage)
        growthStageSerializerClass = growthStageSerializer

        ##
        ##____________________SOIL CONDITION____________________
        soil_condition = soilCondition.objects.all()
        print("soil_condition : \n", soil_condition)
        soilConditionSerializerClass = soilConditionSerializer

        soilConditionInfo = soil_condition.filter(soilTexture=inputs["soilType"]).values()  
        for q in soilConditionInfo:
            averagePlantAvailableWaterInFtQUERY = q['averagePlantAvailableWaterInFt']
            averagePlantAvailableWaterInInQUERY = q['averagePlantAvailableWaterInIn']
            permanentWiltingPointInInQUERY = q['permanentWiltingPointInIn']

        # print("for soil type _",inputs["soilType"],"_ \n",
        # "averagePlantAvailableWaterInFt = ",averagePlantAvailableWaterInFtQUERY,"\n",
        # "averagePlantAvailableWaterInInQUERY =", averagePlantAvailableWaterInInQUERY ,"\n", 
        # "permanentWiltingPointInInQUERY = ", permanentWiltingPointInInQUERY)
        ##

        ##____________________SOIL DRAINAGE GROUP____________________
        soil_drainage_group  = soilDrainageGroup.objects.all()
        print("soil_drainage_group  : \n", soil_drainage_group )
        soilDrainageGroupSerializerClass = soilDrainageGroupSerializer

        soilDrainageGroupInfo = soil_drainage_group.filter(descriptionForCN=inputs["plantCond"]).values()  
        print("soilDrainageGroupInfo======", soilDrainageGroupInfo)
        for q in soilDrainageGroupInfo:
            aQUERY = q['a']
            bQUERY = q['b']
            cQUERY = q['c']
            dQUERY = q['d']   
        
        if inputs["hydroSoilGrp"]=="A":            
            hydroSoilvalueQUERY =aQUERY  
        if inputs["hydroSoilGrp"]=="B":
            hydroSoilvalueQUERY =bQUERY  
        if inputs["hydroSoilGrp"]=="C":
            hydroSoilvalueQUERY =cQUERY  
        if inputs["hydroSoilGrp"]=="D":
            hydroSoilvalueQUERY =dQUERY     
          
        ##____________________SOIL MOISTURE____________________
        soil_moisture  = soilMoisture.objects.all()
        print("soil_moisture  : \n", soil_moisture )
        soilMoistureSerializerClass = soilMoistureSerializer

        soilMoistureInfo = soil_moisture.filter(initialConditions=inputs["initMoistCond"]).values()
        for q in soilMoistureInfo:
            ratioQUERY = q['ratio']
          
        
        ##____________________UNIT CONVERSION____________________
        unit_conversion  = unitConversion.objects.all()
        print("unit_conversion  : \n", unit_conversion )
        unitConversionSerializerClass = unitConversionSerializer



        planting_date = datetime.strptime(inputs["plantDate"], "%m/%d/%Y")
        # print("inputs[plantDate] = ", inputs["plantDate"])
        # print("type inputs[plantDate] = ", type(inputs["plantDate"]))
        # print("planting_date = ", planting_date)
        if inputs["seasonLength"] == "":
            inputs["seasonLength"] = lengthOfGrowingPeriodQUERY
               
      
        date_range = [(planting_date + timedelta(days=i)) for i in range(inputs["seasonLength"])]         
        days_after_planting = [i for i in range(0,inputs["seasonLength"])]      
        #plant_growth_stage = []  


        if inputs["maxRootDepth"] == "":
            max_root_depth = maxRootDepthQUERY
        dap = dAPforMaxRootDepthQUERY

        root_depth = []
        for no_days in days_after_planting:
            if no_days == 0:
                root_depth.append(1.0)
            elif no_days<dap:
                root_depth.append(round((root_depth[no_days-1]+((max_root_depth-1)/dap)),2))
            else:
                root_depth.append(max_root_depth)

        if inputs["permWiltPoint"] == "":
            inputs["permWiltPoint"] = permanentWiltingPointInInQUERY
            print("inputs[permWiltPoint]",inputs["permWiltPoint"])

        if inputs["fieldCap"] == "":
            inputs["fieldCap"]  = inputs["permWiltPoint"] + averagePlantAvailableWaterInInQUERY
            print("inputs[fieldCap]",inputs["fieldCap"])
            
        field_capacity = [round(i*inputs["fieldCap"] ,2) for i in root_depth]    
        perm_wilt_point = [round(i*inputs["permWiltPoint"],2) for i in root_depth]    

        if inputs["maxAllowDepl"] == "":
            inputs["maxAllowDepl"] = maxAlllowableDeplitionQUERY
        refill_point = [round(i-(inputs["maxAllowDepl"]/100)*(i-j),2) for i,j in zip(field_capacity,perm_wilt_point)]

        #
        if inputs["cropType"]=="Corn":
            kc = "kcforCorn"
            dap = "dAPforCorn"
        if inputs["cropType"]=="Soybean":
            kc = "kcforSoybean"
            dap = "dAPforSoybean"
        if inputs["cropType"]=="Cotton":
            kc = "kcforCotton"
            dap = "dAPforCotton"
        if inputs["cropType"]=="Grain Sorghum":
            kc = "kcforGrainSorghum"
            dap = "dAPforSorghum"
        if inputs["cropType"]=="Sugarcane":
            kc = "kcforSugarcane"
            dap = "dAPforSugarcane"    
        #

        for item in daps:
            if daps[item]=="":
                daps[item] = list(cropPeriod.objects.all().filter(period__icontains=item).values(dap))[0][dap]
        print("daps----",daps)

        for item in cropCoeff:
            if cropCoeff[item]=="":
                cropCoeff[item] = float(list(cropPeriod.objects.all().filter(period__icontains=item).values(dap))[0][kc])
        print("cropcoeff----", cropCoeff)    

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

        storage = (1000/hydroSoilvalueQUERY) -10
        print("inputs[plantCond] = ", inputs["plantCond"], "inputs[hydroSoilGrp] = ", inputs["hydroSoilGrp"], "storage =", storage)
        
        ratio = ratioQUERY
        print("ratio =", ratio)
        



        ####################################################################
        #Run the calculation
        SWLs = []               #append starting water level
        EWLs = []               #append ending water level
        DPs = []                #append deep percolation
        SRs = []                #append surface runoff
        VWCs = []               #append volumetric water content
        effIrrig = []           #append effective irrigation
        irrigEffic = []         #append irrigation efficiency
        #######
        #at planting date, day = 0

        day = 0

        rain = rainfall_totalIN            #dictRainfall['rainDay0']         #0.01 #API
        print("Rain on planting day = ", rain)


        #julian day
        #J0 = int(format(planting_date, '%j'))
        tt = planting_date.timetuple()
        J0 = tt.tm_yday
        print("J0 = ", J0)
        
        #all other values will come from API
        #ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J0)

        ET0 = penman_monteith(31.177, 21.6, maxTempF, minTempF, maxHumidity, minHumidity, solradWM2, windSpeedMPH,J0)
        #penman_monteith(station_lat, station_z, Tmax_F,Tmin_F,Rhmax,Rhmin,avg_RS,wind_speed,J,wind_z=10,Gsc=0.0820,alpha=0.23,G=0):

        #if farmer provides irrigation value for a day
        grossIrrigation = 0                #farmer override
        grossIrrigUnit = "Acre-inch"       #dropdown if farmer provides a value in grossIrrigation
        
        unitConversionInfo = unit_conversion.filter(flowMeterReadings=grossIrrigUnit).values()
        for q in unitConversionInfo:
            conversionQUERY = q['conversion']
        grossIrrigFactor =  conversionQUERY   
        print("grossIrrigFactor = ",grossIrrigFactor)


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

        
        ## For next day to the planting day
        print("\n\n")
        NextDayDate = plantingDate+ timedelta(days=1)  
        #NextDay_Date = str(datetime.strftime(NextDay_Date, "%m/%d/%Y"))
        print("NextDay Date : ", NextDayDate)

        ## API request 
        rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(NextDayDate)
        #print("second---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)
        ####################################################################

        #increase day incrementally
        day= 1
        rain = rainfall_totalIN        #API
        print("Rain on day 1 = ", rain)

        #ET
        J = J0+day
        #all other values will come from API
        ET0 = penman_monteith(31.177, 21.6, maxTempF, minTempF, maxHumidity, minHumidity, solradWM2, windSpeedMPH,J)
        # ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J)
        print("ET0 : ", ET0)


        #if farmer provides irrigation value for a day
        grossIrrigation = 0              #farmer override
        grossIrrigUnit = "Acre-inch"     #dropdown if farmer provides a value in grossIrrigation
        
       
        unitConversionInfo = unit_conversion.filter(flowMeterReadings=grossIrrigUnit).values()
        for q in unitConversionInfo:
            conversionQUERY = q['conversion']
        grossIrrigFactor =  conversionQUERY   
        print("grossIrrigFactor = ",grossIrrigFactor)


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
            irrigation_eff = "nan"     #np.nan
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
        return Response({'results': results})