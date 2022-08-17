from Player.Abilities import Ability


class Player:
    def __init__(self, name, player_class, photo):
        self.name = name
        self.player_class = player_class

        self.photo = photo

        self.stats = {"strength": player_class.strength,
                      "vitality": player_class.vitality,
                      "intellect": player_class.intellect,
                      "crit_chance": player_class.crit_chance,
                      "physical_def": player_class.physical_def,
                      "magical_def": player_class.magical_def,
                      "avoidance": player_class.avoidance,
                      "shield": 0,
                      "crit_resist": 0,
                      "damage_modifier": 1,
                      "incoming_damage_modifier": 1,
                      "healing_modifier": 1}

        self.stats["max_hp"] = self.stats["vitality"] * 10
        self.stats["current_hp"] = self.stats["max_hp"]

        self.buffs = []
        self.debuffs = []
        self.effects = []

        self.abilities = [Ability("Basic Attack")]

        self.level = 1

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
            self.stats["shield"] = 0
            for effect in self.buffs:
                if effect.stat == "shield":
                    effect.expire(self)
            self.stats["current_hp"] -= value

    def reset_player(self):
        self.stats["current_hp"] = self.stats["max_hp"]
        for effect in self.buffs + self.debuffs:
            effect.expire()

    def reduce_cooldowns(self):
        for ability in self.abilities:
            ability.reduce_cooldown()

    def is_dead(self):
        return self.stats["current_hp"] <= 0

    def __str__(self):
        return self.name + ", a level " + str(self.level) + " " + type(self.player_class).__name__


class PlayableCharacter(Player):
    def __init__(self, name, player_class, photo):
        super().__init__(name, player_class, photo)
        self.gear = {"head": None, "shoulders": None, "chest": None, "hands": None, "legs": None, "feet": None,
                     "main_hand": None, "off_hand": None}
        self.add_ability(self.player_class.defense_ability())
        self.level = 1
        self.inventory = [[None for _ in range(8)] for _ in range(3)]

    def add_gear(self, slot, gear):
        if not gear or slot == gear.slot:
            old_gear = self.gear[slot]
            if old_gear:
                self.stats = old_gear.remove_stats(self)
            self.gear[slot] = gear
            if gear:
                self.stats = gear.apply_stats(self)
            return old_gear
        return None

    def first_empty_slot(self):
        for i in range(3):
            for j in range(8):
                if not self.inventory[i][j]:
                    return i, j
        return -1, -1

    def add_to_inventory(self, gear):
        row, col = self.first_empty_slot()
        if row != -1:
            self.inventory[row][col] = gear

    def set_item_inv_slot(self, row, col, item):
        self.inventory[row][col] = item


class Gear:
    def __init__(self, name, slot, level, stats, image):
        self.name = name
        self.slot = slot
        self.level = level
        self.stats = stats
        self.image = image

    def apply_stats(self, player):
        for stat in self.stats.keys():
            player.stats[stat] += self.stats[stat]
        return player.stats

    def remove_stats(self, player):
        for stat in self.stats.keys():
            player.stats[stat] -= self.stats[stat]
        return player.stats

    def __str__(self):
        st = self.name + "\n" + str(self.slot) + "\nLevel " + str(self.level) + "\n"
        for stat in self.stats.keys():
            st += "+ " + str(self.stats[stat]) + " " + stat + "\n"
        return st[:-1]


if __name__ == '__main__':
    '''
    p1 = PlayableCharacter("Bulliette", Bruiser(), "./Portraits/billy.png")
    p1.add_ability("Aim")
    with open("./Saves/save1.pickle", "wb") as f:
        pickle.dump(p1, f)

    p2 = PlayableCharacter("Merlin", Mage(), "./Portraits/mez.png")
    p2.add_ability("Life-stealing Firebolt")
    with open("./Saves/save2.pickle", "wb") as f:
        pickle.dump(p2, f)
    

    # with open("./Saves/save2.pickle", "rb") as f:
    #     p1 = pickle.load(f)

    helmet = Gear(name="Regular Helmet", slot="head", level=1, stats={"intellect": 5, "crit_chance": 5})
    print(p1.stats)
    p1.add_gear(slot="head", gear=helmet)
    print(p1.gear)
    print(p1.stats)
    p1.add_gear(slot="head", gear=None)
    print(p1.gear)
    print(p1.stats)
    print(p1.abilities)

    # p2 = Player("Billy", Bruiser(), "./Portraits/billy.png")
    # p2.add_ability("Adrenaline")
    # p2.add_ability("Aim")

    # match = Match(p1, p2)
    # match.print_current_hp()
    # while not match.game_over():
    #    match.play_round_manual(0)
    #    time.sleep(5)
    '''
