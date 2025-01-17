import logging
from telegram.ext import Updater
from auth import auth
from commands import (
    start,
    partecipanti,
    risultati,
    classifica,
    partite,
    miepartite,
    iscrivimi,
    inserisci,
    help,
    seed,
)

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO,
	handlers=[
    logging.FileHandler("log/log.txt"),
    logging.StreamHandler()
])


def main() -> None:
    # Create the Updater and pass it your bot's token.
    f = open(".credentials/token.txt", "r")
    updater = Updater(f.readline().strip(), use_context=True)
    f.close()

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(auth.handler)
    dispatcher.add_handler(start.handler)
    dispatcher.add_handler(partecipanti.handler)
    dispatcher.add_handler(risultati.handler)
    dispatcher.add_handler(classifica.handler)
    dispatcher.add_handler(partite.handler)
    dispatcher.add_handler(miepartite.handler)
    dispatcher.add_handler(iscrivimi.handler)
    dispatcher.add_handler(inserisci.handler)
    dispatcher.add_handler(help.handler)
    dispatcher.add_handler(seed.handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
