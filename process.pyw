import asyncio, aiohttp
import json
from websites import *

class core:
    def __init__(self, module_name):
        self.PATH = "websites\\configurations\\meta.json"
        self.MODULE_KEY = module_name
        self.MODULE_KEYS = ["bbc"]
        self.MODULE_SUB_KEYS = ["news_options", "api_url", "cloudflare", "headers", "method"]

    async def startup_code(self) -> bool:
        with open(self.PATH, "r", encoding='utf-8') as r:
            self.data = await self.check_meta_content(r)

            if self.data['status'] == False:
                return self.data, False
            
            self.data = self.data['content']

        brute_content = await self.request_module_handler()

        if brute_content[1] == False:
            return brute_content

        match self.MODULE_KEY:
            case "bbc":
                print("bbc")

            case _:
                return self.MODULE_KEY, False
    


    async def request_module_handler(self) -> dict:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(4)) as request:
            if self.data['method'] == 'get':
                async with request.get(self.data.get('api_url'), data=self.data.get('payload'), headers=self.data.get('headers')) as html:
                    await asyncio.sleep(0.1)
                    if html.status in self.data.get('ok_http_code'):
                        return html.status, await html.text()
                    else: return html.status, False

            else:
                async with request.post(self.data.get('api_url'), data=self.data.get('payload'), headers=self.data.get('headers')) as html:
                    await asyncio.sleep(0.1)
                    if html.status in self.data.get('ok_http_code'):
                        return html.status, await html.text()
                    
                    else: return html.status, False           

    async def check_meta_content(self, data) -> dict:
        try:
            data = json.load(data)

            
            checklist_results = {
                "status": False,
                "MissedKeys": [],
                "MissedSubKeys": [],
                "content": data[self.MODULE_KEY]
            }

            for key in self.MODULE_KEYS:
                if key not in data.keys():
                    checklist_results['MissedKeys'].append(key)
                        
                else:
                    for sub_key in self.MODULE_SUB_KEYS:
                        if sub_key not in data[key].keys():
                            checklist_results['MissedSubKeys'].append(sub_key)
                        
                        await asyncio.sleep(0)

                await asyncio.sleep(0)

            checklist_results['status'] = True
            return checklist_results

        except Exception as e:
            print(e)            




asyncio.run(core(module_name="bbc").startup_code())

