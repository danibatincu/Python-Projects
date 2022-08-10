from PlayerClasses import *


class Player:
    def __init__(self, player_class):
        self.player_class = player_class

        self.stats = {"strength": player_class.strength,
                      "vitality": player_class.vitality,
                      "intellect": player_class.intellect,
                      "crit_chance": player_class.crit_chance,
                      "physical_def": player_class.physical_def,
                      "magical_def": player_class.magical_def,
                      "avoidance": player_class.avoidance,
                      "shield": 0,
                      "crit_resist": 0}

        self.stats["max_hp"] = self.stats["vitality"] * 10
        self.stats["current_hp"] = self.stats["max_hp"]

        self.effects = []

        self.abilities = {"basic": Abilities.basic_ability, "defensive": self.player_class.defence_ability}
        self.abilities_cooldown = {"basic": 0, "defensive": 0}

    def add_effect(self, effect):
        self.effects.append(effect)

    def apply_effects(self):
        new_effects = []
        for effect in self.effects:
            self.stats[effect.stat] = effect.apply(self)
            if effect.duration == 0:
                if not effect.repeated:
                    self.stats[effect.stat] = effect.expire(self)
            if effect.duration > 0:
                new_effects.append(effect)
        self.effects = new_effects

    def take_damage(self, value):
        if value <= self.stats["shield"]:
            self.stats["shield"] -= value
        else:
            value -= self.stats["shield"]
            self.stats["current_hp"] -= value

    def reset_current_hp(self):
        self.stats["current_hp"] = self.stats["max_hp"]

    def reduce_cooldowns(self):
        for ability in self.abilities_cooldown.keys():
            self.abilities_cooldown[ability] -= 1
            self.abilities_cooldown[ability] = max(self.abilities_cooldown[ability], 0)


class Match:
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2

    def update_hp_shields(self):
        self.__player1.stats["shield"] = max(self.__player1.stats["shield"], 0)
        self.__player2.stats["shield"] = max(self.__player2.stats["shield"], 0)
        self.__player1.stats["current_hp"] = min(self.__player1.stats["current_hp"], self.__player1.stats["max_hp"])
        self.__player2.stats["current_hp"] = min(self.__player2.stats["current_hp"], self.__player2.stats["max_hp"])

    def print_current_hp(self):
        p1_shield = \
            " (" + str(self.__player1.stats["shield"]) + " shield)" if self.__player1.stats["shield"] > 0 else ""
        p2_shield = \
            " (" + str(self.__player2.stats["shield"]) + " shield)" if self.__player2.stats["shield"] > 0 else ""
        print("Player 1: " +
              str(self.__player1.stats["current_hp"]) + "/" + str(self.__player1.stats["max_hp"]) + p1_shield)
        print("Player 2: " +
              str(self.__player2.stats["current_hp"]) + "/" + str(self.__player2.stats["max_hp"]) + p2_shield)
        print()

    def print_effects(self):
        if len(self.__player1.effects) > 0:
            print("Player 1 effects:")
            for effect in self.__player1.effects:
                print("\t" + str(effect))
        if len(self.__player2.effects) > 0:
            print("Player 2 effects:")
            for effect in self.__player2.effects:
                print("\t" + str(effect))
        print()

    def play(self):
        self.print_current_hp()
        while self.__player1.stats["current_hp"] > 0 and self.__player2.stats["current_hp"] > 0:
            if self.__player1.abilities_cooldown['defensive'] == 0:
                name, self.__player1, self.__player2, cd, message = \
                    self.__player1.abilities["defensive"](self.__player1, self.__player2)
                self.__player1.abilities_cooldown['defensive'] = cd
                m = ""
                if message:
                    m = " ".join(message)
                print("Player 1 used " + name + "." + m)
            else:
                name, self.__player1, self.__player2, cd, message = \
                    self.__player1.abilities["basic"](self.__player1, self.__player2)
                self.__player1.abilities_cooldown['basic'] = cd
                print("Player 1 used " + name + " and dealt " + message[1] + " damage." + message[0])
                if self.__player2.stats["current_hp"] <= 0:
                    break

            self.__player1.reduce_cooldowns()
            self.__player1.apply_effects()
            self.update_hp_shields()

            self.print_effects()
            self.print_current_hp()
            print()

            if self.__player2.abilities_cooldown['defensive'] == 0:
                name, self.__player2, self.__player1, cd, message = \
                    self.__player2.abilities["defensive"](self.__player2, self.__player1)
                self.__player2.abilities_cooldown['defensive'] = cd
                m = ""
                if message:
                    m = " ".join(message)
                print("Player 2 used " + name + "." + m)
            else:
                name, self.__player2, self.__player1, cd, message = \
                    self.__player2.abilities["basic"](self.__player2, self.__player1)
                self.__player2.abilities_cooldown['basic'] = cd
                print("Player 2 used " + name + " and dealt " + message[1] + " damage." + message[0])

            self.__player2.reduce_cooldowns()
            self.__player2.apply_effects()
            self.update_hp_shields()

            self.print_effects()
            self.print_current_hp()
            print("-" * 20)

        if self.__player1.stats["current_hp"] <= 0:
            print("Player 2 won!")
        if self.__player2.stats["current_hp"] <= 0:
            print("Player 1 won!")


if __name__ == '__main__':
    p1 = Player(Mage())
    p2 = Player(Bruiser())
    match = Match(p1, p2)
    match.play()
