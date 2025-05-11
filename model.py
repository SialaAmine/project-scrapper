from pydantic import BaseModel

class SearchRequest(BaseModel):
    destination: str
    location: str
    
class  Request(BaseModel):
    destination: str
    location: str
    checkin: str
    checkout: str
    adults: int
    children: int = 0
    rooms: int = 1

class ReviewsModel(BaseModel):
    scoreText: str
    score: str
    reviewsCount: int


class AddressModel(BaseModel):
    countryId: int
    full: str
    cityName: str
    cityId: int
    countryName: str
    areaName: str
    address: str
    postalCode: str


class TaxModel(BaseModel):
    title: str
    taxesAndSurchargesList: list[str]
    totaltax: float
    tax: float


class PricingModel(BaseModel):
    price: float
    tax: TaxModel
    roomPricePerNightTaxExc: float
    roomPricePerNightTaxInc: float
    totalPriceTaxExc: float
    totalPriceTaxInc: float
    totalPricePerNightTaxExc: float
    totalPricePerNightTaxInc: float


class HotelItem(BaseModel):
    website: str
    hotelId: int
    name: str
    url: str
    starRating: float
    reviews: ReviewsModel
    address: AddressModel
    mapParams: list[float]
    pricing: PricingModel
    currencyCode: str
    description: str
