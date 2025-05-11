from playwright.async_api import async_playwright
import logging
import asyncio
from fuzzywuzzy import fuzz
from typing import List, Optional
from model import SearchRequest
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class HotelItem:
    def __init__(self, name: str, location: str, url: str):
        self.name = name
        self.location = location
        self.url = url
    
    def __str__(self):
        return f"HotelItem(name='{self.name}', location='{self.location}', url='{self.url}')"

async def get_hotel_items(page) -> List[HotelItem]:
    """
    Extract hotel items from the search results page
    """
    logger.info("Extracting hotel items from search results...")
    
    # Get the first three hotel items
    hotel_items_elements = await page.locator('li[data-selenium="hotel-item"]').all()
    hotel_items_elements = hotel_items_elements[:3] if len(hotel_items_elements) > 3 else hotel_items_elements
    hotel_items = []
    
    for element in hotel_items_elements:
        try:
            # Get hotel name
            name_element = element.locator('h3[data-selenium="hotel-name"]')
            name = await name_element.inner_text() if await name_element.count() > 0 else ""
            
            # Get hotel location
            location_element = element.locator('button[data-selenium="area-city-text"] span')
            location = ""
            if await location_element.count() > 0:
                location_text = await location_element.inner_text()
                # Remove "- Voir sur la carte" part
                if " - " in location_text:
                    location = location_text.split(" - ")[0]
                else:
                    location = location_text
            
            # Get hotel URL
            url_element = element.locator('a[data-element-name="property-card-content"]')
            url = ""
            if await url_element.count() > 0:
                href = await url_element.get_attribute("href")
                if href:
                    url = f"https://www.agoda.com{href}"
            
            hotel_item = HotelItem(name=name, location=location, url=url)
            hotel_items.append(hotel_item)
            logger.info(f"Extracted hotel item: {hotel_item}")
            
        except Exception as e:
            logger.error(f"Error extracting hotel item: {e}")
    
    return hotel_items

def find_matching_hotel(search_request: SearchRequest, hotel_items: List[HotelItem]) -> Optional[str]:
    """
    Find the best matching hotel based on name and location similarity
    """
    logger.info(f"Finding matching hotel for: {search_request}")
    
    best_match = None
    highest_score = 0
    
    for item in hotel_items:
        # Calculate name similarity
        name_similarity = fuzz.ratio(search_request.destination.lower(), item.name.lower())
        
        # Calculate location similarity
        location_similarity = fuzz.partial_ratio(item.location.lower(), search_request.location.lower())
        
        # Calculate combined score (giving more weight to name similarity)
        combined_score = (name_similarity * 0.7) + (location_similarity * 0.3)
        
        logger.info(f"Similarity scores for {item.name}: name={name_similarity}, location={location_similarity}, combined={combined_score}")
        
        # If this is the best match so far, update our tracking variables
        if combined_score > highest_score:
            highest_score = combined_score
            best_match = item
    
    # Return the URL of the best match if the score is above a threshold, otherwise None
    if best_match and highest_score > 60:  # Threshold of 60%
        logger.info(f"Found matching hotel: {best_match}")
        return best_match.url
    else:
        logger.info("No matching hotel found")
        return None

async def get_url(search_request: SearchRequest):
    """
    Use Playwright to access the agooda.com website and get the url for the search
    """
    logger.info(f"Getting search url for: {search_request}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set to True for headless mode
        context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    viewport={"width": 1280, "height": 720}
)
        # Create a page
        page = await context.new_page()

        input_selector = 'input[data-selenium="textInput"]'
        search_button_selector = 'button[data-selenium="searchButton"]'
        suggestion_ignore_selector = 'div[id="screen-dimmer"]'

        try:
            # Navigate to the search page
            logger.info("Navigating to agooda.com homepage...")
            await page.goto("https://www.agoda.com/",timeout=60000)

            # Wait for the page to load
            logger.info("Waiting for page to load...")

            search_input = page.locator(input_selector)
            await search_input.fill(search_request.destination)
            logger.info("Filled search input")

            await asyncio.sleep(0.5)

            await page.keyboard.press("Escape")
            logger.info("Pressed Escape")
            await asyncio.sleep(0.5)

            search_button = page.locator(search_button_selector)
            await search_button.click()
            logger.info("Clicked search button")

            # Wait for the search results to load
            logger.info("Waiting for search results to load...")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(5)
            # Extract hotel items
            hotel_items = await get_hotel_items(page)
            
            # Find matching hotel
            matching_url = find_matching_hotel(search_request, hotel_items)
            
            return matching_url
            
        except Exception as e:
            logger.error(f"Error getting search url: {e}")
            raise e

if __name__ == "__main__":
    # Example usage
    search_request = SearchRequest(
        destination="Riadh Palms- Family & Couples only",
        location="Avenue 14 Janvier, Sousse, Sousse, Tunisie, 4039"
    )
    url = asyncio.run(get_url(search_request))
    
    if url:
        print(f"Found matching hotel URL: {url}")
    else:
        print("No matching hotel found")

