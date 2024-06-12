from bs4 import BeautifulSoup
import datetime, aiohttp, asyncio



class handler:
    def __init__(self, html, arguments: dict, data):
        self.HTML = html[1]
        self.ARGUMENTS = arguments
        self.DATA = data

    async def scrap(self) -> dict:
        results = {}
        html = BeautifulSoup(self.HTML, "html.parser")
        for x in self.get_all_news_pages(html):
            await asyncio.sleep(0.01)
            results[x[0]] = await self.scrap_all_news_pages(x[0], x[1])

        return results

    def get_all_news_pages(self, html) -> any: ## return a generator where have url of pages setted in news_options in meta
        for pages in self.DATA["news_options"]:
            yield (pages, self.DATA['url']+html.find("li", class_='bbc-zakhp8 e11sm0on2', string=pages).a['href'])
    

    async def scrap_all_news_pages(self, page: str, url: str) -> dict: ## start scrap from previous url of pages in news_option passed from get_all_news_pages

        scrapping_results = {}

        if self.ARGUMENTS.get('timeStamp') == "today":
            today_date = str(datetime.datetime.now().date())
            
            results = await self.core_request_handler(url)
            if results[1] == False:
                return False
            
            for content in BeautifulSoup(results[1], "html.parser").find_all("li", class_="bbc-t44f9r"):
                await asyncio.sleep(0.01)
                NEWS_DATE = content.find("div", class_="promo-text").time['datetime']
                if NEWS_DATE == today_date:
                    ANCHOR_CONTENT = content.find("div", class_="promo-text").find("a", class_="focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0")
                    NEWS_TEXT = ANCHOR_CONTENT.text
                    NEWS_HREF = ANCHOR_CONTENT['href']

                    if NEWS_TEXT not in scrapping_results.keys():
                        scrapping_results[NEWS_TEXT] = NEWS_HREF


        return scrapping_results
    
    async def core_request_handler(self, url: str) -> str: ## return the html content to scrap_all_news_page scrap all content
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(4)) as request:
            async with request.get(url, headers=self.DATA.get('headers')) as html:
                await asyncio.sleep(0.3)
               
                if html.status in self.DATA.get('ok_http_code'):
                    return html.status, await html.text()
                
                else: return html.status, False

