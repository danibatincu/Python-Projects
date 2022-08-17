from utils import *


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

        '''
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
        '''

    def play_round_manual(self, ability_code):
        self.turn[self.tp], self.turn[int(not self.tp)], message = \
            self.turn[self.tp].abilities[ability_code].use(self.turn[self.tp], self.turn[int(not self.tp)])

        self.turn[self.tp].reduce_cooldowns()
        self.turn[self.tp].apply_effects()

        self.__player1 = self.turn[0]
        self.__player2 = self.turn[1]

        self.update_hp_shields()

        # self.print_effects()
        # self.print_current_hp()
        # print("-" * 20)
        # print()

        self.tp = int(not self.tp)

        # if self.game_over():
        #   print(self.winner() + " won")

        return message
