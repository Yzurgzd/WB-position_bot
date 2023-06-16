import aiohttp
import ujson


WB_SEARCH_API_URL = 'https://search.wb.ru/exactmatch/ru/common/v4'
WB_ADS_SEARCH_API_URL = 'https://catalog-ads.wildberries.ru/api/v5'


async def onSearch(query='', page=1):
    async with aiohttp.ClientSession() as session:
        params = {
            'TestGroup': 'no_test',
            'TestID': 'no_test',
            'appType': '1',
            'curr': 'rub',
            'dest': '-412731',
            'page': page,
            'query': query,
            'regions': '80,38,4,64,83,33,68,70,69,30,86,40,1,66,110,22,31,48,114',
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '0',
            'suppressSpellcheck': 'false'
        }
        url = f'{WB_SEARCH_API_URL}/search?'
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.read()
                search = ujson.loads(data)
                return search['data']['products']
        except aiohttp.ClientError as e:
            print(f'An error occurred during the search request: {e}')
            return []


async def onAds(query=''):
    async with aiohttp.ClientSession() as session:
        params = {'keyword': query}
        url = f'{WB_ADS_SEARCH_API_URL}/search?'
        try:
            async with session.get(url, params=params) as resp:
                data = await resp.read()
                return ujson.loads(data)
        except aiohttp.ClientError as e:
            print(f'An error occurred during the ads search request: {e}')
            return {}