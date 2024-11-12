#!/usr/bin/env python3

import sss

s = sss.ssh()
s.retrieve()

t = sss.telnet()
t.retrieve()

f = sss.file()
f.retrieve()
