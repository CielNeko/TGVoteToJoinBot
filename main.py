from pathlib import Path
from utils.base import ReadConfig
from app.controller import BotRunner
from loguru import logger
import sys

logger.remove()
handler_id = logger.add(sys.stderr, level="INFO")
logger.add(sink='run.log',
           format="{time} - {level} - {message}",
           level="INFO",
           rotation="20 MB",
           enqueue=True)

config = ReadConfig().parseFile(str(Path.cwd()) + "/Config/app.toml", toObj=True)
App = BotRunner(config)
App.run()