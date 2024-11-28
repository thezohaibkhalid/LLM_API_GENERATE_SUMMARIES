import asyncio
from playwright.async_api import async_playwright 
import config;
import google.generativeai as genai

url = "https://www.google.com/maps/place/Tahir+Hospital/@31.4501451,73.1071943,512m/data=!3m1!1e3!4m6!3m5!1s0x392269322cbab8ab:0x3ec4f002afe25152!8m2!3d31.4499063!4d73.1070017!16s%2Fg%2F11fj_bgcyh?entry=ttu&g_ep=EgoyMDI0MTEyNC4xIKXMDSoASAFQAw%3D%3D"
reviews = []
async def scrape_reviews(url):
    async with async_playwright() as p:  # Use async context manager
        
        browser = await p.chromium.launch(headless=False)  # Launch browser asynchronously
        page = await browser.new_page()  # Open a new page asynchronously
        await page.goto(url, timeout = 120000)  # Navigate to the URL asynchronously

        # Your scraping logic goes here. For now, let's print the title.
        title = await page.title()
        print(f"Page Title: {title}")

        await page.wait_for_selector('.w8nwRe ')
        more_buttons = await page.query_selector_all('.w8nwRe')
        if more_buttons is not None:
            for button in more_buttons:
                await button.click()
                await page.wait_for_timeout(1000)  # Wait for reviews to load
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

    genai.configure(api_key=config.GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = 'I colleceted some reviews about the place i was considering visiting. Can you summarize the reviews for me ?'
    for review in reviews:
        prompt+= "\n" + review
        print(prompt)
    response = model.generate_content(prompt)
    print("Text response is ")
    print(response.text)

# Run the asynchronous function with asyncio
asyncio.run(scrape_reviews(url))
Gemini(reviews)


