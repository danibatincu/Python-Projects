import random


class Effect:
    def __init__(self, name, stat, value, duration, repeated, variable_value=False):
        self.name = name
        self.stat = stat
        self.value = value
        self.duration = duration
        self.repeated = repeated
        self.is_applied = False

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
            message = " (Critical!)"
        damage = int(damage * (100 - target.stats["physical_def"]) / 100) if source.player_class.type == "physical" \
            else int(damage * (100 - target.stats["magical_def"]) / 100)
        if random.random() < target.stats["avoidance"] / 100:
            damage = 0
            message = " (Avoided!)"
        target.take_damage(damage)
        return "Basic Attack", source, target, 0, [message, str(damage)]

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
        return "Vanish", source, target, 6, []

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
        return "Adrenaline", source, target, 6, []

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
        return "Heal", source, target, 6, [message]

    """
    shields caster for 20% of max hp
    lasts 2 rounds
    cooldown 6 rounds
    """
    @staticmethod
    def mana_shield(source, target):
        shield = Effect("Shielded from damage", "shield", int(0.2 * source.stats["max_hp"]), 3, False)
        source.add_effect(shield)
        return "Mana Shield", source, target, 6, []
