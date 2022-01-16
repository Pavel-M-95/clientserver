import logging
import time
import inspect
import sys

logging.basicConfig(
    filename="messenger.log",
    format="%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s",
    level=logging.INFO,
    filemode="a"
)

# В данном примере аналогичен базовой настройке, но может быть и другим
main_format = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s")

handler1 = logging.FileHandler("messenger.log")
# handler2 = logging.StreamHandler(sys.stdout)

handler1.setFormatter(main_format)
# handler2.setFormatter(main_format)

main_log = logging.getLogger('messanger')
main_log.setLevel(logging.INFO)
main_log.addHandler(handler1)
# main_log.addHandler(handler2)
main_log.propagate = False


def log(func):
    def wrapped(*args, **kwargs):
        # добавляем вместо %(message)s аргументы нашей функции
        # dt = time.ctime(time.time())
        # name = func.__name__
        # caller = inspect.stack()[1].function
        # print("{} Function \"{}\" is called by \"{}\"-function\n".format(dt, name, caller))
        # main_log.info("Function \"%s\" is called by %s", name, caller)
        main_log.info("%s ", tuple(args))
        r = func(*args, **kwargs)
        return r
    return wrapped
