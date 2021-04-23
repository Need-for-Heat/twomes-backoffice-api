from typing import ClassVar, List, Optional

from pydantic import BaseModel, condecimal, conint, constr

from field import Datetime
from model import Account, Building


class HttpStatus(BaseModel):
    code: ClassVar[int]
    detail: str


class BadRequest(HttpStatus):
    code = 400


class Unauthorized(HttpStatus):
    code = 401


class Forbidden(HttpStatus):
    code = 403


class NotFound(HttpStatus):
    code = 404


class AccountLocation(BaseModel):
    longitude: condecimal(
        max_digits=Building.LOCATION_MAX_DIGITS,
        decimal_places=Building.LOCATION_DECIMAL_PLACES
    )
    latitude: condecimal(
        max_digits=Building.LOCATION_MAX_DIGITS,
        decimal_places=Building.LOCATION_DECIMAL_PLACES
    )


class AccountCreate(BaseModel):
    pseudonym: Optional[conint(ge=Account.PSEUDONYM_MIN, le=Account.PSEUDONYM_MAX)] = None
    location: Optional[AccountLocation] = None


class AccountItem(BaseModel):
    id: int
    pseudonym: int
    activation_token: str
    firebase_url: str


class AccountActivate(BaseModel):
    activation_token: str


class SessionToken(BaseModel):
    session_token: str


class AccountSession(SessionToken):
    pass


class DeviceSession(SessionToken):
    pass


class DeviceCreate(BaseModel):
    device_type: str
    proof_of_presence_id: constr(strip_whitespace=True, min_length=8, max_length=1024)


class DeviceVerify(BaseModel):
    proof_of_presence_id: constr(strip_whitespace=True, min_length=8, max_length=1024)


class DeviceTypeItem(BaseModel):
    name: str
    installation_manual_url: str

    class Config:
        orm_mode = True


class PropertyCompleteItem(BaseModel):
    id: int
    name: str
    unit: Optional[str]

    class Config:
        orm_mode = True


class DeviceTypeCompleteItem(BaseModel):
    id: int
    name: str
    installation_manual_url: str
    properties: List[PropertyCompleteItem]

    class Config:
        orm_mode = True


class DeviceItem(BaseModel):
    id: int
    device_type: DeviceTypeItem
    created_on: Datetime
    activated_on: Optional[Datetime]

    class Config:
        orm_mode = True


class DeviceItemMeasurementTime(DeviceItem):
    latest_measurement_timestamp: Optional[Datetime]

    class Config:
        orm_mode = True


class DeviceCompleteItem(BaseModel):
    id: int
    device_type: DeviceTypeCompleteItem
    proof_of_presence_id: str
    created_on: Datetime
    activated_on: Optional[Datetime]

    class Config:
        orm_mode = True


class Measurement(BaseModel):
    timestamp: Datetime
    value: str


class PropertyMeasurements(BaseModel):
    property_id: int
    measurements: List[Measurement]


class MeasurementsUpload(BaseModel):
    device_time: Datetime
    items: List[PropertyMeasurements]


class MeasurementsUploadResult(BaseModel):
    server_time: Datetime
    size: int