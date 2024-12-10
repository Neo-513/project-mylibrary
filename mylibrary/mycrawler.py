import aiofiles
import aiohttp
import asyncio
import collections
import os
import re
import time

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
HEADERS = {"user-agent": USER_AGENT}
PROXY = "http://127.0.0.1:17890"


def crawl(
	urls: list,
	cookie: str = None,
	sifters: list[str] = None,
	proxy: str = "",
	folder: str = "",
	encoding: str = "utf-8"
):
	async def _main():
		connector = aiohttp.TCPConnector(ssl=False)
		async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
			tasks = [_fetch(url, session) for url in urls]  # 任务列表
			await asyncio.gather(*tasks)  # 异步执行任务列表

	async def _fetch(url, session):  # 爬取单个url
		async with await session.get(url, proxy=proxy) as response:
			param["count"] += 1
			print(f'[{param["count"]:0{zfill}}]  {folder}  {url}')
			response.raise_for_status()

			if folder:
				async with aiofiles.open(f'{folder.rstrip("/")}/{url.split("/")[-1]}', mode="wb") as file:
					data = await response.read()
					await file.write(data)
			else:
				data = await response.text(encoding=encoding)
				dic[url] = data if not sifters else sum([sifter.findall(data) for sifter in sifters], [])

	if cookie:
		HEADERS["cookie"] = cookie
	if sifters:
		sifters = [re.compile(sifter, re.S) for sifter in sifters]
	if folder and not os.path.exists(folder):
		os.mkdir(folder)

	param = {"count": -1}
	zfill = len(str(len(urls) - 1))
	dic = collections.defaultdict(dict)

	tictoc = time.time()
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(_main())
	print(f"[CRAWLED IN]    {time.time() - tictoc}")

	if not folder:
		return [dic[url] for url in urls if url in dic]
