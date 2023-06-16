from collections import deque
from service import onSearch, onAds

async def findProductPosition(id, query):
    ads = await onAds(query)
    ads_pages_data = ads['pages']
    ads_pages = set(data['page'] for data in ads_pages_data)
    ads_products = deque(ads['adverts'])
    found = False
    results = {}

    for i in range(1, 61):
        current_page = i
        search_products = await onSearch(query, current_page)

        product_ids_to_remove = set(ap['id'] for ap in ads_products)

        products = [p for p in search_products if p['id'] not in product_ids_to_remove]

        if current_page in ads_pages and not ads_products:
            key_page = list(ads_pages).index(current_page)
            positions = ads_pages_data[key_page]['positions']

            for position in positions:
                if not ads_products:
                    products.insert(position - 1, ads_products.popleft())

        for idx, product in enumerate(products):
            if str(product['id']) == id:
                results['data'] = {'position': idx + 1, 'page': current_page}
                found = True
                break
        if found:
            break
    results['found'] = found
    return results