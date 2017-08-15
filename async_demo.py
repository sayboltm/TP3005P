#https://stackoverflow.com/questions/41398596/two-independent-async-loops-in-python

import asyncio
import random

my_list = []

from datetime import datetime
# ...

start = datetime.now()
def notify():
    length = len(my_list)
    print("t: {:.1f}, List has changed! {}".format(
        (datetime.now() - start).total_seconds(), length))

async def append_task():
    while True:
        await asyncio.sleep(1)
        my_list.append(random.random())
        notify()

async def pop_task():
    while True:
        await asyncio.sleep(1.8)
        my_list.pop()
        notify()

#def notify():
#    length = len(my_list)
#    print("List has changed!", length)
#
#async def append_task():
#    while True:
#        await asyncio.sleep(1)
#        my_list.append(random.random())
#        notify()
#
#async def pop_task():
#    while True:
#        await asyncio.sleep(1.8)
#        my_list.pop()
#        notify()
#

loop = asyncio.get_event_loop()
cors = asyncio.wait([append_task(), pop_task()])
loop.run_until_complete(cors)

### NOOO this is the bad one
#import asyncio
#import time 
#import random
#
#my_list = []
#
#def notify():
#    length = len(my_list)
#    print("List has changed!", length)
#
#async def append_task():
#    while True:
#        time.sleep(1)
#        await my_list.append(random.random())
#        notify()
#
#async def pop_task():
#    while True:
#        time.sleep(1.8)
#        await my_list.pop() 
#        notify()
#        
#loop = asyncio.get_event_loop() 
#loop.create_task(append_task())
#loop.create_task(pop_task())
#loop.run_forever()
