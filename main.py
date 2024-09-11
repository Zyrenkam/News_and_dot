import logging
import threading

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


def func1():
    import bot


def func2():
    import controller_bot


logger.info("Try to connect...")

download1 = threading.Thread(target=func1, name="Downloader")

download2 = threading.Thread(target=func2, name="Downloader")

try:
    download1.start()
    download2.start()
    logger.info("Bot is working")

except Exception as err:
    print('WE HAVE PROBLEMS!')
    logging.error(err, exc_info=True)
