import numpy as np

# Penman-Monteith function
def penman_monteith(station_lat, station_z, Tmax_F,Tmin_F,Rhmax,Rhmin,avg_RS,wind_speed,J,wind_z=10,Gsc=0.0820,alpha=0.23,G=0):
    """
    station_lat = Latitude of the station (degrees)  ##https://api.aerisapi.com/normals/stations?client_id={{clientID}}&client_secret={{clientSecret}}&p=70803 loc.lat
    station_z = altitude of the station (meters)     ##https://www.aerisweather.com/support/docs/api/reference/endpoints/normals-stations/. profile.elevFT 
    Tmax_F = maximum temperature in F
    Tmin_F = minimum temperature in F
    Rhmax = maximum relative humidity (%)
    Rhmin = minimum relative humidity (%)
    avg_RS = average radiation in W/m2    #solrad 
    wind_speed = average wind speed in mph
    J =Julian day (day number from 1 to 366)  ## not from API
    wind_z = height at which the wind speed is estimated (default:10m)  ## check if we need it from API
    
    Gsc = solar constant (MJ m-2 min-1)
    alpha = Albedo (For the green grass reference crop, alpha is assumed to have a value of 0.23)
    G = Soil heat flux (the soil heat flux is small compared to Rn and may often be ignored)
    
    """

    Tmax = (Tmax_F-32)*(5/9) + 273.15
    Tmin = (Tmin_F-32)*(5/9) + 273.15
    Tmean= ((Tmax+ Tmin)/2 ) - 273.15 
    u2= (wind_speed*0.44704*4.87)/np.log(67.8*wind_z-5.42)
    P = 101.3*np.power(((293-0.0065*station_z)/293),5.26)
    y= 0.000665 * P
    slope = 4098 * 0.6108 * np.exp(17.27 * Tmean /(Tmean+237.3)) / np.power((Tmean+237.3),2) 
    
    etmax = 0.6108 * np.exp(17.27*(Tmax-273.15)/(Tmax-273.15+237.3))
    etmin = 0.6108 * np.exp(17.27*(Tmin-273.15)/(Tmin-273.15+237.3))
    es = (etmax + etmin)/2
    ea = ((Rhmax/100)*etmin + (Rhmin/100) * etmax)/2
    
    dr = 1 + 0.033 * np.cos((2*3.1416*J)/365)
    shy = (3.1416/180) * station_lat
    delta = 0.409 * np.sin(((2*3.1416*J)/365) - 1.39)
    ws = np.arccos(-np.tan(shy)* np.tan(delta))
    
    Ra = (24*60/3.1416) * Gsc * dr * (ws*np.sin(shy)*np.sin(delta) + np.cos(shy)*np.cos(delta)*np.sin(ws))
    Rso = (0.75 + 2*  10**-5 *station_z) * Ra

    Rs = 0.0864 * avg_RS    
    Rns = (1-alpha) * Rs
    
    sigma_max = 4.903 * 10**-9 * np.power(Tmax,4)
    sigma_min = 4.903 * 10**-9* np.power(Tmin,4)
      
    if (Rs/Rso)<0.3:
        Rs_Rso = 0.3
    elif (Rs/Rso)>1:
        Rs_Rso = 1.0
    else:
        Rs_Rso = Rs/Rso
        
    Rnl =(sigma_max + sigma_min)/2 * (0.34 - 0.14* np.sqrt(ea)) * (1.35 * (Rs_Rso) - 0.35)
    Rn = Rns - Rnl
    
    term1= 0.408 * slope * (Rn-G)/(slope + y * (1+0.34*u2))
    term2= y *(900/(Tmean+273.15)) * u2 * (es-ea) / (slope + y * (1+0.34*u2))
    return round((term1+term2)/25.4,2)

def plantingDay(ET0,rain,fc,ratio,pwp,rp,Kc,storage,root_depth,gross_irrig_inch=0):
    swl = fc - ratio * (fc - pwp)
    if swl>rp:
        Ks = 1
    else:
        Ks = (swl - pwp)/(rp-pwp)

    crop_et = ET0 * Kc * Ks
    
    if rain < 0.1:
        sr = rain
    else:
        sr = ((rain-0.2*storage)**2/(rain+0.8*storage))
    
    if swl-crop_et+rain+gross_irrig_inch>fc:
        dp = swl-crop_et+rain+gross_irrig_inch-fc
    else:
        dp = 0
        
    if swl-crop_et+rain-sr>fc:
        eff_rainfall = fc - swl
    else:
        eff_rainfall = rain - sr

    if swl-crop_et+eff_rainfall+gross_irrig_inch<pwp:
        ewl = pwp
    else:
        ewl = swl-crop_et+eff_rainfall+gross_irrig_inch
    
    vwc = ewl/root_depth

    return (swl,crop_et,eff_rainfall, sr, dp,ewl,vwc)

def growthDay(ET0,rain,ewl0,root_depth0,root_depth,fc,field_cap,rp,pwp,Kc,storage,gross_irrig_inch=0):  
    
    if ewl0>fc:
        swl = fc
    else:
        if root_depth>root_depth0:
            swl = (root_depth-root_depth0)*field_cap + ewl0
        else:
            swl = ewl0
    
    if swl>rp:
        Ks = 1
    else:
        Ks = (swl - pwp)/(rp-pwp)
    
    crop_et = ET0 * Kc * Ks
    
    if rain < 0.1:
        sr = rain
    else:
        sr = ((rain-0.2*storage)**2/(rain+0.8*storage))

    if swl-crop_et+rain+gross_irrig_inch>fc:
        dp = swl-crop_et+rain+gross_irrig_inch-fc
    else:
        dp = 0

    if swl-crop_et+rain-sr>fc:
        eff_rainfall = fc - swl
    else:
        eff_rainfall = rain - sr

    if swl-crop_et+eff_rainfall+gross_irrig_inch<pwp:
        ewl = pwp
    else:
        ewl = swl-crop_et+eff_rainfall+gross_irrig_inch
    
    vwc = ewl/root_depth
     
    return (swl,crop_et,eff_rainfall, sr, dp,ewl,vwc)
    
  