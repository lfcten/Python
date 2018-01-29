import logging
import sys

# 日志信息配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', # - 表示左对齐
    datefmt='%c',   # %a %b %d %H:%M:%S %Y
    filename='test.log',
    filemode='w'
)

# 定义Handler 打印INFO及以上级别日志到控制台
console = logging.StreamHandler()
console.setLevel(logging.INFO)
format = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(format)
logging.getLogger('').addHandler(console)
logging.info("This is an info_level log")
logging.debug("This is an info_debug log")

# 设定name
logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')

