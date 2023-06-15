from pathlib import Path
from app.controller import BotRunner
from loguru import logger
from utils.base import readconfig
import sys

logger.remove()
handler_id = logger.add(sys.stderr, level="INFO")
logger.add(sink='run.log',
           format="{time} - {level} - {message}",
           level="INFO",
           rotation="20 MB",
           enqueue=True)

config = readconfig().parseFile(str(Path.cwd()) + "/config/app.toml", toObj=True)
App = BotRunner(config)
App.run()