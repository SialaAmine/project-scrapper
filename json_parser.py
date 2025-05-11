import json
import asyncio
from model import HotelItem, AddressModel, ReviewsModel, TaxModel, PricingModel
def parse_json(json_string):
    try:
        parsed_json = json.loads(json_string)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = file.read()
            return parse_json(json_data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
async def generate_output(json_data):
    # Generate the output based on the JSON data
    if json_data:
        print("JSON data loaded successfully!")
        print(f"Type of json_data: {type(json_data)}")
        # Create nested models first
        tax_model = TaxModel(
            title=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["taxesAndSurcharges"]["title"],
            taxesAndSurchargesList=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["taxesAndSurchargesList"],
            totaltax=json_data["tealium"]["tax"],
            tax=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["pricing"]["extraInfo"]["roomTaxAndFeePRPN"]
        )   
        pricing_model = PricingModel(
            price=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["pricing"]["displayPrice"],
            tax=tax_model,
            roomPricePerNightTaxExc=json_data["tealium"]["totalPriceTaxExc"],
            roomPricePerNightTaxInc=json_data["tealium"]["totalPriceTaxInc"],
            totalPriceTaxExc=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["pricing"]["extraInfo"]["totalPriceWithoutTaxAndFee"],
            totalPriceTaxInc=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["totalPrice"]["display"],
            totalPricePerNightTaxExc=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["perNightPrice"]["display"],
            totalPricePerNightTaxInc=json_data["roomGridData"]["masterRooms"][0]["rooms"][0]["inclusivePricePerNightWithoutExtraBed"]["display"]
        )    
        # Create the main HotelItem model
        hotel_item = HotelItem(
            website="www.agoda.com",
            hotelId=json_data["hotelId"],
            name=json_data["hotelInfo"]["name"],
            url="www.agoda.com" + json_data["searchbox"]["config"]["defaultSearchURL"],
            starRating=json_data["hotelInfo"]["starRating"]["value"],
            reviews=ReviewsModel(
                scoreText=json_data["reviews"]["scoreText"],
                score=json_data["reviews"]["score"],
                reviewsCount=json_data["reviews"]["reviewsCount"]
            ),
            address=AddressModel(
                countryId=json_data["hotelInfo"]["address"]["countryId"],
                full=json_data["hotelInfo"]["address"]["full"],
                cityName=json_data["hotelInfo"]["address"]["cityName"],
                cityId=json_data["hotelInfo"]["address"]["cityId"],
                countryName=json_data["hotelInfo"]["address"]["countryName"],
                areaName=json_data["hotelInfo"]["address"]["areaName"],
                address=json_data["hotelInfo"]["address"]["address"],
                postalCode=json_data["hotelInfo"]["address"]["postalCode"]
            ),
            mapParams=json_data["mapParams"]["latlng"],
            pricing=pricing_model,
            currencyCode=json_data["currencyInfo"]["code"],
            description=json_data["aboutHotel"]["hotelDesc"]["overview"]
        )
        if hotel_item:
            return hotel_item
            #export_data(hotel_item)
        else: return "no data found"
    else:
        print("Failed to load JSON data")
        return None
def export_data(json_data):
    # Write the model to a JSON file
        with open("hotelitem222.json", "w", encoding="utf-8") as f:
            # For Pydantic v1
            # json.dump(hotel_item.dict(), f, indent=2, ensure_ascii=False)
            # For Pydantic v2
            json.dump(json_data.model_dump(), f, indent=2, ensure_ascii=False)
# Example usage
if __name__ == "__main__":
    import asyncio
    async def main():
        # Replace with the actual path to your test-easy.json file
        file_path = "./test_easy.json"
        # Read and parse the JSON file
        json_data = read_json_file(file_path)
        # Now json_data variable contains the parsed JSON
        output = await generate_output(json_data)
        if output:
            export_data(output)
    # Run the async main function
    asyncio.run(main())



