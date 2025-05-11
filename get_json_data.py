from playwright.async_api import async_playwright
import time
import asyncio
    
async def capture_api_response(url:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        # Create a page
        page = await context.new_page()

        # Store API responses
        api_responses = {}
        response_received = False

        async def handle_response(response):
            nonlocal response_received
            if "api/cronos/property/BelowFoldParams/GetSecondaryData" in response.url:
                print(f"Captured GetSecondaryData API response: {response.url}")
                try:
                    # Get response body as JSON
                    api_responses["GetSecondaryData"] = await response.json()
                    print("Successfully parsed JSON response")
                    print(f"Type of json_data: {type(api_responses['GetSecondaryData'])}")
                    
                    #with open("test_easy.json", "w", encoding="utf-8") as f:
                        #json.dump(api_responses["GetSecondaryData"], f, indent=2, ensure_ascii=False)
                    #print("Saved API response to test_easy.json")
                    response_received = True
                except Exception as e:
                    print(f"Error parsing response: {e}")
                    try:
                        # Try to get as text if JSON parsing fails
                        api_responses["GetSecondaryData_text"] = await response.text()
                        print("Saved response as text")
                        response_received = True
                    except:
                        print("Failed to get response text")

        # Listen for response events
        page.on("response", handle_response)

        # Add a timeout for page navigation
        try:
            # Navigate to the page with timeout
            print("Navigating to the hotel page...")
            await page.goto(url, timeout=30000)  # 30 second timeout
        except Exception as e:
            print(f"Navigation error: {e}")
            await browser.close()
            return None
        
        # Wait for a reasonable time or until we get the response
        print("Waiting for API calls...")
        max_wait = 60  # Maximum wait time in seconds
        start_time = time.time()
        
        while not response_received and time.time() - start_time < max_wait:
            await asyncio.sleep(1)
            print(".", end="", flush=True)
        
        print("\nDone waiting")
                
        # Close browser
        await browser.close()
        data = api_responses["GetSecondaryData"]
        # Return the captured data
        return data
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(capture_api_response("https://www.agoda.com/fr-fr/le-monaco-hotel-thalasso-h9626389/hotel/sousse-tn.html?countryId=56&finalPriceView=1&cid=-1&familyMode=false&adults=4&children=2&rooms=2&maxRooms=0&checkIn=2025-06-18&isCalendarCallout=false&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=EUR&isFreeOccSearch=false&los=3&searchrequestid=b0e3ace1-fd81-4ea4-8a6a-22ab740697ba&checkOut=2025-06-21"))
    