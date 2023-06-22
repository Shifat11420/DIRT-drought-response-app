from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse

from django.shortcuts import get_object_or_404

# drought calculator imports
from datetime import datetime, timedelta, date
from .functionAPI import *
from .functions import *


class CropTypes(viewsets.ReadOnlyModelViewSet):
    queryset = cropType.objects.all()
    serializer_class = cropTypesSerializer


class cropPeriodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = cropPeriod.objects.all()
    serializer_class = cropPeriodSerializer


class drainageTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = drainageType.objects.all()
    serializer_class = drainageTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['HydrologicGroupId']


class soilMoistureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = soilMoisture.objects.all()
    serializer_class = soilMoistureSerializer


class SoilTypes(viewsets.ReadOnlyModelViewSet):
    queryset = soilType.objects.all().order_by('Name')
    serializer_class = soilTypeSerializer


class hydrologicGroups(viewsets.ReadOnlyModelViewSet):
    queryset = hydrologicGroup.objects.all()
    serializer_class = hydrologicGroupSerializer


class userInfo(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = userSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['AuthenticationId']


class userfield(viewsets.ModelViewSet):
    queryset = field.objects.all()
    serializer_class = fieldSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['OwnerId']

    @action(detail=True, methods=['delete'])
    def deleteresults(self, request, pk=None):
        currentfield = self.get_object()
        deleteforField = results.objects.filter(FieldId=currentfield)
        deleteforField.delete()
        return HttpResponse(status=204)


class irrigationActivity(viewsets.ModelViewSet):
    queryset = irrigation.objects.all()
    serializer_class = irrigationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['FieldId']


class resultViewSet(viewsets.ModelViewSet):
    queryset = results.objects.all()
    serializer_class = resultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['FieldId']

    @action(detail=True, methods=['delete'])
    def deleteforfield(self, request, pk=None):
        inputs = request.data
        print(self, request)
        deleteforField = results.objects.filter(FieldId=inputs["fieldId"])
        deleteforField.delete()
        return HttpResponse(status=204)


# drought calculator
class CalculateDroughtAPIView(APIView):
    def get(self, request, format=None):
        SWLs = []                # append starting water level
        EWLs = []                # append ending water level
        DPs = []                 # append deep percolation
        SRs = []                 # append surface runoff
        VWCs = []                # append volumetric water content
        effIrrig = []            # append effective irrigation
        irrigEffic = []          # append irrigation efficiency
        forDate = []
        FC = []
        MADg = []
        waterDeficit = []
        pwp = []
        grossIrrg = []
        rainFall = []
        ETOs = []
        ETCs = []


        inputs = request.data
        fieldsearch = inputs["fieldId"]
        currentField = field.objects.get(id = fieldsearch)
        print("infofromfieldId : ", currentField)


        lat = float(currentField.Latitude)
        long = float(currentField.Longitude)
        elevation = currentField.Elevation

        daps = {"Early": "", "Development": "", "Mid": "",
                "Late": "", "Last Irrig. Event": ""}
        cropCoeff = {"Early": 0.34257447, "Mid": 1.09349127,
                     "Last Irrig. Event": 0.89713052}

        # Table Queries___________________________

        # ____________________CORP INFO____________________
        cropTypeSerializerClass = cropTypesSerializer
        queryCropType =  cropType.objects.get(id=currentField.CropTypeId.id)
        print("queryCropType = ", queryCropType)

        lengthOfGrowingPeriodQUERY = queryCropType.GrowingPeriodDays
        maxRootDepthQUERY = queryCropType.MaxRootDepth
        maxAllowableDeplitionQUERY = queryCropType.MaxAllowableDepletion
        dAPforMaxRootDepthQUERY = queryCropType.MaxRootDepthDaysAfterPlanting
        
        # ____________________CORP PERIOD___________________
        cropPeriodSerializerClass = cropPeriodSerializer

        # ____________________SOIL TYPE____________________
        soilTypeSerializerClass = soilTypeSerializer      
        querySoilType =  soilType.objects.get(id=currentField.SoilTypeId.id)
        print("querySoilType = ", querySoilType)

        averagePlantAvailableWaterQUERY = querySoilType.AveragePlantAvailableWater
        permanentWiltingPointQUERY = querySoilType.PermanentWiltingPoint


        # ____________________SOIL DRAINAGE GROUP and HYDROLOGIC GROUP____________________
        drainageTypeSerializerClass = drainageTypeSerializer
        soildrainageType = drainageType.objects.get(id= currentField.DrainageTypeId.id , HydrologicGroupId = currentField.HydrologicGroupId)
        soildrainageTypeValue = soildrainageType.DrainageValue
        print("soildrainageTypeVaule = ", soildrainageTypeValue)

        # ____________________SOIL MOISTURE____________________
        soilMoistureSerializerClass = soilMoistureSerializer
        soilMoistureInfo = soilMoisture.objects.get(
            id=currentField.SoilMoistureId.id)
        
        ratio = soilMoistureInfo.InitialSoilMoisturePercent
        print("ratio = ", ratio)

        # ____________________UNIT CONVERSION____________________
        unit_conversion = unitConversion.objects.all()
        unitConversionSerializerClass = unitConversionSerializer


        #  Calculations _____________________________

        #__________________________________________
        # # If fieldname does not exist and not calculated previously
        print("\n\n")        
        prevresultcount = results.objects.filter(FieldId=inputs["fieldId"]).count()
        print("prevresult count = ", prevresultcount)

        if prevresultcount>0:
            prevresultLast = results.objects.filter(FieldId=inputs["fieldId"]).last()
            prevresultLastDate = prevresultLast.Date
            print("prevresultLast = ", prevresultLast)
            print("prevresultLastDate = ", prevresultLastDate)
            if prevresultLastDate == date.today():
                print("Calculations till today already exists")
                

        # For planting day
        print("\n\n")
        plantingDate = currentField.PlantDate
        print("plantingDate = ", plantingDate)

        # julian day
        tt = plantingDate.timetuple()
        J0 = tt.tm_yday
        print("J0 = ", J0)

        # API request_____ from AERISweatherAPI
        rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(
            plantingDate, lat, long)
        # print("first---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)


        planting_date = plantingDate
        print("planting_date = ", planting_date)

        if currentField.GrowingPeriodDays:  
            seasonLength = currentField.GrowingPeriodDays
        else:
            seasonLength = lengthOfGrowingPeriodQUERY

        date_range = [(planting_date + timedelta(days=i))
                    for i in range(seasonLength)]
        days_after_planting = [i for i in range(0, seasonLength)]


        max_root_depth = maxRootDepthQUERY
        dap = dAPforMaxRootDepthQUERY

        root_depth = []
        for no_days in days_after_planting:
            if no_days == 0:
                root_depth.append(1.0)
            elif no_days < dap:
                root_depth.append(
                    round((root_depth[no_days-1]+((max_root_depth-1)/dap)), 2))
            else:
                root_depth.append(max_root_depth)

        if currentField.PermanentWiltingPoint:
            permWiltPoint = currentField.PermanentWiltingPoint
        else:    
            permWiltPoint = permanentWiltingPointQUERY
            #print("permWiltPoint = ", permWiltPoint)


        if currentField.FieldCapacity:
            fieldCap = currentField.FieldCapacity
        else:    
            fieldCap = permWiltPoint + averagePlantAvailableWaterQUERY

        field_capacity = [round(i*fieldCap, 2) for i in root_depth]

        perm_wilt_point = [round(i*permWiltPoint, 2)
                        for i in root_depth]
        # print("field_capacity = ", field_capacity)
        # print("perm_wilt_point = ", perm_wilt_point)
            
        maxAllowDepl = maxAllowableDeplitionQUERY    
        refill_point = [round(i-(maxAllowDepl/100)*(i-j), 2)
                        for i, j in zip(field_capacity, perm_wilt_point)]

        cropPeriodForId = cropPeriod.objects.filter(
            CropTypeId=queryCropType.id).all()    
        print("cropPeriodForId = ", cropPeriodForId)

        for item in daps:
            if daps[item] == "":
                daps[item] = float(cropPeriodForId.filter(
                    Name=item).values()[0]['DaysAfterPlanting'])
        print("daps = ", daps)

        for item in cropCoeff:
            if cropCoeff[item] == "":
                kcValue = cropPeriodForId.filter(
                    Name=item).values()[0]['CropCoefficient']
                cropCoeff[item] = float(kcValue) if not (
                    kcValue == "Linear") else kcValue
        print("cropcoeff = ", cropCoeff)

        dev_slope = (cropCoeff['Mid'] - cropCoeff['Early']
                    )/(daps['Mid'] - daps['Development'])
        late_slope = (cropCoeff['Last Irrig. Event'] - cropCoeff['Mid']
                    )/(daps['Last Irrig. Event'] - daps['Late'])

        print("dev_slope = ", dev_slope, " ", "late_slope = ", late_slope)

        Kc = []
        for coeff in days_after_planting:
            if coeff < daps["Development"]:
                Kc.append(cropCoeff['Early'])
            elif coeff < daps["Mid"]:
                Kc.append(cropCoeff['Early'] + dev_slope *
                        (coeff-daps["Development"]))
            elif coeff < daps["Late"]:
                Kc.append(cropCoeff['Mid'])
            elif coeff < daps["Last Irrig. Event"]:
                Kc.append(cropCoeff['Mid'] + late_slope * (coeff-daps["Late"]))
            else:
                Kc.append(cropCoeff['Last Irrig. Event'])

        storage = (1000/soildrainageTypeValue) - 10
        print("storage =", storage)

        if prevresultcount>0:
            # retrieve previously calculated result from database_____________
            res = results.objects.filter(FieldId=inputs["fieldId"], Date=plantingDate).last()
            SWLs.append(res.WaterLevelStart)
            EWLs.append(res.WaterLevelEnd)
            DPs.append(res.DeepPercolation )
            SRs.append(res.SurfaceRunoff)
            VWCs.append(res.VolumetricWaterContent)
            effIrrig.append(res.EffectiveIrrigation)
            irrigEffic.append(res.IrrigationEfficiency)
            forDate.append(res.Date.strftime('%m/%d/%Y'))
            FC.append(res.FieldCapacity)
            MADg.append(res.MaximumAvailableDepletion)
            waterDeficit.append(res.WaterDeficit)
            pwp.append(res.PermanentWiltingPoint)
            grossIrrg.append(res.IrrigationActivityAmount)
            rainFall.append(res.RainObservedAmount)
            ETOs.append(res.EvapotranporationValue)
            ETCs.append(res.EvapotranporationCropValue)
        else: 
            # Run the calculation__________________         
            # at planting date, day = 0
            day = 0
            rain = rainfall_totalIN  
            print("Rain on planting day = ", rain)

            # all other values will come from API
            # ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J0)
            ET0 = penman_monteith(lat, elevation, maxTempF, minTempF,
                                maxHumidity, minHumidity, solradWM2, windSpeedMPH, J0)
            # penman_monteith(station_lat, station_z, Tmax_F,Tmin_F,Rhmax,Rhmin,avg_RS,wind_speed,J,wind_z=10,Gsc=0.0820,alpha=0.23,G=0):
            print("ET0 on planting day = ", ET0)

            # if farmer provides irrigation value for a day
            grossIrrigationQuery = irrigation.objects.filter(FieldId = inputs["fieldId"], Date=plantingDate).last()
            grossIrrigation = grossIrrigationQuery.Amount if grossIrrigationQuery else 0      # farmer override
            print("grossIrrigation for ",plantingDate, " = ", grossIrrigation)
            grossIrrigUnit = "Acre-inch"     # dropdown if farmer provides a value in grossIrrigation

            unitConversionInfo = unit_conversion.filter(
                flowMeterReadings=grossIrrigUnit).values()
            for q in unitConversionInfo:
                conversionQUERY = q['conversion']
            grossIrrigFactor = conversionQUERY
            print("grossIrrigFactor = ", grossIrrigFactor)

            gross_irrig_inch = grossIrrigation * grossIrrigFactor
            FC_plantday = field_capacity[day]  
            pwp_plantday = perm_wilt_point[day]
            MADforgraph = (FC_plantday-pwp_plantday)*maxAllowableDeplitionQUERY+pwp_plantday #maxAllowableDeplitionQUERY #* FC_plantday

            ##############
            swl, crop_et, eff_rainfall, sr, dp, ewl, vwc = plantingDay(ET0, rain, field_capacity[day], ratio, perm_wilt_point[day],
                                                                    refill_point[day], Kc[day], storage, root_depth[day], gross_irrig_inch)

            if (((swl-crop_et+eff_rainfall < refill_point[day] and day >= daps['Development'] and day < daps['Last Irrig. Event']) or
                (day >= daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
                (day < daps['Development'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
                    (field_capacity[day]-swl > 3 and day >= daps['Development'] and day < daps['Last Irrig. Event'])) and (field_capacity[day]-swl > 1)):
                eff_irrigation = field_capacity[day] - swl
            else:
                eff_irrigation = 0

            if gross_irrig_inch > 0:
                irrigation_eff = eff_irrigation/gross_irrig_inch
            else:
                irrigation_eff = None  
            ##############
            water_Deficit = 100 * (FC_plantday-ewl)/FC_plantday
            
            plantdayresults = results(Date=plantingDate, WaterLevelStart=swl, WaterLevelEnd=ewl, DeepPercolation=dp, SurfaceRunoff=sr, VolumetricWaterContent=vwc, EffectiveIrrigation=eff_irrigation, IrrigationEfficiency=irrigation_eff,
                                MaximumAvailableDepletion=MADforgraph, FieldCapacity=FC_plantday, PermanentWiltingPoint=pwp_plantday, WaterDeficit=water_Deficit, IrrigationActivityAmount=grossIrrigation, RainObservedAmount=rainfall_totalIN,  
                                FieldId=currentField, EvapotranporationValue=ET0, EvapotranporationCropValue = crop_et)
            plantdayresults.save()

            SWLs.append(swl)
            EWLs.append(ewl)
            DPs.append(dp)
            SRs.append(sr)
            VWCs.append(vwc)
            effIrrig.append(eff_irrigation)
            irrigEffic.append(irrigation_eff)
            forDate.append(plantingDate.strftime('%m/%d/%Y'))
            FC.append(FC_plantday)
            MADg.append(MADforgraph)
            waterDeficit.append(water_Deficit)
            pwp.append(pwp_plantday)
            grossIrrg.append(grossIrrigation)
            rainFall.append(rainfall_totalIN)
            ETOs.append(ET0)
            ETCs.append(crop_et)

        print("---  here code for loop starts  ---")
        print("\n\n")

        # #increase day incrementally
        dateplanted = plantingDate.strftime('%m/%d/%Y')
        print("planting Date = ", dateplanted)

        today = date.today()
        todaydate = today.strftime("%m/%d/%Y")
        print("today's date =", todaydate)

        date_format = "%m/%d/%Y"
        a = datetime.strptime(dateplanted, date_format)
        b = datetime.strptime(todaydate, date_format)

        delta = b - a
        totaldays = delta.days

        print("totaldays = ", totaldays)

        for dayI in range(1, totaldays+1):  # starts the day after planting day

            # For next day to the planting day
            NextDayDate = plantingDate + timedelta(days=dayI)
            print("NextDay Date : ", NextDayDate)

            if prevresultcount>0:
                res = results.objects.filter(FieldId=inputs["fieldId"], Date=NextDayDate).last()
                if res:
                    SWLs.append(res.WaterLevelStart)
                    EWLs.append(res.WaterLevelEnd)
                    DPs.append(res.DeepPercolation )
                    SRs.append(res.SurfaceRunoff)
                    VWCs.append(res.VolumetricWaterContent)
                    effIrrig.append(res.EffectiveIrrigation)
                    irrigEffic.append(res.IrrigationEfficiency)
                    forDate.append(res.Date.strftime('%m/%d/%Y'))
                    FC.append(res.FieldCapacity)
                    MADg.append(res.MaximumAvailableDepletion)
                    waterDeficit.append(res.WaterDeficit)
                    pwp.append(res.PermanentWiltingPoint)
                    grossIrrg.append(res.IrrigationActivityAmount)
                    rainFall.append(res.RainObservedAmount)
                    ETOs.append(res.EvapotranporationValue)
                    ETCs.append(res.EvapotranporationCropValue)
                    continue


            # API request
            rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(
                NextDayDate, lat, long)
            # print("second---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)


            # increase day incrementally
            day = dayI
            rain = rainfall_totalIN  # API
            print("Rain on day ", dayI, " = ", rain)


            # ET
            J = J0+day
            # all other values will come from API
            ET0 = penman_monteith(lat, elevation, maxTempF, minTempF,
                                  maxHumidity, minHumidity, solradWM2, windSpeedMPH, J)
            print("ET0 : ", ET0)

            # if farmer provides irrigation value for a day
            grossIrrigationQuery = irrigation.objects.filter(FieldId = inputs["fieldId"], Date=NextDayDate).last()
            print("grossIrrigation query = ", grossIrrigationQuery)
            grossIrrigation = grossIrrigationQuery.Amount if grossIrrigationQuery else 0      # farmer override
            print("grossIrrigation for", NextDayDate, " = ", grossIrrigation)
            grossIrrigUnit = "Acre-inch"      # dropdown if farmer provides a value in grossIrrigation

            unitConversionInfo = unit_conversion.filter(
                flowMeterReadings=grossIrrigUnit).values()
            for q in unitConversionInfo:
                conversionQUERY = q['conversion']
            grossIrrigFactor = conversionQUERY
            print("grossIrrigFactor = ", grossIrrigFactor)

            gross_irrig_inch = grossIrrigation * grossIrrigFactor
            FC_growthday = field_capacity[day]
            pwp_growthday = perm_wilt_point[day]
            MADforgraph = (FC_growthday-pwp_growthday)*maxAllowableDeplitionQUERY+pwp_growthday #maxAllowableDeplitionQUERY #* FC_growthday

            #########
            swl, crop_et, eff_rainfall, sr, dp, ewl, vwc = growthDay(ET0, rain, EWLs[day-1], root_depth[day-1], root_depth[day], field_capacity[day], fieldCap,
                                                                     refill_point[day], perm_wilt_point[day], Kc[day], storage, gross_irrig_inch)

            if (((swl-crop_et+eff_rainfall < refill_point[day] and day >= daps['Development'] and day < daps['Last Irrig. Event']) or
                (day >= daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
                (day < daps['Development'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
                    (field_capacity[day]-swl > 3 and day >= daps['Development'] and day < daps['Last Irrig. Event'])) and (field_capacity[day]-swl > 1)):
                eff_irrigation = field_capacity[day] - swl
            else:
                eff_irrigation = 0

            if gross_irrig_inch > 0:
                irrigation_eff = eff_irrigation/gross_irrig_inch
            else:
                irrigation_eff = None  # np.nan
            ###############

            water_Deficit = 100 * (FC_growthday-ewl)/FC_growthday

            SWLs.append(swl)
            EWLs.append(ewl)
            DPs.append(dp)
            SRs.append(sr)
            VWCs.append(vwc)
            effIrrig.append(eff_irrigation)
            irrigEffic.append(irrigation_eff)
            forDate.append(NextDayDate.strftime('%m/%d/%Y'))
            FC.append(FC_growthday)
            MADg.append(MADforgraph)
            waterDeficit.append(water_Deficit)
            pwp.append(pwp_growthday)
            grossIrrg.append(grossIrrigation)
            rainFall.append(rainfall_totalIN)
            ETOs.append(ET0)
            ETCs.append(crop_et)

            growingdaysresults = results(Date=NextDayDate, WaterLevelStart=swl, WaterLevelEnd=ewl, DeepPercolation=dp, SurfaceRunoff=sr, VolumetricWaterContent=vwc, EffectiveIrrigation=eff_irrigation, IrrigationEfficiency=irrigation_eff,
                                         MaximumAvailableDepletion=MADforgraph, FieldCapacity=FC_growthday, PermanentWiltingPoint=pwp_growthday, WaterDeficit=water_Deficit, IrrigationActivityAmount=grossIrrigation, RainObservedAmount=rainfall_totalIN,  
                                         FieldId=currentField, EvapotranporationValue=ET0, EvapotranporationCropValue = crop_et)
            growingdaysresults.save()

        print("SWLs : ", SWLs)
        print("EWLs : ", EWLs)
        print("DPs : ", DPs)
        print("SRs : ", SRs)
        print("VWCs : ", VWCs)
        print("effIrrig : ", effIrrig)
        print("irrigEffic : ", irrigEffic)
        print("forDate : ", forDate)
        print("field capacity : ", FC)
        print("MADg : ", MADg)
        print("waterDeficit(%) :", waterDeficit)
        print("pwp : ", pwp)
        print(" gross irrigation : ", grossIrrg)
        print("rain fall in inches : ", rainFall)
        print("EvapotranporationValue : ", ETOs)
        print("EvapotranporationCropValue : ", ETCs)

        resultsDict = {'SWLs': SWLs, 'EWLs': EWLs, 'DPs': DPs, 'SRs': SRs, 'VWCs': VWCs, 'effIrrig': effIrrig, 'irrigEffic': irrigEffic, 'forDate': forDate,
                       "MAD": MADg, "FC": FC, "PWP": pwp, "Deficit(%)": waterDeficit, "irrigation activity": grossIrrg, "rain observed": rainFall, 
                       'EvapotranporationValue': ETOs, 'EvapotranporationCropValue' : ETCs}
        return Response({'results': resultsDict})
