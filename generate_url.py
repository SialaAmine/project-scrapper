from get_url import get_url
from get_url import SearchRequest
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import asyncio
from datetime import datetime
from model import Request, SearchRequest

async def Setup_params(base_url: str, params: Request):
    """Modify the base URL with parameters from the Request object.
    
    Args:
        base_url: The original URL obtained from get_url function
        params: Request object containing checkin, checkout, adults, children, and rooms
        
    Returns:
        Modified URL with updated parameters
    """
    # Check if base_url is a valid URL
    if base_url == "No matching hotel found" or not base_url:
        # Return a default URL or handle the error case
        return "No matching hotel found"
    
    checkin = datetime.strptime(params.checkin, "%Y-%m-%d")
    checkout = datetime.strptime(params.checkout, "%Y-%m-%d")

    # Calculate the difference in days
    los = (checkout - checkin).days
    # Parse the base URL
    parsed_url = urlparse(base_url)
    # Get the query parameters
    query_params = parse_qs(parsed_url.query)
    # Update the parameters with values from the Request object
    query_params['checkIn'] = [params.checkin]
    query_params['checkOut'] = [params.checkout]
    query_params['rooms'] = [str(params.rooms)]
    query_params['adults'] = [str(params.adults)]
    query_params['children'] = [str(params.children)]
    query_params['los'] = [str(los)]
    
    # Convert the query parameters back to a string
    # Note: parse_qs creates lists for each parameter, so we need to join them
    new_query = urlencode(query_params, doseq=True)
    
    # Create a new parsed URL with the updated query string
    new_parsed_url = parsed_url._replace(query=new_query)
    print("new parsed url :",new_parsed_url)
    
    # Convert the parsed URL back to a string
    final_url = urlunparse(new_parsed_url)
    
    return final_url

async def generate_url(request: Request):
    search_request = SearchRequest(
        destination=request.destination,
        location=request.location
    )
    base_url = await get_url(search_request)
    if base_url is None or base_url == "No matching hotel found":
        return "No matching hotel found"
    final_url = await Setup_params(base_url, request)
    print("final url :",final_url)
    return final_url


if __name__ == "__main__":
    # Example usage
    request = Request(
        destination = "JAZ Tour Khalef",
        location = "Avenue 14 Janvier, Sousse, Sousse, Tunisie, 4051",
        checkin = "2025-06-18",
        checkout = "2025-06-21",
        adults = 4,
        children = 2,
        rooms = 2
    )
    gurl = asyncio.run(generate_url(request))  
    if gurl:
        print(f"Found matching hotel URL: {gurl}")
    else:
        print("No matching hotel found")