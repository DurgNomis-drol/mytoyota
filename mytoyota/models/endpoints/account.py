"""Toyota Connected Services API - Account Models."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic.v1 import Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.models import CustomBaseModel


class _TermsActivityModel(CustomBaseModel):
    time_stamp: Optional[datetime] = Field(alias="timeStamp")
    version: Optional[str]


class _AdditionalAttributesModel(CustomBaseModel):
    is_terms_accepted: Optional[bool] = Field(alias="isTermsAccepted")
    terms_activity: Optional[List[_TermsActivityModel]] = Field("termsActivity")


class _EmailModel(CustomBaseModel):
    email_address: Optional[str] = Field(alias="emailAddress")
    email_type: Optional[str] = Field(alias="emailType")
    email_verified: Optional[bool] = Field(alias="emailVerified")
    verification_date: Optional[datetime] = Field(alias="verificationDate")


class _PhoneNumberModel(CustomBaseModel):
    country_code: Optional[int] = Field(alias="countryCode")
    phone_number: Optional[int] = Field(alias="phoneNumber")
    phone_verified: Optional[bool] = Field(alias="phoneVerified")
    verification_date: Optional[datetime] = Field("verificationDate")


class _CustomerModel(CustomBaseModel):
    account_status: Optional[str] = Field(alias="accountStatus")
    additional_attributes: Optional[_AdditionalAttributesModel] = Field(
        alias="additionalAttributes"
    )
    create_date: Optional[datetime] = Field(alias="createDate")
    create_source: Optional[str] = Field(alias="createSource")
    customer_type: Optional[str] = Field(alias="customerType")
    emails: Optional[List[_EmailModel]]
    first_name: Optional[str] = Field(alias="firstName")
    forge_rock_id: Optional[UUID] = Field(alias="forgerockId")
    guid: Optional[UUID]
    is_cp_migrated: Optional[bool] = Field(alias="isCpMigrated")
    lastname: Optional[str] = Field(alias="lastName")
    last_update_date: Optional[datetime] = Field("lastUpdateDate")
    last_update_source: Optional[str] = Field("lastUpdateSource")
    phone_numbers: Optional[List[_PhoneNumberModel]] = Field(alias="phoneNumbers")
    preferred_language: Optional[str] = Field(alias="preferredLanguage")
    signup_type: Optional[str] = Field(alias="signupType")
    ui_language: Optional[str] = Field(alias="uiLanguage")


class AccountModel(CustomBaseModel):
    """Model representing an account.

    Attributes
    ----------
        customer (_CustomerModel): The customer associated with the account.

    """

    customer: Optional[_CustomerModel]


class AccountResponseModel(StatusModel):
    """Model representing an account response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[AccountModel], optional): The account payload. Defaults to None.

    """

    payload: Optional[AccountModel] = None
