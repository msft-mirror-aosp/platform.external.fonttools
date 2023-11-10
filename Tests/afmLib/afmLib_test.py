import unittest
import os
from fontTools import afmLib


CWD = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(CWD, "data")
AFM = os.path.join(DATADIR, "TestAFM.afm")


class AFMTest(unittest.TestCase):
    def test_read_afm(self):
        afm = afmLib.AFM(AFM)
        self.assertEqual(
            sorted(afm.kernpairs()),
            sorted(
                [("V", "A"), ("T", "comma"), ("V", "d"), ("T", "c"), ("T", "period")]
            ),
        )
        self.assertEqual(afm["V", "A"], -60)
        self.assertEqual(afm["V", "d"], 30)
        self.assertEqual(afm["A"], (65, 668, (8, -25, 660, 666)))

    def test_write_afm(self):
        afm = afmLib.AFM(AFM)
        newAfm, afmData = self.write(afm)
        self.assertEqual(afm.kernpairs(), newAfm.kernpairs())
        self.assertEqual(afm.chars(), newAfm.chars())
        self.assertEqual(
            afm.comments(), newAfm.comments()[1:]
        )  # skip the "generated by afmLib" comment
        for pair in afm.kernpairs():
            self.assertEqual(afm[pair], newAfm[pair])
        for char in afm.chars():
            self.assertEqual(afm[char], newAfm[char])
        with open(AFM, "r") as f:
            originalLines = f.read().splitlines()
        newLines = afmData.splitlines()
        del newLines[1]  # remove the "generated by afmLib" comment
        self.assertEqual(originalLines, newLines)

    @staticmethod
    def write(afm, sep="\r"):
        temp = os.path.join(DATADIR, "temp.afm")
        try:
            afm.write(temp, sep)
            with open(temp, "r") as f:
                afmData = f.read()
            afm = afmLib.AFM(temp)
        finally:
            if os.path.exists(temp):
                os.remove(temp)
        return afm, afmData


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
