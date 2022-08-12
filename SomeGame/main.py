from PlayerClasses import *
from Abilities import Ability
import time


class Player:
    def __init__(self, name, player_class):
        self.name = name
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

        self.buffs = []
        self.debuffs = []
        self.effects = []

        self.abilities = [Ability("Basic Attack")]

    def add_ability(self, ability):
        if len(self.abilities) == 8:
            return
        self.abilities.append(Ability(ability))

    def add_effect(self, effect):
        if effect.buff:
            self.buffs.append(effect)
            return
        self.debuffs.append(effect)

    def apply_effects(self):
        new_buffs = []
        new_debuffs = []
        for effect in self.buffs + self.debuffs:
            self.stats[effect.stat] = effect.apply(self)
            if effect.duration == 0:
                if not effect.repeated:
                    self.stats[effect.stat] = effect.expire(self)
            if effect.duration > 0:
                if effect.buff:
                    new_buffs.append(effect)
                else:
                    new_debuffs.append(effect)
        self.buffs = new_buffs
        self.debuffs = new_debuffs
        self.effects = self.buffs + self.debuffs

    def take_damage(self, value):
        if value <= self.stats["shield"]:
            self.stats["shield"] -= value
        else:
            value -= self.stats["shield"]
            self.stats["current_hp"] -= value

    def reset_current_hp(self):
        self.stats["current_hp"] = self.stats["max_hp"]

    def reduce_cooldowns(self):
        for ability in self.abilities:
            ability.reduce_cooldown()

    def is_dead(self):
        return self.stats["current_hp"] <= 0


class Match:
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.turn = [self.__player1, self.__player2]
        self.tp = int(random.random() < 0.5)

    @property
    def player1(self):
        return self.__player1

    @property
    def player2(self):
        return self.__player2

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
        print(self.__player1.name + ": " +
              str(self.__player1.stats["current_hp"]) + "/" + str(self.__player1.stats["max_hp"]) + p1_shield)
        print(self.__player2.name + ": " +
              str(self.__player2.stats["current_hp"]) + "/" + str(self.__player2.stats["max_hp"]) + p2_shield)
        print()

    def print_effects(self):
        if len(self.__player1.effects) > 0:
            print(self.__player1.name + " effects:")
            for effect in self.__player1.effects:
                print("\t" + str(effect))
        if len(self.__player2.effects) > 0:
            print(self.__player2.name + " effects:")
            for effect in self.__player2.effects:
                print("\t" + str(effect))
        print()

    def game_over(self):
        return self.__player1.is_dead() or self.__player2.is_dead()

    def winner(self):
        if self.__player1.is_dead():
            return self.__player2.name
        return self.__player1.name

    def play_round(self):
        if self.turn[self.tp].abilities[1].active:
            self.turn[self.tp], self.turn[int(not self.tp)], message = \
                self.turn[self.tp].abilities[1].use(self.turn[self.tp], self.turn[int(not self.tp)])
            m = ""
            if message:
                m = " ".join(message)
            print(self.turn[self.tp].name + " used " + self.turn[self.tp].abilities[1].name + "." + m)
        else:
            self.turn[self.tp], self.turn[int(not self.tp)], message = \
                self.turn[self.tp].abilities[0].use(self.turn[self.tp], self.turn[int(not self.tp)])
            print(self.turn[self.tp].name + " used " + self.turn[self.tp].abilities[0].name +
                  " and dealt " + message[1] + " damage." + message[0])

        self.turn[self.tp].reduce_cooldowns()
        self.turn[self.tp].apply_effects()

        self.__player1 = self.turn[0]
        self.__player2 = self.turn[1]

        self.update_hp_shields()

        self.print_effects()
        self.print_current_hp()
        print("-" * 20)
        print()

        self.tp = int(not self.tp)

        if self.game_over():
            print(self.winner() + " won")

        def play_round(self):
            if self.turn[self.tp].abilities[1].active:
                self.turn[self.tp], self.turn[int(not self.tp)], message = \
                    self.turn[self.tp].abilities[1].use(self.turn[self.tp], self.turn[int(not self.tp)])
                m = ""
                if message:
                    m = " ".join(message)
                print(self.turn[self.tp].name + " used " + self.turn[self.tp].abilities[1].name + "." + m)
            else:
                self.turn[self.tp], self.turn[int(not self.tp)], message = \
                    self.turn[self.tp].abilities[0].use(self.turn[self.tp], self.turn[int(not self.tp)])
                print(self.turn[self.tp].name + " used " + self.turn[self.tp].abilities[0].name +
                      " and dealt " + message[1] + " damage." + message[0])

            self.turn[self.tp].reduce_cooldowns()
            self.turn[self.tp].apply_effects()

            self.__player1 = self.turn[0]
            self.__player2 = self.turn[1]

            self.update_hp_shields()

            self.print_effects()
            self.print_current_hp()
            print("-" * 20)
            print()

            self.tp = int(not self.tp)

            if self.game_over():
                print(self.winner() + " won")

    def play_round_manual(self, ability_code):
        self.turn[self.tp], self.turn[int(not self.tp)], message = \
            self.turn[self.tp].abilities[ability_code].use(self.turn[self.tp], self.turn[int(not self.tp)])
        m = ""
        if message:
            m = " ".join(message)

        print(self.turn[self.tp].name + " used " + self.turn[self.tp].abilities[ability_code].name + "." + m)

        self.turn[self.tp].reduce_cooldowns()
        self.turn[self.tp].apply_effects()

        self.__player1 = self.turn[0]
        self.__player2 = self.turn[1]

        self.update_hp_shields()

        self.print_effects()
        self.print_current_hp()
        print("-" * 20)
        print()

        self.tp = int(not self.tp)

        if self.game_over():
            print(self.winner() + " won")

        return m


if __name__ == '__main__':
    p1 = Player("Alfred", Priest())
    p1.add_ability("Heal")

    p2 = Player("Billy", Bruiser())
    p2.add_ability("Adrenaline")

    match = Match(p1, p2)
    match.print_current_hp()
    while not match.game_over():
        match.play_round_manual(0)
        time.sleep(5)
