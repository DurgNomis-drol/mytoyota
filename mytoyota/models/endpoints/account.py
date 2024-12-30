"""Toyota Connected Services API - Account Models."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.models import CustomBaseModel


class _TermsActivityModel(CustomBaseModel):
    time_stamp: Optional[datetime] = Field(None, alias="timeStamp")
    version: Optional[str] = None


class _AdditionalAttributesModel(CustomBaseModel):
    is_terms_accepted: Optional[bool] = Field(None, alias="isTermsAccepted")
    terms_activity: Optional[List[_TermsActivityModel]] = Field("termsActivity")


class _EmailModel(CustomBaseModel):
    email_address: Optional[str] = Field(None, alias="emailAddress")
    email_type: Optional[str] = Field(None, alias="emailType")
    email_verified: Optional[bool] = Field(None, alias="emailVerified")
    verification_date: Optional[datetime] = Field(None, alias="verificationDate")


class _PhoneNumberModel(CustomBaseModel):
    country_code: Optional[int] = Field(None, alias="countryCode")
    phone_number: Optional[int] = Field(None, alias="phoneNumber")
    phone_verified: Optional[bool] = Field(None, alias="phoneVerified")
    verification_date: Optional[datetime] = Field("verificationDate")


class _CustomerModel(CustomBaseModel):
    account_status: Optional[str] = Field(None, alias="accountStatus")
    additional_attributes: Optional[_AdditionalAttributesModel] = Field(
        None, alias="additionalAttributes"
    )
    create_date: Optional[datetime] = Field(None, alias="createDate")
    create_source: Optional[str] = Field(None, alias="createSource")
    customer_type: Optional[str] = Field(None, alias="customerType")
    emails: Optional[List[_EmailModel]] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    forge_rock_id: Optional[UUID] = Field(None, alias="forgerockId")
    guid: Optional[UUID] = None
    is_cp_migrated: Optional[bool] = Field(None, alias="isCpMigrated")
    lastname: Optional[str] = Field(None, alias="lastName")
    last_update_date: Optional[datetime] = Field("lastUpdateDate")
    last_update_source: Optional[str] = Field("lastUpdateSource")
    phone_numbers: Optional[List[_PhoneNumberModel]] = Field(None, alias="phoneNumbers")
    preferred_language: Optional[str] = Field(None, alias="preferredLanguage")
    signup_type: Optional[str] = Field(None, alias="signupType")
    ui_language: Optional[str] = Field(None, alias="uiLanguage")


class AccountModel(CustomBaseModel):
    """Model representing an account.

    Attributes
    ----------
        customer (_CustomerModel): The customer associated with the account.

    """

    customer: Optional[_CustomerModel] = None


class AccountResponseModel(StatusModel):
    """Model representing an account response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[AccountModel], optional): The account payload. Defaults to None.

    """

    payload: Optional[AccountModel] = None
