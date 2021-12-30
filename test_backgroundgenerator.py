import unittest as ut
import BackgroundGenerator as BG

class generatorTestCase(ut.TestCase):
    def setUp(self):
        self.PC_A = BG.PC()
        PC_A.Strength, PC_A.Dexterity, PC_A.Wisdom, PC_A.Constitution, PC_A.Intelligence, PC_A.Charisma = 10,10,10,10,10,10
        PC_A.sex = "Male"
        PC_A.name = "Foobar"
        self.PC_B = BG.PC()
        PC_B.Strength, PC_B.Dexterity, PC_B.Wisdom, PC_B.Constitution, PC_B.Intelligence, PC_B.Charisma = 10,10,10,10,10,10
        PC_B.sex = PC_A.sex
        PC_B.name = PC_A.name
