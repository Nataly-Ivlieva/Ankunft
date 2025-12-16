import logging

logger = logging.getLogger("import")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("import.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
