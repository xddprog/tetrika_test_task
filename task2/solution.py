import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

async def url_producer(session, start_url, queue, num_workers):
    current_url = start_url
    urls_count = 0
    
    while current_url:
        await queue.put(current_url)
        urls_count += 1
        
        async with session.get(current_url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            next_link = None
            for link in soup.find_all('a'):
                if link.text == 'Следующая страница':
                    next_link = 'https://ru.wikipedia.org' + link['href']
                    break
            current_url = next_link
    
    for _ in range(num_workers):
        await queue.put(None)

async def page_consumer(session, queue, animals_by_letter, worker_id):
    while True:
        url = await queue.get()
        if url is None:
            queue.task_done()
            break
            
        try:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                for item in soup.select('div.mw-category-group li a'):
                    if item.text:
                        first_letter = item.text[0].upper()
                        animals_by_letter[first_letter] += 1

        except Exception as e:
            print(f"Error processing {url}: {e}")
        finally:
            queue.task_done()

async def main():
    base_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    animals_by_letter = defaultdict(int)
    num_workers = 5
    
    queue = asyncio.Queue()
    
    async with aiohttp.ClientSession() as session:
        producer = asyncio.create_task(url_producer(session, base_url, queue, num_workers))
        consumers = [
            asyncio.create_task(page_consumer(session, queue, animals_by_letter, i))
            for i in range(num_workers)
        ]
        
        await producer
        await queue.join()
        await asyncio.gather(*consumers)

    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(animals_by_letter.keys()):
            writer.writerow([letter, animals_by_letter[letter]])

if __name__ == '__main__':
    asyncio.run(main())
