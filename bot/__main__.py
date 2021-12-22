from loguru import logger

from bot.load import main


try:
    main()
except (KeyboardInterrupt, SystemExit):
    logger.info("Bot stopped.")
