import asyncio
import aiofiles
import aiohttp
import requests
from timeit import default_timer as timer


async def download_file_async(session, url):
    async with session.get(url, ssl=False) as res:
        name = url.split('/')[-1]
        file_path = f'output/async/{name}'

        async with aiofiles.open(file_path, 'wb') as f:
            while True:
                chunk = await res.content.read(1024)
                if not chunk:
                    break
                await f.write(chunk)

        return await res.release()


async def main_async(url):
    async with aiohttp.ClientSession() as session:
        await download_file_async(session, url)


def download_async():
    loop = asyncio.get_event_loop()
    with open('links.txt', 'r') as links:
        urls = [link.replace("\n", "") for link in links.readlines()]
        loop.run_until_complete(asyncio.gather(
            *(main_async(url) for url in urls)
        ))


def download_sync():
    with open('links.txt', 'r') as links:
        for url in links.readlines():
            url = url.replace("\n", "")
            res = requests.get(url)

            name = url.split('/')[-1]
            file_path = f'output/sync/{name}'
            with open(file_path, 'wb') as f:
                f.write(res.content)


if __name__ == '__main__':
    start = timer()
    download_async()
    print(f'Took async {timer() - start}')

    start = timer()
    download_sync()
    print(f'Took sync {timer() - start}')
