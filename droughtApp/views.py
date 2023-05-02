from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

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


# drought calculator
####################################################################


class CalculateDroughtAPIView(APIView):
    def get(self, request, format=None):
        # Inputs ____________________
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
        lat = inputs["lat"]
        long = inputs["long"]
        elevation = inputs["elevation"]

        currentField = field.objects.get(
            id=inputs["fieldId"])

        daps = {"Early": "", "Development": "", "Mid": "",
                "Late": "", "Last Irrig. Event": ""}
        cropCoeff = {"Early": 0.34257447, "Mid": 1.09349127,
                     "Last Irrig. Event": 0.89713052}

        # _________________________________________
        # For planting day
        print("\n\n")
        print("inputs[plantDate] = ", inputs["plantDate"])
        plantingDate = datetime.strptime(inputs["plantDate"], "%m/%d/%Y")
        print("plantingDate = ", plantingDate)

        # API request_____ from AERISweatherAPI
        rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(
            plantingDate, lat, long)
        # print("first---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)

        # _______________________________________

        # Table Queries___________________________
        # ____________________CORP INFO____________________
        croptype = cropType.objects.all()
        print("croptype : \n", croptype)
        cropTypeSerializerClass = cropTypesSerializer

        queryCropType = croptype.filter(Name=inputs["cropType"]).values()

        for q in queryCropType:
            lengthOfGrowingPeriodQUERY = q['GrowingPeriodDays']
            maxRootDepthQUERY = q['MaxRootDepth']
            maxAllowableDeplitionQUERY = q['MaxAllowableDepletion']
            dAPforMaxRootDepthQUERY = q['MaxRootDepthDaysAfterPlanting']

        print("for crops _", inputs["cropType"], "_ \n", "length Of Growing Period Days = ", lengthOfGrowingPeriodQUERY, "\n", "maxRootDepthQUERY=", maxRootDepthQUERY, "\n",
              "maxAllowableDeplitionQUERY =", maxAllowableDeplitionQUERY, "\n",
              "dAPforMaxRootDepthQUERY =", dAPforMaxRootDepthQUERY)

        # ____________________CORP PERIOD___________________
        crop_period1 = cropPeriod.objects.all()
        print("crop_period1 : \n", crop_period1)
        cropPeriodSerializerClass = cropPeriodSerializer

        # ____________________SOIL TYPE____________________
        soilTypeInfoall = soilType.objects.all()
        print("soil type : \n", soilTypeInfoall)
        soilTypeSerializerClass = soilTypeSerializer

        soilTypeInfo = soilTypeInfoall.filter(
            Name=inputs["soilType"]).values()

        for q in soilTypeInfo:
            averagePlantAvailableWaterQUERY = q['AveragePlantAvailableWater']
            permanentWiltingPointQUERY = q['PermanentWiltingPoint']

        print("for soil type _", inputs["soilType"], "_ \n",
              "averagePlantAvailableWaterQUERY =", averagePlantAvailableWaterQUERY, "\n",
              "permanentWiltingPointQUERY = ", permanentWiltingPointQUERY)

        # ____________________SOIL DRAINAGE GROUP and HYDROLOGIC GROUP____________________

        hydrogrpQUERY = hydrologicGroup.objects.filter(
            Name=inputs["hydroSoilGrp"]).values()[0]['Name']
        print("hydrogrpQUERY = ", hydrogrpQUERY)

        hydrogrpQUERY = hydrologicGroup.objects.filter(
            Name=inputs["hydroSoilGrp"]).values()[0]
        hydrogroupName = hydrogrpQUERY['Name']
        hydrogroupId = hydrogrpQUERY['id']
        print("hydrogroupName = ", hydrogroupName)
        print("hydrogroupId = ", hydrogroupId)

        drainageTypeInfo = drainageType.objects.all()
        print("drainageTypeInfo  : \n", drainageTypeInfo)
        drainageTypeSerializerClass = drainageTypeSerializer

        soildrainageTypeValue = drainageTypeInfo.filter(
            Name=inputs["plantCond"], HydrologicGroupId=hydrogroupId).values()[0]['DrainageValue']
        print("soildrainageTypeVaule======", soildrainageTypeValue)

        # ____________________SOIL MOISTURE____________________
        soil_moisture = soilMoisture.objects.all()
        print("soil_moisture  : \n", soil_moisture)
        soilMoistureSerializerClass = soilMoistureSerializer

        soilMoistureInfo = soil_moisture.filter(
            Name=inputs["initMoistCond"]).values()
        print("soilMoistureInfo = ", soilMoistureInfo)
        for q in soilMoistureInfo:
            ratio = q['InitialSoilMoisturePercent']
        print("ratio = ", ratio)

        # ____________________UNIT CONVERSION____________________
        unit_conversion = unitConversion.objects.all()
        print("unit_conversion  : \n", unit_conversion)
        unitConversionSerializerClass = unitConversionSerializer

        #  Calculations _____________________________
        planting_date = datetime.strptime(inputs["plantDate"], "%m/%d/%Y")
        # print("inputs[plantDate] = ", inputs["plantDate"])
        # print("type inputs[plantDate] = ", type(inputs["plantDate"]))
        # print("planting_date = ", planting_date)
        if inputs["seasonLength"] == "":
            inputs["seasonLength"] = lengthOfGrowingPeriodQUERY

        date_range = [(planting_date + timedelta(days=i))
                      for i in range(inputs["seasonLength"])]
        days_after_planting = [i for i in range(0, inputs["seasonLength"])]

        if inputs["maxRootDepth"] == "":
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

        if inputs["permWiltPoint"] == "":
            inputs["permWiltPoint"] = permanentWiltingPointQUERY
            print("inputs[permWiltPoint]", inputs["permWiltPoint"])

        if inputs["fieldCap"] == "":
            inputs["fieldCap"] = inputs["permWiltPoint"] + \
                averagePlantAvailableWaterQUERY
            print("inputs[fieldCap]", inputs["fieldCap"])

        field_capacity = [round(i*inputs["fieldCap"], 2) for i in root_depth]

        perm_wilt_point = [round(i*inputs["permWiltPoint"], 2)
                           for i in root_depth]

        if inputs["maxAllowDepl"] == "":
            inputs["maxAllowDepl"] = maxAllowableDeplitionQUERY
        refill_point = [round(i-(inputs["maxAllowDepl"]/100)*(i-j), 2)
                        for i, j in zip(field_capacity, perm_wilt_point)]

        # demo is the cropid matched from croptype
        cropIdForType = cropType.objects.filter(
            Name=inputs["cropType"]).values()[0]['id']
        print("cropIdForType = ", cropIdForType)

        # cropPeriodForId is filtered for the cropId from cropPeriod
        cropPeriodForId = cropPeriod.objects.filter(
            CropTypeId=cropIdForType).all()

        print("cropPeriodForId = ", cropPeriodForId)

        for item in daps:
            if daps[item] == "":
                daps[item] = float(cropPeriodForId.filter(
                    Name=item).values()[0]['DaysAfterPlanting'])
        print("daps---", daps)

        for item in cropCoeff:
            if cropCoeff[item] == "":
                kcValue = cropPeriodForId.filter(
                    Name=item).values()[0]['CropCoefficient']
                cropCoeff[item] = float(kcValue) if not (
                    kcValue == "Linear") else kcValue
        print("cropcoeff---", cropCoeff)

        dev_slope = (cropCoeff['Mid'] - cropCoeff['Early']
                     )/(daps['Mid'] - daps['Development'])
        late_slope = (cropCoeff['Last Irrig. Event'] - cropCoeff['Mid']
                      )/(daps['Last Irrig. Event'] - daps['Late'])

        print(" dev_slope = ", dev_slope, " late_slope = ", late_slope)

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
        print("inputs[plantCond] = ", inputs["plantCond"],
              "inputs[hydroSoilGrp] = ", inputs["hydroSoilGrp"], "storage =", storage)

        ############## _________________________________##############
        # Run the calculation
        SWLs = []  # append starting water level
        EWLs = []  # append ending water level
        DPs = []  # append deep percolation
        SRs = []  # append surface runoff
        VWCs = []  # append volumetric water content
        effIrrig = []  # append effective irrigation
        irrigEffic = []  # append irrigation efficiency
        forDate = []
        FC = []
        MADg = []
        waterDeficit = []
        pwp = []
        grossIrrg = []
        rainFall = []

        #######
        # at planting date, day = 0
        day = 0
        rain = rainfall_totalIN  # dictRainfall['rainDay0']         #0.01 #API
        print("Rain on planting day = ", rain)

        # julian day
        # J0 = int(format(planting_date, '%j'))
        tt = planting_date.timetuple()
        J0 = tt.tm_yday
        print("J0 = ", J0)

        # all other values will come from API
        # ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J0)

        ET0 = penman_monteith(lat, elevation, maxTempF, minTempF,
                              maxHumidity, minHumidity, solradWM2, windSpeedMPH, J0)
        # penman_monteith(station_lat, station_z, Tmax_F,Tmin_F,Rhmax,Rhmin,avg_RS,wind_speed,J,wind_z=10,Gsc=0.0820,alpha=0.23,G=0):

        # if farmer provides irrigation value for a day
        grossIrrigation = 0  # farmer override
        grossIrrigUnit = "Acre-inch"  # dropdown if farmer provides a value in grossIrrigation

        unitConversionInfo = unit_conversion.filter(
            flowMeterReadings=grossIrrigUnit).values()
        for q in unitConversionInfo:
            conversionQUERY = q['conversion']
        grossIrrigFactor = conversionQUERY
        print("grossIrrigFactor = ", grossIrrigFactor)

        gross_irrig_inch = grossIrrigation * grossIrrigFactor

        FC_plantday = field_capacity[day]
        MADforgraph = maxAllowableDeplitionQUERY * FC_plantday
        pwp_plantday = perm_wilt_point[day]

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
            irrigation_eff = None  # np.nan
        ##############
        water_Deficit = 100 * (FC_plantday-ewl)/FC_plantday

        plantdayresults = results(Date=plantingDate, WaterLevelStart=swl, WaterLevelEnd=ewl, DeepPercolation=dp, SurfaceRunoff=sr, VolumetricWaterContent=vwc, EffectiveIrrigation=eff_irrigation, IrrigationEfficiency=irrigation_eff,
                                  MaximumAvailableDepletion=MADforgraph, FieldCapacity=FC_plantday, PermanentWiltingPoint=pwp_plantday, WaterDeficit=water_Deficit, IrrigationActivityAmount=grossIrrigation, RainObservedAmount=rainfall_totalIN, FieldId=currentField)
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

        # #### ---------------here just current day results -----------####
        # #######
        # """"""

        # # For next day to the planting day
        # print("\n\n")
        # NextDayDate = plantingDate + timedelta(days=5)
        # # NextDay_Date = str(datetime.strftime(NextDay_Date, "%m/%d/%Y"))
        # print("NextDay Date : ", NextDayDate)

        # # API request
        # rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(
        #     NextDayDate, lat, long)
        # # print("second---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)
        # ####################################################################

        # # increase day incrementally
        # day = 1
        # rain = rainfall_totalIN  # API
        # print("Rain on day 1 = ", rain)

        # # ET
        # J = J0+day
        # # all other values will come from API
        # ET0 = penman_monteith(lat, elevation, maxTempF, minTempF,
        #                       maxHumidity, minHumidity, solradWM2, windSpeedMPH, J)
        # # ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J)
        # print("ET0 : ", ET0)

        # # if farmer provides irrigation value for a day
        # grossIrrigation = 0  # farmer override
        # grossIrrigUnit = "Acre-inch"  # dropdown if farmer provides a value in grossIrrigation

        # unitConversionInfo = unit_conversion.filter(
        #     flowMeterReadings=grossIrrigUnit).values()
        # for q in unitConversionInfo:
        #     conversionQUERY = q['conversion']
        # grossIrrigFactor = conversionQUERY
        # print("grossIrrigFactor = ", grossIrrigFactor)

        # gross_irrig_inch = grossIrrigation * grossIrrigFactor
        # FC_growthday = field_capacity[day]
        # MADforgraph = maxAllowableDeplitionQUERY * FC_growthday
        # pwp_growthday = perm_wilt_point[day]

        # #########
        # swl, crop_et, eff_rainfall, sr, dp, ewl, vwc = growthDay(ET0, rain, EWLs[day-1], root_depth[day-1], root_depth[day], field_capacity[day], inputs["fieldCap"],
        #                                                          refill_point[day], perm_wilt_point[day], Kc[day], storage, gross_irrig_inch=0)

        # if (((swl-crop_et+eff_rainfall < refill_point[day] and day >= daps['Development'] and day < daps['Last Irrig. Event']) or
        #     (day >= daps['Last Irrig. Event'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
        #     (day < daps['Development'] and swl-crop_et+eff_rainfall < 1.25*perm_wilt_point[day]) or
        #         (field_capacity[day]-swl > 3 and day >= daps['Development'] and day < daps['Last Irrig. Event'])) and (field_capacity[day]-swl > 1)):
        #     eff_irrigation = field_capacity[day] - swl
        # else:
        #     eff_irrigation = 0

        # if gross_irrig_inch > 0:
        #     irrigation_eff = eff_irrigation/gross_irrig_inch
        # else:
        #     irrigation_eff = "nan"  # np.nan
        # ###############

        # water_Deficit = 100 * (FC_growthday-ewl)/FC_growthday

        # SWLs.append(swl)
        # EWLs.append(ewl)
        # DPs.append(dp)
        # SRs.append(sr)
        # VWCs.append(vwc)
        # effIrrig.append(eff_irrigation)
        # irrigEffic.append(irrigation_eff)
        # forDate.append(NextDayDate.strftime('%m/%d/%Y'))
        # FC.append(FC_growthday)
        # MADg.append(MADforgraph)
        # waterDeficit.append(water_Deficit)
        # pwp.append(pwp_growthday)
        # grossIrrg.append(grossIrrigation)
        # rainFall.append(rainfall_totalIN)

        # #-----------------------FOR LOOP-------------------------------------------------------------------------------------

        print("---  here code for loop starts  ---")
        print("\n\n")
        # #######
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

        # rain = 0        #API

        for dayI in range(1, totaldays+1):  # starts the day after planting day

            # For next day to the planting day

            NextDayDate = plantingDate + timedelta(days=dayI)
            # NextDay_Date = str(datetime.strftime(NextDay_Date, "%m/%d/%Y"))
            print("NextDay Date : ", NextDayDate)

            # API request
            rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2 = api_results(
                NextDayDate, lat, long)
            # print("second---------- ", rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2)
            ############### ____________________________________#################

            # increase day incrementally
            day = dayI
            rain = rainfall_totalIN  # API
            print("Rain on day ", dayI, " = ", rain)

            # ET
            J = J0+day
            # all other values will come from API
            ET0 = penman_monteith(lat, elevation, maxTempF, minTempF,
                                  maxHumidity, minHumidity, solradWM2, windSpeedMPH, J)
            # ET0 = penman_monteith(31.177,21.6,82.2,68,100,54.2,76,16,J)
            print("ET0 : ", ET0)

            # if farmer provides irrigation value for a day
            grossIrrigation = 0  # farmer override
            grossIrrigUnit = "Acre-inch"  # dropdown if farmer provides a value in grossIrrigation

            unitConversionInfo = unit_conversion.filter(
                flowMeterReadings=grossIrrigUnit).values()
            for q in unitConversionInfo:
                conversionQUERY = q['conversion']
            grossIrrigFactor = conversionQUERY
            print("grossIrrigFactor = ", grossIrrigFactor)

            gross_irrig_inch = grossIrrigation * grossIrrigFactor
            FC_growthday = field_capacity[day]
            MADforgraph = maxAllowableDeplitionQUERY * FC_growthday
            pwp_growthday = perm_wilt_point[day]

            #########
            swl, crop_et, eff_rainfall, sr, dp, ewl, vwc = growthDay(ET0, rain, EWLs[day-1], root_depth[day-1], root_depth[day], field_capacity[day], inputs["fieldCap"],
                                                                     refill_point[day], perm_wilt_point[day], Kc[day], storage, gross_irrig_inch=0)

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

            growingdaysresults = results(Date=NextDayDate, WaterLevelStart=swl, WaterLevelEnd=ewl, DeepPercolation=dp, SurfaceRunoff=sr, VolumetricWaterContent=vwc, EffectiveIrrigation=eff_irrigation, IrrigationEfficiency=irrigation_eff,
                                         MaximumAvailableDepletion=MADforgraph, FieldCapacity=FC_growthday, PermanentWiltingPoint=pwp_growthday, WaterDeficit=water_Deficit, IrrigationActivityAmount=grossIrrigation, RainObservedAmount=rainfall_totalIN,  FieldId=currentField)
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

        resultsDict = {'SWLs': SWLs, 'EWLs': EWLs, 'DPs': DPs, 'SRs': SRs, 'VWCs': VWCs, 'effIrrig': effIrrig, 'irrigEffic': irrigEffic, 'forDate': forDate,
                       "MAD": MADg, "FC": FC, "PWP": pwp, "Deficit(%)": waterDeficit, "irrigation activity": grossIrrg, "rain observed": rainFall}
        return Response({'results': resultsDict})
