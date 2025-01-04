"""Toyota Connected Services API - Vehicle Models."""
from datetime import date
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.models import CustomBaseModel


class _TranslationModel(CustomBaseModel):
    english: Optional[Any] = None  # TODO unsure what this returns
    french: Optional[Any] = None  # TODO unsure what this returns
    spanish: Optional[Any] = None  # TODO unsure what this returns


class _CapabilitiesModel(CustomBaseModel):
    description: Optional[str] = None
    display: Optional[bool] = None
    display_name: Optional[Any] = Field(None, alias="displayName")  # TODO unsure what this returns
    name: Optional[str] = None
    translation: Optional[_TranslationModel] = None


class _ExtendedCapabilitiesModel(CustomBaseModel):
    c_scheduling: Optional[bool] = Field(None, alias="acScheduling")
    battery_status: Optional[bool] = Field(None, alias="batteryStatus")
    bonnet_status: Optional[bool] = Field(None, alias="bonnetStatus")
    bump_collisions: Optional[bool] = Field(None, alias="bumpCollisions")
    buzzer_capable: Optional[bool] = Field(None, alias="buzzerCapable")
    charge_management: Optional[bool] = Field(None, alias="chargeManagement")
    climate_capable: Optional[bool] = Field(None, alias="climateCapable")
    climate_temperature_control_full: Optional[bool] = Field(None, alias="climateTemperatureControlFull")
    climate_temperature_control_limited: Optional[bool] = Field(
        None, alias="climateTemperatureControlLimited"
    )
    dashboard_warning_lights: Optional[bool] = Field(None, alias="dashboardWarningLights")
    door_lock_unlock_capable: Optional[bool] = Field(None, alias="doorLockUnlockCapable")
    drive_pulse: Optional[bool] = Field(None, alias="drivePulse")
    ecare: Optional[bool] = Field(None, alias="ecare")
    econnect_climate_capable: Optional[bool] = Field(None, alias="econnectClimateCapable")
    econnect_vehicle_status_capable: Optional[bool] = Field(None, alias="econnectVehicleStatusCapable")
    electric_pulse: Optional[bool] = Field(None, alias="electricPulse")
    emergency_assist: Optional[bool] = Field(None, alias="emergencyAssist")
    enhanced_security_system_capable: Optional[bool] = Field(None, alias="enhancedSecuritySystemCapable")
    equipped_with_alarm: Optional[bool] = Field(None, alias="equippedWithAlarm")
    ev_battery: Optional[bool] = Field(None, alias="evBattery")
    ev_charge_stations_capable: Optional[bool] = Field(None, alias="evChargeStationsCapable")
    fcv_stations_capable: Optional[bool] = Field(None, alias="fcvStationsCapable")
    front_defogger: Optional[bool] = Field(None, alias="frontDefogger")
    front_driver_door_lock_status: Optional[bool] = Field(None, alias="frontDriverDoorLockStatus")
    front_driver_door_open_status: Optional[bool] = Field(None, alias="frontDriverDoorOpenStatus")
    front_driver_door_window_status: Optional[bool] = Field(None, alias="frontDriverDoorWindowStatus")
    front_driver_seat_heater: Optional[bool] = Field(None, alias="frontDriverSeatHeater")
    front_driver_seat_ventilation: Optional[bool] = Field(None, alias="frontDriverSeatVentilation")
    front_passenger_door_lock_status: Optional[bool] = Field(None, alias="frontPassengerDoorLockStatus")
    front_passenger_door_open_status: Optional[bool] = Field(None, alias="frontPassengerDoorOpenStatus")
    front_passenger_door_window_status: Optional[bool] = Field(
        None, alias="frontPassengerDoorWindowStatus"
    )
    front_passenger_seat_heater: Optional[bool] = Field(None, alias="frontPassengerSeatHeater")
    front_passenger_seat_ventilation: Optional[bool] = Field(None, alias="frontPassengerSeatVentilation")
    fuel_level_available: Optional[bool] = Field(None, alias="fuelLevelAvailable")
    fuel_range_available: Optional[bool] = Field(None, alias="fuelRangeAvailable")
    guest_driver: Optional[bool] = Field(None, alias="guestDriver")
    hazard_capable: Optional[bool] = Field(None, alias="hazardCapable")
    horn_capable: Optional[bool] = Field(None, alias="hornCapable")
    hybrid_pulse: Optional[bool] = Field(None, alias="hybridPulse")
    hydrogen_pulse: Optional[bool] = Field(None, alias="hydrogenPulse")
    last_parked_capable: Optional[bool] = Field(None, alias="lastParkedCapable")
    light_status: Optional[bool] = Field(None, alias="lightStatus")
    lights_capable: Optional[bool] = Field(None, alias="lightsCapable")
    manual_rear_windows: Optional[bool] = Field(None, alias="manualRearWindows")
    mirror_heater: Optional[bool] = Field(None, alias="mirrorHeater")
    moonroof: Optional[bool] = Field(None, alias="moonroof")
    next_charge: Optional[bool] = Field(None, alias="nextCharge")
    power_tailgate_capable: Optional[bool] = Field(None, alias="powerTailgateCapable")
    power_windows_capable: Optional[bool] = Field(None, alias="powerWindowsCapable")
    rear_defogger: Optional[bool] = Field(None, alias="rearDefogger")
    rear_driver_door_lock_status: Optional[bool] = Field(None, alias="rearDriverDoorLockStatus")
    rear_driver_door_open_status: Optional[bool] = Field(None, alias="rearDriverDoorOpenStatus")
    rear_driver_door_window_status: Optional[bool] = Field(None, alias="rearDriverDoorWindowStatus")
    rear_driver_seat_heater: Optional[bool] = Field(None, alias="rearDriverSeatHeater")
    rear_driver_seat_ventilation: Optional[bool] = Field(None, alias="rearDriverSeatVentilation")
    rear_hatch_rear_window: Optional[bool] = Field(None, alias="rearHatchRearWindow")
    rear_passenger_door_lock_status: Optional[bool] = Field(None, alias="rearPassengerDoorLockStatus")
    rear_passenger_door_open_status: Optional[bool] = Field(None, alias="rearPassengerDoorOpenStatus")
    rear_passenger_door_window_status: Optional[bool] = Field(
        None, alias="rearPassengerDoorWindowStatus"
    )
    rear_passenger_seat_heater: Optional[bool] = Field(None, alias="rearPassengerSeatHeater")
    rear_passenger_seat_ventilation: Optional[bool] = Field(None, alias="rearPassengerSeatVentilation")
    remote_econnect_capable: Optional[bool] = Field(None, alias="remoteEConnectCapable")
    remote_engine_start_stop: Optional[bool] = Field(None, alias="remoteEngineStartStop")
    smart_key_status: Optional[bool] = Field(None, alias="smartKeyStatus")
    steering_heater: Optional[bool] = Field(None, alias="steeringHeater")
    stellantis_climate_capable: Optional[bool] = Field(None, alias="stellantisClimateCapable")
    stellantis_vehicle_status_capable: Optional[bool] = Field(
        None, alias="stellantisVehicleStatusCapable"
    )
    sunroof: Optional[bool] = Field(None, alias="sunroof")
    telemetry_capable: Optional[bool] = Field(None, alias="telemetryCapable")
    trunk_lock_unlock_capable: Optional[bool] = Field(None, alias="trunkLockUnlockCapable")
    try_and_play: Optional[bool] = Field(None, alias="tryAndPlay")
    vehicle_diagnostic_capable: Optional[bool] = Field(None, alias="vehicleDiagnosticCapable")
    vehicle_finder: Optional[bool] = Field(None, alias="vehicleFinder")
    vehicle_status: Optional[bool] = Field(None, alias="vehicleStatus")
    we_hybrid_capable: Optional[bool] = Field(None, alias="weHybridCapable")
    weekly_charge: Optional[bool] = Field(None, alias="weeklyCharge")


class _LinksModel(CustomBaseModel):
    body: Optional[str] = None  # TODO unsure what this returns
    button_text: Optional[str] = Field(None, alias="buttonText")
    image_url: Optional[str] = Field(alias="imageUrl", default=None)
    link: Optional[str] = None
    name: Optional[str] = None


class _DcmModel(CustomBaseModel):  # Data connection model
    country_code: Optional[str] = Field(alias="countryCode", default=None)
    destination: Optional[str] = Field(None, alias="dcmDestination")
    grade: Optional[str] = Field(None, alias="dcmGrade")
    car_model_year: Optional[str] = Field(None, alias="dcmModelYear")
    supplier: Optional[str] = Field(None, alias="dcmSupplier")
    supplier_name: Optional[str] = Field(alias="dcmSupplierName", default=None)
    euicc_id: Optional[str] = Field(None, alias="euiccid")
    hardware_type: Optional[str] = Field(None, alias="hardwareType")
    vehicle_unit_terminal_number: Optional[str] = Field(None, alias="vehicleUnitTerminalNumber")


class _HeadUnitModel(CustomBaseModel):
    description: Optional[Any] = Field(None, alias="huDescription")  # TODO unsure what this returns
    generation: Optional[Any] = Field(None, alias="huGeneration")  # TODO unsure what this returns
    version: Optional[Any] = Field(None, alias="huVersion")  # TODO unsure what this returns
    mobile_platform_code: Optional[Any] = Field(
        None, alias="mobilePlatformCode"
    )  # TODO unsure what this returns
    multimedia_type: Optional[Any] = Field(None, alias="multimediaType")  # TODO unsure what this returns


class _SubscriptionsModel(CustomBaseModel):
    auto_renew: Optional[bool] = Field(None, alias="autoRenew")
    category: Optional[str] = None
    components: Optional[Any] = None  # TODO unsure what this returns
    consolidated_goodwill_ids: Optional[List[Any]] = Field(
        None, alias="consolidatedGoodwillIds"
    )  # TODO unsure what this returns
    consolidated_product_ids: Optional[List[Any]] = Field(
        None, alias="consolidatedProductIds"
    )  # TODO unsure what this returns
    display_procuct_name: Optional[str] = Field(None, alias="displayProductName")
    display_term: Optional[str] = Field(None, alias="displayTerm")
    future_cancel: Optional[bool] = Field(None, alias="futureCancel")
    good_will_issued_for: Optional[Any] = Field(
        None, alias="goodwillIssuedFor"
    )  # TODO unsure what this returns
    product_code: Optional[str] = Field(None, alias="productCode")
    product_description: Optional[str] = Field(None, alias="productDescription")
    product_line: Optional[str] = Field(None, alias="productLine")
    product_name: Optional[str] = Field(None, alias="productName")
    procut_type: Optional[Any] = Field(None, alias="productType")
    renewable: Optional[bool] = None
    status: Optional[str] = None
    subscription_end_date: Optional[date] = Field(None, alias="subscriptionEndDate")
    subscription_id: Optional[str] = Field(None, alias="subscriptionID")
    subscription_next_billing_date: Optional[Any] = Field(
        None, alias="subscriptionNextBillingDate",
    )  # TODO unsure what this returns
    subscription_remaining_days: Optional[int] = Field(None, alias="subscriptionRemainingDays")
    subscription_remaining_term: Optional[Any] = Field(
        None, alias="subscriptionRemainingTerm",
    )  # TODO unsure what this returns
    subscription_start_date: Optional[date] = Field(None, alias="subscriptionStartDate")
    subscription_term: Optional[str] = Field(None, alias="subscriptionTerm")
    term: Optional[int] = None
    term_unit: Optional[str] = Field(None, alias="termUnit")
    type: Optional[str] = None


class _RemoteServiceCapabilitiesModel(CustomBaseModel):
    acsetting_enabled: Optional[bool] = Field(None, alias="acsettingEnabled")
    allow_hvac_override_capable: Optional[bool] = Field(None, alias="allowHvacOverrideCapable")
    dlock_unlock_capable: Optional[bool] = Field(None, alias="dlockUnlockCapable")
    estart_enabled: Optional[bool] = Field(None, alias="estartEnabled")
    estart_stop_capable: Optional[bool] = Field(None, alias="estartStopCapable")
    estop_enabled: Optional[bool] = Field(None, alias="estopEnabled")
    guest_driver_capable: Optional[bool] = Field(None, alias="guestDriverCapable")
    hazard_capable: Optional[bool] = Field(None, alias="hazardCapable")
    head_light_capable: Optional[bool] = Field(None, alias="headLightCapable")
    moon_roof_capable: Optional[bool] = Field(None, alias="moonRoofCapable")
    power_window_capable: Optional[bool] = Field(None, alias="powerWindowCapable")
    steering_wheel_heater_capable: Optional[bool] = Field(None, alias="steeringWheelHeaterCapable")
    trunk_capable: Optional[bool] = Field(None, alias="trunkCapable")
    vehicle_finder_capable: Optional[bool] = Field(None, alias="vehicleFinderCapable")
    ventilator_capable: Optional[bool] = Field(None, alias="ventilatorCapable")


class _DataConsentModel(CustomBaseModel):
    can_300: Optional[bool] = Field(None, alias="can300")
    dealer_contact: Optional[bool] = Field(None, alias="dealerContact")
    service_connect: Optional[bool] = Field(None, alias="serviceConnect")
    ubi: Optional[bool] = Field(None, alias="ubi")


class _FeaturesModel(CustomBaseModel):
    ach_payment: Optional[bool] = Field(None, alias="achPayment")
    add_service_record: Optional[bool] = Field(None, alias="addServiceRecord")
    auto_drive: Optional[bool] = Field(None, alias="autoDrive")
    cerence: Optional[bool] = Field(None, alias="cerence")
    charging_station: Optional[bool] = Field(None, alias="chargingStation")
    climate_start_engine: Optional[bool] = Field(None, alias="climateStartEngine")
    collision_assistance: Optional[bool] = Field(None, alias="collisionAssistance")
    connected_card: Optional[bool] = Field(None, alias="connectedCard")
    connected_insurance: Optional[bool] = Field(None, alias="connectedInsurance")
    connected_support: Optional[bool] = Field(None, alias="connectedSupport")
    crash_notification: Optional[bool] = Field(None, alias="crashNotification")
    critical_alert: Optional[bool] = Field(None, alias="criticalAlert")
    dashboard_lights: Optional[bool] = Field(None, alias="dashboardLights")
    dealer_appointment: Optional[bool] = Field(None, alias="dealerAppointment")
    digital_key: Optional[bool] = Field(None, alias="digitalKey")
    door_lock_capable: Optional[bool] = Field(None, alias="doorLockCapable")
    drive_pulse: Optional[bool] = Field(None, alias="drivePulse")
    driver_companion: Optional[bool] = Field(None, alias="driverCompanion")
    driver_score: Optional[bool] = Field(None, alias="driverScore")
    dtc_access: Optional[bool] = Field(None, alias="dtcAccess")
    dynamic_navi: Optional[bool] = Field(None, alias="dynamicNavi")
    eco_history: Optional[bool] = Field(None, alias="ecoHistory")
    eco_ranking: Optional[bool] = Field(None, alias="ecoRanking")
    electric_pulse: Optional[bool] = Field(None, alias="electricPulse")
    emergency_assist: Optional[bool] = Field(None, alias="emergencyAssist")
    enhanced_security_system: Optional[bool] = Field(None, alias="enhancedSecuritySystem")
    ev_charge_station: Optional[bool] = Field(None, alias="evChargeStation")
    ev_remote_services: Optional[bool] = Field(None, alias="evRemoteServices")
    ev_vehicle_status: Optional[bool] = Field(None, alias="evVehicleStatus")
    financial_services: Optional[bool] = Field(None, alias="financialServices")
    flex_rental: Optional[bool] = Field(None, alias="flexRental")
    h2_fuel_station: Optional[bool] = Field(None, alias="h2FuelStation")
    home_charge: Optional[bool] = Field(None, alias="homeCharge")
    how_to_videos: Optional[bool] = Field(None, alias="howToVideos")
    hybrid_pulse: Optional[bool] = Field(None, alias="hybridPulse")
    hydrogen_pulse: Optional[bool] = Field(None, alias="hydrogenPulse")
    important_message: Optional[bool] = Field(None, alias="importantMessage")
    insurance: Optional[bool] = Field(None, alias="insurance")
    last_parked: Optional[bool] = Field(None, alias="lastParked")
    lcfs: Optional[bool] = Field(None, alias="lcfs")
    linked_accounts: Optional[bool] = Field(None, alias="linkedAccounts")
    maintenance_timeline: Optional[bool] = Field(None, alias="maintenanceTimeline")
    marketing_card: Optional[bool] = Field(None, alias="marketingCard")
    marketing_consent: Optional[bool] = Field(None, alias="marketingConsent")
    master_consent_editable: Optional[bool] = Field(None, alias="masterConsentEditable")
    my_destination: Optional[bool] = Field(None, alias="myDestination")
    owners_manual: Optional[bool] = Field(None, alias="ownersManual")
    paid_product: Optional[bool] = Field(None, alias="paidProduct")
    parked_vehicle_locator: Optional[bool] = Field(None, alias="parkedVehicleLocator")
    parking: Optional[bool] = Field(None, alias="parking")
    parking_notes: Optional[bool] = Field(None, alias="parkingNotes")
    personalized_settings: Optional[bool] = Field(None, alias="personalizedSettings")
    privacy: Optional[bool] = Field(None, alias="privacy")
    recent_trip: Optional[bool] = Field(None, alias="recentTrip")
    remote_dtc: Optional[bool] = Field(None, alias="remoteDtc")
    remote_parking: Optional[bool] = Field(None, alias="remoteParking")
    remote_service: Optional[bool] = Field(None, alias="remoteService")
    roadside_assistance: Optional[bool] = Field(None, alias="roadsideAssistance")
    safety_recall: Optional[bool] = Field(None, alias="safetyRecall")
    schedule_maintenance: Optional[bool] = Field(None, alias="scheduleMaintenance")
    service_history: Optional[bool] = Field(None, alias="serviceHistory")
    shop_genuine_parts: Optional[bool] = Field(None, alias="shopGenuineParts")
    smart_charging: Optional[bool] = Field(None, alias="smartCharging")
    ssa_download: Optional[bool] = Field(None, alias="ssaDownload")
    sxm_radio: Optional[bool] = Field(None, alias="sxmRadio")
    telemetry: Optional[bool] = Field(None, alias="telemetry")
    tff: Optional[bool] = Field(None, alias="tff")
    tire_pressure: Optional[bool] = Field(None, alias="tirePressure")
    v1g: Optional[bool] = Field(None, alias="v1g")
    va_setting: Optional[bool] = Field(None, alias="vaSetting")
    vehicle_diagnostic: Optional[bool] = Field(None, alias="vehicleDiagnostic")
    vehicle_health_report: Optional[bool] = Field(None, alias="vehicleHealthReport")
    vehicle_specifications: Optional[bool] = Field(None, alias="vehicleSpecifications")
    vehicle_status: Optional[bool] = Field(None, alias="vehicleStatus")
    we_hybrid: Optional[bool] = Field(None, alias="weHybrid")
    wifi: Optional[bool] = Field(None, alias="wifi")
    xcapp: Optional[bool] = Field(None, alias="xcapp")


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

    alerts: Optional[List[Any]] = None  # TODO unsure what this returns
    asi_code: Optional[str] = Field(None, alias="asiCode")
    brand: Optional[str] = None
    capabilities: Optional[List[_CapabilitiesModel]] = None
    car_line_name: Optional[str] = Field(None, alias="carlineName")
    color: Optional[str] = None
    commercial_rental: Optional[bool] = Field(None, alias="commercialRental")
    contract_id: Optional[str] = Field(None, alias="contractId")
    cts_links: Optional[_LinksModel] = Field(None, alias="ctsLinks")
    data_consent: Optional[_DataConsentModel] = Field(None, alias="dataConsent")
    date_of_first_use: Optional[date] = Field(None, alias="dateOfFirstUse")
    dcm: Optional[_DcmModel] = None
    dcm_active: Optional[bool] = Field(None, alias="dcmActive")
    dcms: Optional[Any] = None  # TODO unsure what this returns
    display_model_description: Optional[str] = Field(None, alias="displayModelDescription")
    display_subscriptions: Optional[List[Dict[str, str]]] = Field(None, alias="displaySubscriptions")
    electrical_platform_code: Optional[str] = Field(alias="electricalPlatformCode", default=None)
    emergency_contact: Optional[Any] = Field(
        None, alias="emergencyContact"
    )  # TODO unsure what this returns
    ev_vehicle: Optional[bool] = Field(None, alias="evVehicle")
    extended_capabilities: Optional[_ExtendedCapabilitiesModel] = Field(
        None, alias="extendedCapabilities"
    )
    external_subscriptions: Optional[Any] = Field(None, alias="externalSubscriptions")
    family_sharing: Optional[bool] = Field(None, alias="familySharing")
    faq_url: Optional[str] = Field(None, alias="faqUrl")
    features: Optional[_FeaturesModel] = None
    fleet_ind: Optional[Any] = Field(None, alias="fleetInd")  # TODO unsure what this returns
    fuel_type: Optional[str] = Field(alias="fuelType", default=None)
    generation: Optional[str] = None
    head_unit: Optional[_HeadUnitModel] = Field(None, alias="headUnit")
    hw_type: Optional[Any] = Field(None, alias="hwType")  # TODO unsure what this returns
    image: Optional[str] = None
    imei: Optional[str] = None
    katashiki_code: Optional[str] = Field(None, alias="katashikiCode")
    manufactured_date: Optional[date] = Field(None, alias="manufacturedDate")
    manufactured_code: Optional[str] = Field(None, alias="manufacturerCode")
    car_model_code: Optional[str] = Field(None, alias="modelCode")
    car_model_description: Optional[str] = Field(None, alias="modelDescription")
    car_model_name: Optional[str] = Field(None, alias="modelName")
    car_model_year: Optional[str] = Field(None, alias="modelYear")
    nickname: Optional[str] = Field(alias="nickName", default=None)
    non_cvt_vehicle: Optional[bool] = Field(None, alias="nonCvtVehicle")
    old_imei: Optional[Any] = Field(None, alias="oldImei")  # TODO unsure what this returns
    owner: Optional[bool] = None
    personalized_settings: Optional[_LinksModel] = Field(
        None, alias="personalizedSettings"
    )  # TODO unsure what this returns
    preferred: Optional[bool] = None
    primary_subscriber: Optional[bool] = Field(None, alias="primarySubscriber")
    region: Optional[str] = None
    registration_number: Optional[str] = Field(None, alias="registrationNumber")
    remote_display: Optional[Any] = Field(None, alias="remoteDisplay")  # TODO unsure what this returns
    remote_service_capabilities: Optional[_RemoteServiceCapabilitiesModel] = Field(
        None, alias="remoteServiceCapabilities"
    )
    remote_service_exceptions: Optional[List[Any]] = Field(
        None, alias="remoteServicesExceptions"
    )  # TODO unsure what this returns
    remote_subscription_exists: Optional[bool] = Field(None, alias="remoteSubscriptionExists")
    remote_subscription_status: Optional[str] = Field(None, alias="remoteSubscriptionStatus")
    remote_user: Optional[bool] = Field(None, alias="remoteUser")
    remote_user_guid: Optional[Union[UUID, str]] = Field(alias="remoteUserGuid", default=None)
    service_connect_status: Optional[Any] = Field(
        None, alias="serviceConnectStatus"
    )  # TODO unsure what this returns
    services: Optional[List[Any]] = None  # TODO unsure what this returns
    shop_genuine_parts_url: Optional[str] = Field(None, alias="shopGenuinePartsUrl")
    status: Optional[str] = None
    stock_pic_reference: Optional[str] = Field(None, alias="stockPicReference")
    subscriber_guid: Optional[UUID] = Field(None, alias="subscriberGuid")
    subscription_expiration_status: Optional[bool] = Field(None, alias="subscriptionExpirationStatus")
    subscription_status: Optional[str] = Field(None, alias="subscriptionStatus")
    subscriptions: Optional[List[_SubscriptionsModel]] = None
    suffix_code: Optional[Any] = Field(None, alias="suffixCode")
    svl_satus: Optional[bool] = Field(None, alias="svlStatus")
    tff_links: Optional[_LinksModel] = Field(None, alias="tffLinks")
    transmission_type: Optional[str] = Field(None, alias="transmissionType")
    vehicle_capabilities: Optional[List[Any]] = Field(None, alias="vehicleCapabilities")
    vehicle_data_consents: Optional[Any] = Field(None, alias="vehicleDataConsents")
    vin: Optional[str] = None


class VehiclesResponseModel(StatusModel):
    r"""Model representing a vehicles response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[List[VehicleGuidModel]], optional): The vehicles payload. \n
            Defaults to None.

    """

    payload: Optional[List[VehicleGuidModel]] = None
