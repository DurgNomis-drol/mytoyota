"""Toyota Connected Services API - Vehicle Models."""
from datetime import date
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic.v1 import Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.models import CustomBaseModel


class _TranslationModel(CustomBaseModel):
    english: Optional[Any]  # TODO unsure what this returns
    french: Optional[Any]  # TODO unsure what this returns
    spanish: Optional[Any]  # TODO unsure what this returns


class _CapabilitiesModel(CustomBaseModel):
    description: Optional[str]
    display: Optional[bool]
    display_name: Optional[Any] = Field(alias="displayName")  # TODO unsure what this returns
    name: Optional[str]
    translation: Optional[_TranslationModel]


class _ExtendedCapabilitiesModel(CustomBaseModel):
    c_scheduling: Optional[bool] = Field(alias="acScheduling")
    battery_status: Optional[bool] = Field(alias="batteryStatus")
    bonnet_status: Optional[bool] = Field(alias="bonnetStatus")
    bump_collisions: Optional[bool] = Field(alias="bumpCollisions")
    buzzer_capable: Optional[bool] = Field(alias="buzzerCapable")
    charge_management: Optional[bool] = Field(alias="chargeManagement")
    climate_capable: Optional[bool] = Field(alias="climateCapable")
    climate_temperature_control_full: Optional[bool] = Field(alias="climateTemperatureControlFull")
    climate_temperature_control_limited: Optional[bool] = Field(
        alias="climateTemperatureControlLimited"
    )
    dashboard_warning_lights: Optional[bool] = Field(alias="dashboardWarningLights")
    door_lock_unlock_capable: Optional[bool] = Field(alias="doorLockUnlockCapable")
    drive_pulse: Optional[bool] = Field(alias="drivePulse")
    ecare: Optional[bool] = Field(alias="ecare")
    econnect_climate_capable: Optional[bool] = Field(alias="econnectClimateCapable")
    econnect_vehicle_status_capable: Optional[bool] = Field(alias="econnectVehicleStatusCapable")
    electric_pulse: Optional[bool] = Field(alias="electricPulse")
    emergency_assist: Optional[bool] = Field(alias="emergencyAssist")
    enhanced_security_system_capable: Optional[bool] = Field(alias="enhancedSecuritySystemCapable")
    equipped_with_alarm: Optional[bool] = Field(alias="equippedWithAlarm")
    ev_battery: Optional[bool] = Field(alias="evBattery")
    ev_charge_stations_capable: Optional[bool] = Field(alias="evChargeStationsCapable")
    fcv_stations_capable: Optional[bool] = Field(alias="fcvStationsCapable")
    front_defogger: Optional[bool] = Field(alias="frontDefogger")
    front_driver_door_lock_status: Optional[bool] = Field(alias="frontDriverDoorLockStatus")
    front_driver_door_open_status: Optional[bool] = Field(alias="frontDriverDoorOpenStatus")
    front_driver_door_window_status: Optional[bool] = Field(alias="frontDriverDoorWindowStatus")
    front_driver_seat_heater: Optional[bool] = Field(alias="frontDriverSeatHeater")
    front_driver_seat_ventilation: Optional[bool] = Field(alias="frontDriverSeatVentilation")
    front_passenger_door_lock_status: Optional[bool] = Field(alias="frontPassengerDoorLockStatus")
    front_passenger_door_open_status: Optional[bool] = Field(alias="frontPassengerDoorOpenStatus")
    front_passenger_door_window_status: Optional[bool] = Field(
        alias="frontPassengerDoorWindowStatus"
    )
    front_passenger_seat_heater: Optional[bool] = Field(alias="frontPassengerSeatHeater")
    front_passenger_seat_ventilation: Optional[bool] = Field(alias="frontPassengerSeatVentilation")
    fuel_level_available: Optional[bool] = Field(alias="fuelLevelAvailable")
    fuel_range_available: Optional[bool] = Field(alias="fuelRangeAvailable")
    guest_driver: Optional[bool] = Field(alias="guestDriver")
    hazard_capable: Optional[bool] = Field(alias="hazardCapable")
    horn_capable: Optional[bool] = Field(alias="hornCapable")
    hybrid_pulse: Optional[bool] = Field(alias="hybridPulse")
    hydrogen_pulse: Optional[bool] = Field(alias="hydrogenPulse")
    last_parked_capable: Optional[bool] = Field(alias="lastParkedCapable")
    light_status: Optional[bool] = Field(alias="lightStatus")
    lights_capable: Optional[bool] = Field(alias="lightsCapable")
    manual_rear_windows: Optional[bool] = Field(alias="manualRearWindows")
    mirror_heater: Optional[bool] = Field(alias="mirrorHeater")
    moonroof: Optional[bool] = Field(alias="moonroof")
    next_charge: Optional[bool] = Field(alias="nextCharge")
    power_tailgate_capable: Optional[bool] = Field(alias="powerTailgateCapable")
    power_windows_capable: Optional[bool] = Field(alias="powerWindowsCapable")
    rear_defogger: Optional[bool] = Field(alias="rearDefogger")
    rear_driver_door_lock_status: Optional[bool] = Field(alias="rearDriverDoorLockStatus")
    rear_driver_door_open_status: Optional[bool] = Field(alias="rearDriverDoorOpenStatus")
    rear_driver_door_window_status: Optional[bool] = Field(alias="rearDriverDoorWindowStatus")
    rear_driver_seat_heater: Optional[bool] = Field(alias="rearDriverSeatHeater")
    rear_driver_seat_ventilation: Optional[bool] = Field(alias="rearDriverSeatVentilation")
    rear_hatch_rear_window: Optional[bool] = Field(alias="rearHatchRearWindow")
    rear_passenger_door_lock_status: Optional[bool] = Field(alias="rearPassengerDoorLockStatus")
    rear_passenger_door_open_status: Optional[bool] = Field(alias="rearPassengerDoorOpenStatus")
    rear_passenger_door_window_status: Optional[bool] = Field(
        alias="rearPassengerDoorWindowStatus"
    )
    rear_passenger_seat_heater: Optional[bool] = Field(alias="rearPassengerSeatHeater")
    rear_passenger_seat_ventilation: Optional[bool] = Field(alias="rearPassengerSeatVentilation")
    remote_econnect_capable: Optional[bool] = Field(alias="remoteEConnectCapable")
    remote_engine_start_stop: Optional[bool] = Field(alias="remoteEngineStartStop")
    smart_key_status: Optional[bool] = Field(alias="smartKeyStatus")
    steering_heater: Optional[bool] = Field(alias="steeringHeater")
    stellantis_climate_capable: Optional[bool] = Field(alias="stellantisClimateCapable")
    stellantis_vehicle_status_capable: Optional[bool] = Field(
        alias="stellantisVehicleStatusCapable"
    )
    sunroof: Optional[bool] = Field(alias="sunroof")
    telemetry_capable: Optional[bool] = Field(alias="telemetryCapable")
    trunk_lock_unlock_capable: Optional[bool] = Field(alias="trunkLockUnlockCapable")
    try_and_play: Optional[bool] = Field(alias="tryAndPlay")
    vehicle_diagnostic_capable: Optional[bool] = Field(alias="vehicleDiagnosticCapable")
    vehicle_finder: Optional[bool] = Field(alias="vehicleFinder")
    vehicle_status: Optional[bool] = Field(alias="vehicleStatus")
    we_hybrid_capable: Optional[bool] = Field(alias="weHybridCapable")
    weekly_charge: Optional[bool] = Field(alias="weeklyCharge")


class _LinksModel(CustomBaseModel):
    body: Optional[str]  # TODO unsure what this returns
    button_text: Optional[str] = Field(alias="buttonText")
    image_url: Optional[str] = Field(alias="imageUrl", default=None)
    link: Optional[str]
    name: Optional[str]


class _DcmModel(CustomBaseModel):  # Data connection model
    country_code: Optional[str] = Field(alias="countryCode", default=None)
    destination: Optional[str] = Field(alias="dcmDestination")
    grade: Optional[str] = Field(alias="dcmGrade")
    car_model_year: Optional[str] = Field(alias="dcmModelYear")
    supplier: Optional[str] = Field(alias="dcmSupplier")
    supplier_name: Optional[str] = Field(alias="dcmSupplierName", default=None)
    euicc_id: Optional[str] = Field(alias="euiccid")
    hardware_type: Optional[str] = Field(alias="hardwareType")
    vehicle_unit_terminal_number: Optional[str] = Field(alias="vehicleUnitTerminalNumber")


class _HeadUnitModel(CustomBaseModel):
    description: Optional[Any] = Field(alias="huDescription")  # TODO unsure what this returns
    generation: Optional[Any] = Field(alias="huGeneration")  # TODO unsure what this returns
    version: Optional[Any] = Field(alias="huVersion")  # TODO unsure what this returns
    mobile_platform_code: Optional[Any] = Field(
        alias="mobilePlatformCode"
    )  # TODO unsure what this returns
    multimedia_type: Optional[Any] = Field(alias="multimediaType")  # TODO unsure what this returns


class _SubscriptionsModel(CustomBaseModel):
    auto_renew: Optional[bool] = Field(alias="autoRenew")
    category: Optional[str]
    components: Optional[Any]  # TODO unsure what this returns
    consolidated_goodwill_ids: Optional[List[Any]] = Field(
        alias="consolidatedGoodwillIds"
    )  # TODO unsure what this returns
    consolidated_product_ids: Optional[List[Any]] = Field(
        alias="consolidatedProductIds"
    )  # TODO unsure what this returns
    display_procuct_name: Optional[str] = Field(alias="displayProductName")
    display_term: Optional[str] = Field(alias="displayTerm")
    future_cancel: Optional[bool] = Field(alias="futureCancel")
    good_will_issued_for: Optional[Any] = Field(
        alias="goodwillIssuedFor"
    )  # TODO unsure what this returns
    product_code: Optional[str] = Field(alias="productCode")
    product_description: Optional[str] = Field(alias="productDescription")
    product_line: Optional[str] = Field(alias="productLine")
    product_name: Optional[str] = Field(alias="productName")
    procut_type: Optional[Any] = Field(alias="productType")
    renewable: Optional[bool]
    status: Optional[str]
    subscription_end_date: Optional[date] = Field(alias="subscriptionEndDate")
    subscription_id: Optional[str] = Field(alias="subscriptionID")
    subscription_next_billing_date: Optional[Any] = Field(
        alias="subscriptionNextBillingDate",
    )  # TODO unsure what this returns
    subscription_remaining_days: Optional[int] = Field(alias="subscriptionRemainingDays")
    subscription_remaining_term: Optional[Any] = Field(
        alias="subscriptionRemainingTerm",
    )  # TODO unsure what this returns
    subscription_start_date: Optional[date] = Field(alias="subscriptionStartDate")
    subscription_term: Optional[str] = Field(alias="subscriptionTerm")
    term: Optional[int]
    term_unit: Optional[str] = Field(alias="termUnit")
    type: Optional[str]


class _RemoteServiceCapabilitiesModel(CustomBaseModel):
    acsetting_enabled: Optional[bool] = Field(alias="acsettingEnabled")
    allow_hvac_override_capable: Optional[bool] = Field(alias="allowHvacOverrideCapable")
    dlock_unlock_capable: Optional[bool] = Field(alias="dlockUnlockCapable")
    estart_enabled: Optional[bool] = Field(alias="estartEnabled")
    estart_stop_capable: Optional[bool] = Field(alias="estartStopCapable")
    estop_enabled: Optional[bool] = Field(alias="estopEnabled")
    guest_driver_capable: Optional[bool] = Field(alias="guestDriverCapable")
    hazard_capable: Optional[bool] = Field(alias="hazardCapable")
    head_light_capable: Optional[bool] = Field(alias="headLightCapable")
    moon_roof_capable: Optional[bool] = Field(alias="moonRoofCapable")
    power_window_capable: Optional[bool] = Field(alias="powerWindowCapable")
    steering_wheel_heater_capable: Optional[bool] = Field(alias="steeringWheelHeaterCapable")
    trunk_capable: Optional[bool] = Field(alias="trunkCapable")
    vehicle_finder_capable: Optional[bool] = Field(alias="vehicleFinderCapable")
    ventilator_capable: Optional[bool] = Field(alias="ventilatorCapable")


class _DataConsentModel(CustomBaseModel):
    can_300: Optional[bool] = Field(alias="can300")
    dealer_contact: Optional[bool] = Field(alias="dealerContact")
    service_connect: Optional[bool] = Field(alias="serviceConnect")
    ubi: Optional[bool] = Field(alias="ubi")


class _FeaturesModel(CustomBaseModel):
    ach_payment: Optional[bool] = Field(alias="achPayment")
    add_service_record: Optional[bool] = Field(alias="addServiceRecord")
    auto_drive: Optional[bool] = Field(alias="autoDrive")
    cerence: Optional[bool] = Field(alias="cerence")
    charging_station: Optional[bool] = Field(alias="chargingStation")
    climate_start_engine: Optional[bool] = Field(alias="climateStartEngine")
    collision_assistance: Optional[bool] = Field(alias="collisionAssistance")
    connected_card: Optional[bool] = Field(alias="connectedCard")
    connected_insurance: Optional[bool] = Field(alias="connectedInsurance")
    connected_support: Optional[bool] = Field(alias="connectedSupport")
    crash_notification: Optional[bool] = Field(alias="crashNotification")
    critical_alert: Optional[bool] = Field(alias="criticalAlert")
    dashboard_lights: Optional[bool] = Field(alias="dashboardLights")
    dealer_appointment: Optional[bool] = Field(alias="dealerAppointment")
    digital_key: Optional[bool] = Field(alias="digitalKey")
    door_lock_capable: Optional[bool] = Field(alias="doorLockCapable")
    drive_pulse: Optional[bool] = Field(alias="drivePulse")
    driver_companion: Optional[bool] = Field(alias="driverCompanion")
    driver_score: Optional[bool] = Field(alias="driverScore")
    dtc_access: Optional[bool] = Field(alias="dtcAccess")
    dynamic_navi: Optional[bool] = Field(alias="dynamicNavi")
    eco_history: Optional[bool] = Field(alias="ecoHistory")
    eco_ranking: Optional[bool] = Field(alias="ecoRanking")
    electric_pulse: Optional[bool] = Field(alias="electricPulse")
    emergency_assist: Optional[bool] = Field(alias="emergencyAssist")
    enhanced_security_system: Optional[bool] = Field(alias="enhancedSecuritySystem")
    ev_charge_station: Optional[bool] = Field(alias="evChargeStation")
    ev_remote_services: Optional[bool] = Field(alias="evRemoteServices")
    ev_vehicle_status: Optional[bool] = Field(alias="evVehicleStatus")
    financial_services: Optional[bool] = Field(alias="financialServices")
    flex_rental: Optional[bool] = Field(alias="flexRental")
    h2_fuel_station: Optional[bool] = Field(alias="h2FuelStation")
    home_charge: Optional[bool] = Field(alias="homeCharge")
    how_to_videos: Optional[bool] = Field(alias="howToVideos")
    hybrid_pulse: Optional[bool] = Field(alias="hybridPulse")
    hydrogen_pulse: Optional[bool] = Field(alias="hydrogenPulse")
    important_message: Optional[bool] = Field(alias="importantMessage")
    insurance: Optional[bool] = Field(alias="insurance")
    last_parked: Optional[bool] = Field(alias="lastParked")
    lcfs: Optional[bool] = Field(alias="lcfs")
    linked_accounts: Optional[bool] = Field(alias="linkedAccounts")
    maintenance_timeline: Optional[bool] = Field(alias="maintenanceTimeline")
    marketing_card: Optional[bool] = Field(alias="marketingCard")
    marketing_consent: Optional[bool] = Field(alias="marketingConsent")
    master_consent_editable: Optional[bool] = Field(alias="masterConsentEditable")
    my_destination: Optional[bool] = Field(alias="myDestination")
    owners_manual: Optional[bool] = Field(alias="ownersManual")
    paid_product: Optional[bool] = Field(alias="paidProduct")
    parked_vehicle_locator: Optional[bool] = Field(alias="parkedVehicleLocator")
    parking: Optional[bool] = Field(alias="parking")
    parking_notes: Optional[bool] = Field(alias="parkingNotes")
    personalized_settings: Optional[bool] = Field(alias="personalizedSettings")
    privacy: Optional[bool] = Field(alias="privacy")
    recent_trip: Optional[bool] = Field(alias="recentTrip")
    remote_dtc: Optional[bool] = Field(alias="remoteDtc")
    remote_parking: Optional[bool] = Field(alias="remoteParking")
    remote_service: Optional[bool] = Field(alias="remoteService")
    roadside_assistance: Optional[bool] = Field(alias="roadsideAssistance")
    safety_recall: Optional[bool] = Field(alias="safetyRecall")
    schedule_maintenance: Optional[bool] = Field(alias="scheduleMaintenance")
    service_history: Optional[bool] = Field(alias="serviceHistory")
    shop_genuine_parts: Optional[bool] = Field(alias="shopGenuineParts")
    smart_charging: Optional[bool] = Field(alias="smartCharging")
    ssa_download: Optional[bool] = Field(alias="ssaDownload")
    sxm_radio: Optional[bool] = Field(alias="sxmRadio")
    telemetry: Optional[bool] = Field(alias="telemetry")
    tff: Optional[bool] = Field(alias="tff")
    tire_pressure: Optional[bool] = Field(alias="tirePressure")
    v1g: Optional[bool] = Field(alias="v1g")
    va_setting: Optional[bool] = Field(alias="vaSetting")
    vehicle_diagnostic: Optional[bool] = Field(alias="vehicleDiagnostic")
    vehicle_health_report: Optional[bool] = Field(alias="vehicleHealthReport")
    vehicle_specifications: Optional[bool] = Field(alias="vehicleSpecifications")
    vehicle_status: Optional[bool] = Field(alias="vehicleStatus")
    we_hybrid: Optional[bool] = Field(alias="weHybrid")
    wifi: Optional[bool] = Field(alias="wifi")
    xcapp: Optional[bool] = Field(alias="xcapp")


class VehicleGuidModel(CustomBaseModel):
    """Model representing a vehicle with its associated information.

    Attributes
    ----------
        alerts (List[Any]): The alerts associated with the vehicle.
        asiCode (str): The ASI code of the vehicle.
        brand (str): The brand of the vehicle.
        capabilities (List[_CapabilitiesModel]): The capabilities of the vehicle.
        car_line_name (str): The name of the car line.
        color (str): The color of the vehicle.
        commercial_rental (bool): Indicates if the vehicle is used for commercial rental.
        contract_id (str): The contract ID of the vehicle.
        cts_links (_LinksModel): The CTS (Connected Technologies Services) links of the vehicle.
        data_consent (_DataConsentModel): The data consent information of the vehicle.
        date_of_first_use (Optional[date]): The date of first use of the vehicle.
        dcm (_DcmModel): The DCM (Data Communication Module) information of the vehicle.
        dcm_active (bool): Indicates if the DCM is active for the vehicle.
        dcms (Optional[Any]): The DCMS (Data Communication Module Status) information
            of the vehicle.
        display_model_description (str): The description of the displayed model.
        display_subscriptions (List[Dict[str, str]]): The displayed subscriptions of the vehicle.
        electrical_platform_code (str): The electrical platform code of the vehicle.
        emergency_contact (Optional[Any]): The emergency contact information of the vehicle.
        ev_vehicle (bool): Indicates if the vehicle is an electric vehicle.
        extended_capabilities (_ExtendedCapabilitiesModel): The extended capabilities
            of the vehicle.
        external_subscriptions (Optional[Any]): The external subscriptions of the vehicle.
        family_sharing (bool): Indicates if the vehicle is part of a family sharing plan.
        faq_url (str): The URL of the FAQ (Frequently Asked Questions) for the vehicle.
        features (_FeaturesModel): The features of the vehicle.
        fleet_ind (Optional[Any]): The fleet indicator of the vehicle.
        generation (str): The generation of the vehicle.
        head_unit (_HeadUnitModel): The head unit information of the vehicle.
        hw_type (Optional[Any]): The hardware type of the vehicle.
        image (str): The image URL of the vehicle.
        imei (str): The IMEI (International Mobile Equipment Identity) of the vehicle.
        katashiki_code (str): The katashiki code of the vehicle.
        manufactured_date (date): The manufactured date of the vehicle.
        manufactured_code (str): The manufacturer code of the vehicle.
        car_model_code (str): The model code of the vehicle.
        car_model_description (str): The description of the model of the vehicle.
        car_model_name (str): The name of the model of the vehicle.
        car_model_year (str): The model year of the vehicle.
        nickname (Optional[str]): The nickname of the vehicle.
        non_cvt_vehicle (bool): Indicates if the vehicle is a non-CVT
            (Continuously Variable Transmission) vehicle.
        old_imei (Optional[Any]): The old IMEI of the vehicle.
        owner (bool): Indicates if the user is the owner of the vehicle.
        personalized_settings (_LinksModel): The personalized settings of the vehicle.
        preferred (Optional[bool]): Indicates if the vehicle is the preferred vehicle.
        primary_subscriber (bool): Indicates if the user is the primary subscriber of the vehicle.
        region (str): The region of the vehicle.
        registration_number (Optional[str]): The registration number of the vehicle.
        remote_display (Optional[Any]): The remote display information of the vehicle.
        remote_service_capabilities (_RemoteServiceCapabilitiesModel): The remote
            service capabilities of the vehicle.
        remote_service_exceptions (List[Any]): The remote service exceptions of the vehicle.
        remote_subscription_exists (bool): Indicates if a remote subscription
            exists for the vehicle.
        remote_subscription_status (str): The remote subscription status of the vehicle.
        remote_user (bool): Indicates if the user is a remote user of the vehicle.
        remote_user_guid (Optional[Union[UUID, str]]): The remote user GUID
            (Globally Unique Identifier) of the vehicle.
        service_connect_status (Optional[Any]): The service connect status of the vehicle.
        services (List[Any]): The services associated with the vehicle.
        shop_genuine_parts_url (str): The URL for shopping genuine parts for the vehicle.
        status (str): The status of the vehicle.
        stock_pic_reference (str): The stock picture reference of the vehicle.
        subscriber_guid (UUID): The subscriber GUID of the vehicle.
        subscription_expiration_status (bool): Indicates if the subscription
            is expired for the vehicle.
        subscription_status (str): The subscription status of the vehicle.
        subscriptions (List[_SubscriptionsModel]): The subscriptions associated with the vehicle.
        suffix_code (Optional[Any]): The suffix code of the vehicle.
        svl_satus (bool): Indicates the SVL (Smart Vehicle Link) status of the vehicle.
        tff_links (_LinksModel): The TFF (Toyota Friend Finder) links of the vehicle.
        transmission_type (str): The transmission type of the vehicle.
        vehicle_capabilities (List[Any]): The capabilities of the vehicle.
        vehicle_data_consents (Optional[Any]): The vehicle data consents of the vehicle.
        vin (str): The VIN (Vehicle Identification Number) of the vehicle.

    """

    alerts: Optional[List[Any]]  # TODO unsure what this returns
    asi_code: Optional[str] = Field(alias="asiCode")
    brand: Optional[str]
    capabilities: Optional[List[_CapabilitiesModel]]
    car_line_name: Optional[str] = Field(alias="carlineName")
    color: Optional[str]
    commercial_rental: Optional[bool] = Field(alias="commercialRental")
    contract_id: Optional[str] = Field(alias="contractId")
    cts_links: Optional[_LinksModel] = Field(alias="ctsLinks")
    data_consent: Optional[_DataConsentModel] = Field(alias="dataConsent")
    date_of_first_use: Optional[date] = Field(alias="dateOfFirstUse")
    dcm: Optional[_DcmModel] = None
    dcm_active: Optional[bool] = Field(alias="dcmActive")
    dcms: Optional[Any]  # TODO unsure what this returns
    display_model_description: Optional[str] = Field(alias="displayModelDescription")
    display_subscriptions: Optional[List[Dict[str, str]]] = Field(alias="displaySubscriptions")
    electrical_platform_code: Optional[str] = Field(alias="electricalPlatformCode", default=None)
    emergency_contact: Optional[Any] = Field(
        alias="emergencyContact"
    )  # TODO unsure what this returns
    ev_vehicle: Optional[bool] = Field(alias="evVehicle")
    extended_capabilities: Optional[_ExtendedCapabilitiesModel] = Field(
        alias="extendedCapabilities"
    )
    external_subscriptions: Optional[Any] = Field(alias="externalSubscriptions")
    family_sharing: Optional[bool] = Field(alias="familySharing")
    faq_url: Optional[str] = Field(alias="faqUrl")
    features: Optional[_FeaturesModel]
    fleet_ind: Optional[Any] = Field(alias="fleetInd")  # TODO unsure what this returns
    fuel_type: Optional[str] = Field(alias="fuelType", default=None)
    generation: Optional[str]
    head_unit: Optional[_HeadUnitModel] = Field(alias="headUnit")
    hw_type: Optional[Any] = Field(alias="hwType")  # TODO unsure what this returns
    image: Optional[str]
    imei: Optional[str]
    katashiki_code: Optional[str] = Field(alias="katashikiCode")
    manufactured_date: Optional[date] = Field(alias="manufacturedDate")
    manufactured_code: Optional[str] = Field(alias="manufacturerCode")
    car_model_code: Optional[str] = Field(alias="modelCode")
    car_model_description: Optional[str] = Field(alias="modelDescription")
    car_model_name: Optional[str] = Field(alias="modelName")
    car_model_year: Optional[str] = Field(alias="modelYear")
    nickname: Optional[str] = Field(alias="nickName", default=None)
    non_cvt_vehicle: Optional[bool] = Field(alias="nonCvtVehicle")
    old_imei: Optional[Any] = Field(alias="oldImei")  # TODO unsure what this returns
    owner: Optional[bool]
    personalized_settings: Optional[_LinksModel] = Field(
        alias="personalizedSettings"
    )  # TODO unsure what this returns
    preferred: Optional[bool] = None
    primary_subscriber: Optional[bool] = Field(alias="primarySubscriber")
    region: Optional[str]
    registration_number: Optional[str] = Field(alias="registrationNumber")
    remote_display: Optional[Any] = Field(alias="remoteDisplay")  # TODO unsure what this returns
    remote_service_capabilities: Optional[_RemoteServiceCapabilitiesModel] = Field(
        alias="remoteServiceCapabilities"
    )
    remote_service_exceptions: Optional[List[Any]] = Field(
        alias="remoteServicesExceptions"
    )  # TODO unsure what this returns
    remote_subscription_exists: Optional[bool] = Field(alias="remoteSubscriptionExists")
    remote_subscription_status: Optional[str] = Field(alias="remoteSubscriptionStatus")
    remote_user: Optional[bool] = Field(alias="remoteUser")
    remote_user_guid: Optional[Union[UUID, str]] = Field(alias="remoteUserGuid", default=None)
    service_connect_status: Optional[Any] = Field(
        alias="serviceConnectStatus"
    )  # TODO unsure what this returns
    services: Optional[List[Any]]  # TODO unsure what this returns
    shop_genuine_parts_url: Optional[str] = Field(alias="shopGenuinePartsUrl")
    status: Optional[str]
    stock_pic_reference: Optional[str] = Field(alias="stockPicReference")
    subscriber_guid: Optional[UUID] = Field(alias="subscriberGuid")
    subscription_expiration_status: Optional[bool] = Field(alias="subscriptionExpirationStatus")
    subscription_status: Optional[str] = Field(alias="subscriptionStatus")
    subscriptions: Optional[List[_SubscriptionsModel]]
    suffix_code: Optional[Any] = Field(alias="suffixCode")
    svl_satus: Optional[bool] = Field(alias="svlStatus")
    tff_links: Optional[_LinksModel] = Field(alias="tffLinks")
    transmission_type: Optional[str] = Field(alias="transmissionType")
    vehicle_capabilities: Optional[List[Any]] = Field(alias="vehicleCapabilities")
    vehicle_data_consents: Optional[Any] = Field(alias="vehicleDataConsents")
    vin: Optional[str]


class VehiclesResponseModel(StatusModel):
    r"""Model representing a vehicles response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[List[VehicleGuidModel]], optional): The vehicles payload. \n
            Defaults to None.

    """

    payload: Optional[List[VehicleGuidModel]] = None
