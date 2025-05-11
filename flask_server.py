from flask import Flask, request, jsonify
import asyncio
from model import Request, HotelItem , PricingModel, ReviewsModel, AddressModel, TaxModel
from generate_url import generate_url
from get_json_data import capture_api_response
from json_parser import generate_output

app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def trigger_scraper():
    try:
        # Parse the JSON request data
        data = request.json
        scraper_request = Request(
            destination=data['destination'],
            location=data['location'],
            checkin=data['checkin'],
            checkout=data['checkout'],
            adults=data['adults'],
            children=data['children'],
            rooms=data['rooms']
        )
        
        # Run the async functions using asyncio
        async def process_request():
            gurl = await generate_url(scraper_request)
            if gurl == "No matching hotel found":
                return {"error": "No matching hotel found"}
            
            json_data = await capture_api_response(gurl)
            output = await generate_output(json_data)
            
            # Convert the Pydantic model to a dictionary before returning
            if isinstance(output, HotelItem):
                return {"result": output.model_dump()}  # For Pydantic v2
                # If using Pydantic v1, use: return {"result": output.dict()}
            
            return {"result": output}
        
        # Run the async function and get the result
        result = asyncio.run(process_request())
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)