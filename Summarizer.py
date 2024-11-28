import asyncio
from playwright.async_api import async_playwright 
import config;
import google.generativeai as genai

url = "https://www.google.com/maps/place/Marhaba+Mahal/@31.4474486,73.1268467,14z/data=!4m6!3m5!1s0x39226f0e91b3eef7:0x4d038343dd7f430b!8m2!3d31.4521504!4d73.154186!16s%2Fg%2F11g8q8m0kg?entry=ttu&g_ep=EgoyMDI0MTEyNC4xIKXMDSoASAFQAw%3D%3D"

async def scrape_reviews(url):
    async with async_playwright() as p:  # Use async context manager
        reviews = []
        browser = await p.chromium.launch(headless=False)  # Launch browser asynchronously
        page = await browser.new_page()  # Open a new page asynchronously
        await page.goto(url)  # Navigate to the URL asynchronously

        # Your scraping logic goes here. For now, let's print the title.
        title = await page.title()
        print(f"Page Title: {title}")

        await page.wait_for_selector('.w8nwRe ')
        more_buttons = await page.query_selector_all('.w8nwRe')
        if more_buttons is not None:
            for button in more_buttons:
                await button.click()
                await page.wait_for_timeout(500)  # Wait for reviews to load
        await page.wait_for_selector('.jftiEf')
        elements = await page.query_selector_all('.jftiEf')
        for element in elements:
            await page.wait_for_selector('.MyEned')
            snippet = await element.query_selector('.MyEned')
            text = await page.evaluate("selected => selected.textContent", snippet)
            print(text)
            reviews.append(text)
        # Close the browser after scraping
        await browser.close()




def Gemini(reviews):

    genai.configure(config.GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = 'I have some resturant reviews I want you to tell me about the resturant based on those reviews'
    for review in reviews:
        prompt+= "\n" + review
        print(prompt)
    response = model.generate_content(prompt)
    print(response.text)

# Run the asynchronous function with asyncio
asyncio.run(scrape_reviews(url))
