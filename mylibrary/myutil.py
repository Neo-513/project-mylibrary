import cProfile
import fitz
import os
import pstats
import time


class Parser:
	@staticmethod
	def cookie(cookie: str | dict) -> dict | str:
		if isinstance(cookie, str):
			return {kv.split("=")[0]: kv.split("=")[1] for kv in cookie.split("; ")}
		elif isinstance(cookie, dict):
			return "; ".join([f"{k}={v}" for k, v in cookie.items()])

	@staticmethod
	def pdf(path: str, save_image: bool = False) -> str:
		with fitz.open(path) as pages:
			if save_image:
				folder_path = "[pdf] " + os.path.splitext(os.path.basename(path))[0]
				if not os.path.exists(folder_path):
					os.mkdir(folder_path)
				images = [image for page in pages for image in page.get_images()]
				for i, image in enumerate(images):
					img = pages.extract_image(image[0])
					file_name = f'image{i}.{img["ext"]}'
					with open(os.path.join(folder_path, file_name), "wb") as f:
						f.write(img["image"])
						print("[SAVE IMAGE]", file_name)
			return "".join([page.get_text() for page in pages])


class Decorator:
	@staticmethod
	def timing(func: callable):
		def _func(*args):
			tictoc = time.time()
			datas = func(*args)
			print(f"{func.__name__}():    {time.time() - tictoc}")
			return datas
		return _func

	@staticmethod
	def performance(func: callable):
		def _func(*args):
			profiler = cProfile.Profile()
			profiler.enable()
			datas = func(*args)
			profiler.disable()
			stats = pstats.Stats(profiler).sort_stats("cumtime")
			stats.print_stats()
			return datas
		return _func
