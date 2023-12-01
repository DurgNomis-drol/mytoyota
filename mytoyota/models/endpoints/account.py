"""Toyota Connected Services API - Account Models."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class _TermsActivityModel(BaseModel):
    time_stamp: datetime = Field(alias="timeStamp")
    version: str


class _AdditionalAttributesModel(BaseModel):
    is_terms_accepted: bool = Field(alias="isTermsAccepted")
    terms_activity: List[_TermsActivityModel] = Field("termsActivity")


class _EmailModel(BaseModel):
    email_address: str = Field(alias="emailAddress")
    email_type: str = Field(alias="emailType")
    email_verified: bool = Field(alias="emailVerified")
    verification_date: datetime = Field(alias="verificationDate")


class _PhoneNumberModel(BaseModel):
    country_code: int = Field(alias="countryCode")
    phone_number: int = Field(alias="phoneNumber")
    phone_verified: bool = Field(alias="phoneVerified")
    verification_date: datetime = Field("verificationDate")


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


class AccountModel(BaseModel):
    """Model representing an account.

    Attributes
    ----------
        customer (_CustomerModel): The customer associated with the account.

    """

    customer: _CustomerModel


class AccountResponseModel(StatusModel):
    """Model representing an account response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[AccountModel], optional): The account payload. Defaults to None.

    """

    payload: Optional[AccountModel] = None
