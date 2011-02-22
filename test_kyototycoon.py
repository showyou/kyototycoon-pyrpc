import kyototycoon as kt
import nose
from nose.tools import ok_

class Test_KyotoTycoon(object):
    def __init__(self):
        self.kt = kt.KyotoTycoon()

    def testOpen(self):
        #print self.kt
        ok_(self.kt.open(port=4130))

    def testSet(self):
        self.testOpen()
        ok_(self.kt.set("japan", "tokyo", 60))

    def testGet(self):
        self.testOpen()
        ok_(self.kt.get("japan"))

    def testVacuum(self):
        self.testOpen()
        ok_(self.kt.vacuum())

    def testRemove(self):
        self.testOpen()
        ok_(self.kt.remove("japan"))

    def testCurJump(self):
        self.testOpen()
        ok_(self.kt.cur_jump())
        ok_(self.kt.cur_get())


if __name__=='__main__':
    nose.main()
