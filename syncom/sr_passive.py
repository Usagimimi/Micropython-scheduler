# sr_passive.py Test of synchronous comms library. Passive end.

# The MIT License (MIT)
#
# Copyright (c) 2016 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from usched import Sched
from syncom import SynCom
from machine import Pin

def passive_thread(chan):
    yield
    while True:
        while not chan.any():
            yield
        obj = chan.get()
        print('passive received: ', obj)
        obj[2] += 1 # modify object and return
        chan.send(obj)

def test():
    mtx = Pin(14, Pin.OUT) # Define passive pins
    mckout = Pin(15, Pin.OUT, value = 0) # clocks must be initialised to zero. Pin 15 has pulldown
    mrx = Pin(13, Pin.IN)
    mckin = Pin(12, Pin.IN) # add 10K pulldown

    objsched = Sched()
    with SynCom(objsched, True, mckin, mckout, mrx, mtx) as channel:
        objsched.add_thread(passive_thread(channel))
        objsched.run()

#test()

