# RAV4 plug-in hybrid HVAC remote control API

Log of the API requests.

## Get HVAC Status

### Request
```
GET https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/remoteControl/status HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip
```

### Response
```
content-type: application/json;charset=utf-8
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: 0
x-frame-options: DENY
vary: Origin
access-control-allow-credentials: true
content-length: 852
date: Mon, 31 Oct 2022 07:02:46 GMT
strict-transport-security: max-age=86400
  
{
    "ReturnCode": "000000",
    "VehicleInfo": {
        "AcquisitionDatetime": "2022-10-31T06:56:52Z",
        "ChargeInfo": {
            "BatteryPowerSupplyPossibleTime": 16383,
            "ChargeEndTime": "42:35",
            "ChargeRemainingAmount": 91,
            "ChargeStartTime": "42:35",
            "ChargeType": 15,
            "ChargeWeek": 0,
            "ChargingStatus": "none",
            "ConnectorStatus": 2,
            "EvDistanceInKm": 68.6,
            "EvDistanceWithAirCoInKm": 64.48,
            "EvTravelableDistance": 68.6,
            "EvTravelableDistanceSubtractionRate": 6,
            "GasolineTravelableDistance": 349,
            "GasolineTravelableDistanceUnit": 1,
            "PlugInHistory": 33,
            "PlugStatus": 12,
            "RemainingChargeTime": 65535,
            "SettingChangeAcceptanceStatus": 0
        },
        "RemoteHvacInfo": {
            "BlowerStatus": 0,
            "FrontDefoggerStatus": 0,
            "InsideTemperature": 22,
            "LatestAcStartTime": "2022-10-31T05:47:36Z",
            "RearDefoggerStatus": 0,
            "RemoteHvacMode": 0,
            "RemoteHvacProhibitionSignal": 1,
            "SettingTemperature": 28.0,
            "TemperatureDisplayFlag": 1,
            "Temperaturelevel": 29
        }
    }
}
```

## Turn On HVAC

### Request
```
POST https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/remoteControl HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Content-Type: application/json; charset=UTF-8
Content-Length: 145
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip

{
    "RemoteHvac": {
        "Option": {
            "FrontDefogger": 0,
            "RearDefogger": 0
        },
        "Sw": 1,
        "Temperature": {
            "SettingTemperature": 20,
            "SettingType": 0,
            "TemperatureUnit": 1
        }
    }
}
```

### Response
```
content-type: application/json;charset=utf-8
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: 0
x-frame-options: DENY
vary: Origin
access-control-allow-credentials: true
content-length: 77
date: Sun, 30 Oct 2022 14:02:55 GMT
strict-transport-security: max-age=86400

{
    "AppRequestNo": "cf9b85a7-2448-3649-9890-c7cd4a3b1e2f",
    "ReturnCode": "000000"
}
```

## Turn Off HVAC

### Request
```
POST https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/remoteControl HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Content-Type: application/json; charset=UTF-8
Content-Length: 23
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip

{
    "RemoteHvac": {
        "Sw": 0
    }
}
```

### Response

```
content-type: application/json;charset=utf-8
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: 0
x-frame-options: DENY
vary: Origin
access-control-allow-credentials: true
content-length: 77
date: Sun, 30 Oct 2022 14:01:29 GMT
strict-transport-security: max-age=86400

{
    "AppRequestNo": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "ReturnCode": "000000"
}
```

## Get AC Reservations (Schedules)

### Request

```
GET https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/hvac/reservations HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip
```

### Response
```
{
    "AirConditioningReservation": [
        {
            "ActiveStatus": 0,
            "Onetime": {
                "AirConditioning": {
                    "Option": {
                        "FrontDefogger": 1,
                        "RearDefogger": 1
                    },
                    "Temperature": {
                        "SettingTemperature": 29.0,
                        "SettingType": 0,
                        "TemperatureUnit": 1
                    }
                },
                "Date": "2021-03-11",
                "Hours": 3,
                "Minutes": 45
            },
            "ReservationNo": 1
        }
    ],
    "ReturnCode": "000000"
}
```

## Enable reservation

### Request
```
PUT https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/hvac/reservations/1 HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Content-Type: application/json; charset=UTF-8
Content-Length: 18
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip

{
    "ActiveStatus": 1
}
```

### Response

```
content-type: application/json;charset=utf-8
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: 0
x-frame-options: DENY
vary: Origin
access-control-allow-credentials: true
content-length: 23
date: Sun, 30 Oct 2022 11:53:12 GMT
strict-transport-security: max-age=86400

{
    "ReturnCode": "000000"
}
```

## New Reservation

### Request

```
POST https://myt-agg.toyota-europe.com/cma/api/vehicles/$VEHICLE_ID/hvac/reservations HTTP/1.1
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
X-TME-LOCALE: fi-fi
Cookie: iPlanetDirectoryPro=$COOKIE_DATA
brand: TOYOTA
X-TME-BRAND: TOYOTA
X-TME-ORIGIN: AN-TOYOTA
User-Agent: MyT/4.13.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-G981B Build/SP1A.210812.016)
X-TME-APP-VERSION: 4.13.1
Accept-Language: fi-FI
Content-Type: application/json; charset=UTF-8
Content-Length: 214
Host: myt-agg.toyota-europe.com
Connection: Keep-Alive
Accept-Encoding: gzip

{
    "ActiveStatus": 1,
    "Repetition": {
        "AirConditioning": {
            "Option": {
                "FrontDefogger": 0,
                "RearDefogger": 0
            },
            "Temperature": {
                "SettingTemperature": 21.0,
                "SettingType": 0,
                "TemperatureUnit": 1
            }
        },
        "Hours": 11,
        "Minutes": 55,
        "Week": [
            4,
            6
        ]
    }
}
```
### Response:
```
content-type: application/json;charset=utf-8
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
cache-control: no-cache, no-store, max-age=0, must-revalidate
pragma: no-cache
expires: 0
x-frame-options: DENY
vary: Origin
access-control-allow-credentials: true
content-length: 41
date: Sun, 30 Oct 2022 11:53:30 GMT
strict-transport-security: max-age=86400

{
    "ReservationNo": 2,
    "ReturnCode": "000000"
}
```


