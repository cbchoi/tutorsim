import asyncio
import sys
import time

from multiprocessing import Process, Value

from subprocess import STDOUT, check_output, TimeoutExpired

cmd = ['python3', '-c', "while True: pass"]

try:
	output = check_output(cmd, stderr=STDOUT, timeout=2)
except TimeoutExpired:
	print("!!!")

print("!")

'''
class DateProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.exit_future.set_result(True)

@asyncio.coroutine
def get_date(loop):
    code = 'import datetime; print(datetime.datetime.now())'
    exit_future = asyncio.Future(loop=loop)

    before = datetime.datetime.now
    # Create the subprocess controlled by the protocol DateProtocol,
    # redirect the standard output into a pipe
    create = loop.subprocess_exec(lambda: DateProtocol(exit_future),
                                  sys.executable, '-c', code,
                                  stdin=None, stderr=None)
    transport, protocol = yield from create

    while(True)
    # Wait for the subprocess exit using the process_exited() method
    # of the protocol
    yield from exit_future

    # Close the stdout pipe
    transport.close()

    # Read the output which was collected by the pipe_data_received()
    # method of the protocol
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

date = loop.run_until_complete(get_date(loop))
print("Current date: %s" % date)
loop.close()

loop = asyncio.get_event_loop()

@asyncio.coroutine
def func(loop):
	global bFlag
	code = 'while True: pass'
	exit_future = asyncio.Future(loop=loop)

	
	# Create the subprocess controlled by the protocol DateProtocol,
	# redirect the standard output into a pipe
	create = loop.subprocess_exec(lambda: DateProtocol(exit_future),
	                              sys.executable, '-c', code,
	                              stdin=None, stderr=None)

	transport, protocol = yield from create
	yield from exit_future
	bFlag = False

print(after - before)
loop.run_until_complete(func(loop))
print("!")
while after - before < 10 and bFlag:

	after = time.time()
	#print(after)

print(after - before)
print("!")



before = time.time()
after = time.time()

bFlag = True

def f(name, n):
	#global bFlag
	while True: time.sleep(0.1)
	n.value = 1


n = Value('i', 0)

p = Process(target=f, args=('bob', n))
p.start()
p.join()

print(bFlag)
while after - before < 10 and n.value < 1:

	after = time.time()
	#print(after)

print(after - before)
print("!")
'''