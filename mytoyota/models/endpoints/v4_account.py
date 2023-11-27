from datetime import datetime
from typing import List, Union, Iterable, Tuple, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


def censor_sensitive_fields(args: Iterable[Tuple[Union[str, None], Any]],
                            replace: List[str]) -> str:
    return " ".join(repr(v) if a is None else f"{a}='*** CENSORED ***'" if a in replace else f"{a}={v!r}" for a, v in
                    args)


class _TermsActivityModel(BaseModel):
    time_stamp: datetime = Field(alias="timeStamp")
    version: str


class _AdditionalAttributesModel(BaseModel):
    is_terms_Accepted: bool = Field(alias="isTermsAccepted")
    terms_activity: List[_TermsActivityModel] = Field("termsActivity")


class _EmailModel(BaseModel):
    email_address: str = Field(alias="emailAddress")
    email_Type: str = Field(alias="emailType")
    email_verified: bool = Field(alias="emailVerified")
    verification_date: datetime = Field(alias="verificationDate")

    def __repr__(self):
        return censor_sensitive_fields(self.__repr_args__(), ["email_address"])


class _PhoneNumberModel(BaseModel):
    country_code: int = Field(alias="countryCode")
    phone_number: int = Field(alias="phoneNumber")
    phone_verified: bool = Field(alias="phoneVerified")
    verification_date: datetime = Field("verificationDate")

    @field_validator("phone_number")
    def censor_original_vin(cls, v):
        v = "POOP"
        return v


class _CustomerModel(BaseModel):
    account_status: str = Field(alias="accountStatus")
    additional_attributes: _AdditionalAttributesModel = Field(alias="additionalAttributes")
    create_date: datetime = Field(alias="createDate")
    create_source: str = Field(alias="createSource")
    customer_type: str = Field(alias="customerType")
    emails: List[_EmailModel]
    first_name: str = Field(alias="firstName")
    forge_rock_id: UUID = Field(alias="forgerockId")
    guid: UUID
    is_cp_migrated: bool = Field(alias="isCpMigrated")
    lastname: str = Field(alias="lastName")
    last_update_date: datetime = Field("lastUpdateDate")
    last_update_source: str = Field("lastUpdateSource")
    phone_numbers: List[_PhoneNumberModel] = Field(alias="phoneNumbers")
    preferred_language: str = Field(alias="preferredLanguage")
    signup_type: str = Field(alias="signupType")
    ui_language: str = Field(alias="uiLanguage")


class _PayloadModel(BaseModel):  # TODO common across all?
    customer: _CustomerModel


class _MessageModel(BaseModel):
    description: str
    response_code: str = Field(alias="responseCode")


class _StatusModel(BaseModel):
    messages: List[_MessageModel]


class V4AccountModel(BaseModel):
    payload: Union[_PayloadModel, None] = None
    status: _StatusModel


if __name__ == "__main__":
    data = {'payload': {'customer': {'accountStatus': 'active',
                                     'additionalAttributes': {'isTermsAccepted': True,
                                                              'termsActivity': [{'timeStamp': 1695059143310,
                                                                                 'version': 'TME_CP_GB_V7'},
                                                                                {'timeStamp': 1699214753709,
                                                                                 'version': 'TME_CP_GB_V8'}]},
                                     'createDate': 1670190933340,
                                     'createSource': 'TME_FR',
                                     'customerType': 'PERSON',
                                     'emails': [{'emailAddress': 'car@rebeccaodonnell.co.uk',
                                                 'emailType': 'forgerock',
                                                 'emailVerified': True,
                                                 'verificationDate': 1670190933340}],
                                     'firstName': 'Rebecca',
                                     'forgerockId': 'd95b0b58-3b3f-40e3-99ca-a3aa2a22a204',
                                     'guid': 'd95b0b58-3b3f-40e3-99ca-a3aa2a22a204',
                                     'isCpMigrated': False,
                                     'lastName': "O'Donnell",
                                     'lastUpdateDate': 1699214742826,
                                     'lastUpdateSource': 'CT_FR',
                                     'phoneNumbers': [{'countryCode': 44,
                                                       'phoneNumber': 7903093574,
                                                       'phoneType': 'MOBILE',
                                                       'phoneVerified': True,
                                                       'verificationDate': 1699214742826}],
                                     'preferredLanguage': 'en-GB',
                                     'signupType': 'regular',
                                     'uiLanguage': 'en-GB'}},
            'status': {'messages': [{'description': 'Customer Found',
                                     'responseCode': 'OCPR-0000'}]}}

    model = V4AccountModel(**data)
    print(model)
    print(model.payload.customer.phone_numbers)
