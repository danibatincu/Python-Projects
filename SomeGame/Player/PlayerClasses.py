class DefaultClass:
    def __init__(self):
        self.__strength = 10
        self.__vitality = 20
        self.__intellect = 10
        self.__crit_chance = 0
        self.__physical_def = 0
        self.__magical_def = 0
        self.__avoidance = 10

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, s):
        self.__strength = s

    @property
    def vitality(self):
        return self.__vitality

    @vitality.setter
    def vitality(self, v):
        self.__vitality = v

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, i):
        self.__intellect = i

    @property
    def crit_chance(self):
        return self.__crit_chance

    @crit_chance.setter
    def crit_chance(self, c):
        self.__crit_chance = c

    @property
    def physical_def(self):
        return self.__physical_def

    @physical_def.setter
    def physical_def(self, pd):
        self.__physical_def = pd

    @property
    def magical_def(self):
        return self.__magical_def

    @magical_def.setter
    def magical_def(self, md):
        self.__magical_def = md

    @property
    def avoidance(self):
        return self.__avoidance

    @avoidance.setter
    def avoidance(self, a):
        self.__avoidance = a


class Assassin:
    def __init__(self):
        self.__strength = 15
        self.__vitality = 15
        self.__intellect = 4
        self.__crit_chance = 20
        self.__physical_def = 0
        self.__magical_def = 0
        self.__avoidance = 20
        self.type = "physical"

    @staticmethod
    def defense_ability():
        return "Vanish"

    @staticmethod
    def description():
        return "A physical damage class that has high damage, low health and " \
               "specializes on the use of poisons and bleeds and avoiding the enemy"

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, s):
        self.__strength = s

    @property
    def vitality(self):
        return self.__vitality

    @vitality.setter
    def vitality(self, v):
        self.__vitality = v

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, i):
        self.__intellect = i

    @property
    def crit_chance(self):
        return self.__crit_chance

    @crit_chance.setter
    def crit_chance(self, c):
        self.__crit_chance = c

    @property
    def physical_def(self):
        return self.__physical_def

    @physical_def.setter
    def physical_def(self, pd):
        self.__physical_def = pd

    @property
    def magical_def(self):
        return self.__magical_def

    @magical_def.setter
    def magical_def(self, md):
        self.__magical_def = md

    @property
    def avoidance(self):
        return self.__avoidance

    @avoidance.setter
    def avoidance(self, a):
        self.__avoidance = a


class Bruiser:
    def __init__(self):
        self.__strength = 12
        self.__vitality = 22
        self.__intellect = 3
        self.__crit_chance = 5
        self.__physical_def = 10
        self.__magical_def = 10
        self.__avoidance = 10
        self.type = "physical"

    @staticmethod
    def defense_ability():
        return "Adrenaline"

    @staticmethod
    def description():
        return "A physical damage-tank class that specializes on both defending " \
               "against the enemy and dealing high amounts of damage with some risks."

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, s):
        self.__strength = s

    @property
    def vitality(self):
        return self.__vitality

    @vitality.setter
    def vitality(self, v):
        self.__vitality = v

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, i):
        self.__intellect = i

    @property
    def crit_chance(self):
        return self.__crit_chance

    @crit_chance.setter
    def crit_chance(self, c):
        self.__crit_chance = c

    @property
    def physical_def(self):
        return self.__physical_def

    @physical_def.setter
    def physical_def(self, pd):
        self.__physical_def = pd

    @property
    def magical_def(self):
        return self.__magical_def

    @magical_def.setter
    def magical_def(self, md):
        self.__magical_def = md

    @property
    def avoidance(self):
        return self.__avoidance

    @avoidance.setter
    def avoidance(self, a):
        self.__avoidance = a


class Priest:
    def __init__(self):
        self.__strength = 2
        self.__vitality = 18
        self.__intellect = 15
        self.__crit_chance = 5
        self.__physical_def = 0
        self.__magical_def = 0
        self.__avoidance = 10
        self.type = "magical"

    @staticmethod
    def defense_ability():
        return "Heal"

    @staticmethod
    def description():
        return "A magical damage-healer class that uses holy and " \
               "dark magic to both aid allies and curse enemies."

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, s):
        self.__strength = s

    @property
    def vitality(self):
        return self.__vitality

    @vitality.setter
    def vitality(self, v):
        self.__vitality = v

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, i):
        self.__intellect = i

    @property
    def crit_chance(self):
        return self.__crit_chance

    @crit_chance.setter
    def crit_chance(self, c):
        self.__crit_chance = c

    @property
    def physical_def(self):
        return self.__physical_def

    @physical_def.setter
    def physical_def(self, pd):
        self.__physical_def = pd

    @property
    def magical_def(self):
        return self.__magical_def

    @magical_def.setter
    def magical_def(self, md):
        self.__magical_def = md

    @property
    def avoidance(self):
        return self.__avoidance

    @avoidance.setter
    def avoidance(self, a):
        self.__avoidance = a


class Mage:
    def __init__(self):
        self.__strength = 1
        self.__vitality = 17
        self.__intellect = 18
        self.__crit_chance = 10
        self.__physical_def = 0
        self.__magical_def = 0
        self.__avoidance = 5
        self.type = "magical"

    @staticmethod
    def defense_ability():
        return "Mana Shield"

    @staticmethod
    def description():
        return "A magical damage class that uses elemental magic " \
               "to both injure enemies and keep himself/herself alive."

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, s):
        self.__strength = s

    @property
    def vitality(self):
        return self.__vitality

    @vitality.setter
    def vitality(self, v):
        self.__vitality = v

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, i):
        self.__intellect = i

    @property
    def crit_chance(self):
        return self.__crit_chance

    @crit_chance.setter
    def crit_chance(self, c):
        self.__crit_chance = c

    @property
    def physical_def(self):
        return self.__physical_def

    @physical_def.setter
    def physical_def(self, pd):
        self.__physical_def = pd

    @property
    def magical_def(self):
        return self.__magical_def

    @magical_def.setter
    def magical_def(self, md):
        self.__magical_def = md

    @property
    def avoidance(self):
        return self.__avoidance

    @avoidance.setter
    def avoidance(self, a):
        self.__avoidance = a
