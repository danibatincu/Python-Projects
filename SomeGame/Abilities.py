import random


class Abilities:
    """
    deals 100% strength for physical characters or 100% intellect for magical characters in damage
    no cooldown
    """

    @staticmethod
    def basic_ability(source, target):
        message = ""
        damage = source.stats["strength"] if source.player_class.type == "physical" else source.stats["intellect"]
        if random.random() < source.stats["crit_chance"] / 100:
            damage = damage * 2
            message = "(Critical!)"
        damage = int(damage * (100 - target.stats["physical_def"]) / 100) if source.player_class.type == "physical" \
            else int(damage * (100 - target.stats["magical_def"]) / 100)
        if random.random() < target.stats["avoidance"] / 100:
            damage = 0
            message = "(Avoided!)"
        target.take_damage(damage)
        return source, target, ["-", message]

    """
    increases avoidance by 30%
    is healed by 5% of max hp per round
    lasts 2 rounds
    cooldown 6 rounds
    """

    @staticmethod
    def vanish(source, target):
        avoidance_increase = Effect("Avoidance Increased", "avoidance", 30, 3, False)
        regen = Effect("Regenerate % max health", "current_hp", int(0.05 * source.stats["max_hp"]), 3, True)
        source.add_effect(avoidance_increase)
        source.add_effect(regen)
        return source, target, []

    """
    increase defences by 30%
    regenerate 5% max hp per round
    lasts 2 rounds
    cooldown 6 rounds
    """

    @staticmethod
    def adrenaline(source, target):
        physical_defence_increase = Effect("Increased defences", "physical_def", 30, 3, False)
        magical_defence_increase = Effect("Increased defences", "magical_def", 30, 3, False)
        regen = Effect("Regenerate % max health", "current_hp", int(0.05 * source.stats["max_hp"]), 3, True)
        source.add_effect(physical_defence_increase)
        source.add_effect(magical_defence_increase)
        source.add_effect(regen)
        return source, target, []

    """
    heals for 7.5% of caster's max hp
    heals 5% of caster's max hp per round
    lasts 2 rounds
    cooldown 6 rounds
    """

    @staticmethod
    def heal(source, target):
        heal = int(0.075 * source.stats["max_hp"])
        source.stats["current_hp"] += heal
        message = " (+" + str(heal) + " health)"
        regen = Effect("Regenerate % max health", "current_hp", int(0.05 * source.stats["max_hp"]), 3, True)
        source.add_effect(regen)
        return source, target, ["+", message]

    """
    shields caster for 20% of max hp
    lasts 2 rounds
    cooldown 6 rounds
    """

    @staticmethod
    def mana_shield(source, target):
        shield = Effect("Shielded from damage", "shield", int(0.2 * source.stats["max_hp"]), 3, False)
        source.add_effect(shield)
        return source, target, []


ability_map = {"Basic Attack": ("Attack a target for 100% of your highest damaging stat.",
                                Abilities.basic_ability, 0),
               "Vanish": ("Increases avoidance by 30% and heal 5% of maximum health per round for 2 rounds "
                          "(6 rounds cooldown).", Abilities.vanish, 6),
               "Adrenaline": ("Increases defences by 30% and heal 5% of maximum health per round for 2 rounds "
                              "(6 rounds cooldown).", Abilities.adrenaline, 6),
               "Heal": ("Instantly heals for 7.5% of maximum health and another 5% per round for 2 rounds "
                        "(6 rounds cooldown).", Abilities.heal, 6),
               "Mana Shield": ("Shields caster for 20% of maximum health for 2 rounds (6 rounds cooldown).",
                               Abilities.mana_shield, 6)}


class Effect:
    def __init__(self, name, stat, value, duration, repeated, buff=True):
        self.name = name
        self.stat = stat
        self.value = value
        self.duration = duration
        self.repeated = repeated
        self.is_applied = False
        self.buff = buff

    def apply(self, target):
        if self.repeated:
            target.stats[self.stat] += self.value
        elif not self.is_applied:
            target.stats[self.stat] += self.value
            self.is_applied = True
        self.duration -= 1
        return target.stats[self.stat]

    def expire(self, target):
        target.stats[self.stat] -= self.value
        self.duration -= 1
        return target.stats[self.stat]

    def __str__(self):
        sign = ""
        if self.value > 0:
            sign = "+"
        return self.name + ", " + sign + str(self.value) + " " + self.stat + ", " + str(self.duration) + " rounds"


class Ability:
    def __init__(self, ability_name):
        self.name = ability_name
        self.desc = ability_map[ability_name][0]
        self.function = ability_map[ability_name][1]
        self.cooldown = ability_map[ability_name][2]
        self.current_cooldown = 0
        self.active = True

    def use(self, source, target):
        self.active = False
        self.current_cooldown = self.cooldown
        return self.function(source, target)

    def reduce_cooldown(self):
        self.current_cooldown -= 1
        if self.current_cooldown <= 0:
            self.current_cooldown = 0
            self.active = True
