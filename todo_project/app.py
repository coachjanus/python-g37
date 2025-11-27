import logging

# logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")
# logging.warning("Hello, Warning!") # # WARNING:root:Hello, Warning!
# logging.info("Hello, INFO!")
# logging.basicConfig(format="{levelname}:{name}:{message}", style="{")
# logging.warning("Hello, Warning!")
# logging.basicConfig(
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
# )
# logging.error("Something went wrong!")

# logging.basicConfig(
#     filename="app.log",
#     encoding="utf-8",
#     filemode="a",
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,)
# logging.warning("Save me!")

# logging.basicConfig(
#     format="{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,
# )
# name = "Samsara"
# logging.debug(f"{name=}")
# # 2025-11-22 14:49 - DEBUG - name='Samsara'

# logging.basicConfig(
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     style="%",
#     datefmt="%Y-%m-%d %H:%M",
#     level=logging.DEBUG,
# )
# name = "Samsara"
# logging.debug("name=%s", name)

# import logging
# logger = logging.getLogger(__name__)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

# logger.addHandler(console_handler)
# logger.addHandler(file_handler)
# print(logger.handlers) #
# [
#   <StreamHandler <stderr> (NOTSET)>,
#   <FileHandler /home/janus/app.log (NOTSET)>
# ]

# logger = logging.getLogger(__name__)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)
# formatter = logging.Formatter(
#    "{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
# )
# console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)
# logger.warning("Stay calm!")

logger = logging.getLogger(__name__)
# logger.level
# # 0

# logger
# # <Logger __main__ (WARNING)>

# logger.parent
# # <RootLogger root (WARNING)>

# formatter = logging.Formatter("{levelname} - {message}", style="{")
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.debug("Just checking in!")
# logger.info("Just checking in, again!")
# # INFO - Just checking in, again!

# console_handler.setLevel("DEBUG")
# logger.debug("Just checking in!")
# print(console_handler) # 
# <StreamHandler <stderr> (DEBUG)>

# logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")
# formatter = logging.Formatter("{levelname} - {message}", style="{")

# console_handler = logging.StreamHandler()
# console_handler.setLevel("DEBUG")
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
# file_handler.setLevel("WARNING")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# logger.debug("Just checking in!")
# # DEBUG - Just checking in!

# logger.warning("Stay curious!")
# # WARNING - Stay curious!

# logger.error("Stay put!")
# # ERROR - Stay put!


def show_only_debug(record):
    return record.levelname == "DEBUG"

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter("{levelname} - {message}", style="{")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
console_handler.addFilter(show_only_debug)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("Just checking in!")
# DEBUG - Just checking in!

logger.warning("Stay curious!")
logger.error("Stay put!")
