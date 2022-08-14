import random


class Abilities:
    @staticmethod
    def calculate_damage(source, target, scaling=1.0):
        message = ""
        damage = source.stats["strength"] if source.player_class.type == "physical" else source.stats["intellect"]
        damage *= scaling
        damage = int(damage * (100 - target.stats["physical_def"]) / 100) if source.player_class.type == "physical" \
            else int(damage * (100 - target.stats["magical_def"]) / 100)
        damage = int(damage * max(0, source.stats["damage_modifier"]))
        damage = int(damage * max(0, target.stats["incoming_damage_modifier"]))
        if random.random() < source.stats["crit_chance"] / 100:
            damage = damage * 2
            message = "(Critical!)"
        if random.random() < target.stats["avoidance"] / 100:
            damage = 0
            message = "(Avoided!)"
        return message, damage

    """
    deals 100% strength for physical characters or 100% intellect for magical characters in damage
    no cooldown
    """

    @staticmethod
    def basic_ability(source, target):
        message, damage = Abilities.calculate_damage(source, target)
        target.take_damage(damage)
        return source, target, [["-", message]]

    """
    attacks for 100% of strength
    applies a 10% damage reduction debuff
    takes 40% of enemy's strength per round
    duration: 9 rounds
    cooldown: 9 rounds
    """

    @staticmethod
    def crippling_poison(source, target):
        message, damage = Abilities.calculate_damage(source, target)
        if message == "(Avoided!)":
            return source, target, [["-", message]]
        cripple = Effect("Deals reduced damage", "damage_modifier", -0.1, 10, False, False)
        poison = Effect(
            "Takes % of caster's strength as damage", "current_hp",
            -int(0.4 * source.stats["strength"] * ((100 - target.stats["physical_def"]) / 100)), 9, True, False)
        target.add_effect(cripple)
        target.add_effect(poison)
        target.stats["damage_modifier"] = cripple.apply(target)
        target.take_damage(damage)
        return source, target, [["-", message]]

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
    increase the damage of the next attack by 150% and incoming damage by 50%
    cooldown 4 rounds
    """

    @staticmethod
    def aim(source, target):
        damage_increase = Effect("Next attack deals bonus damage", "damage_modifier", 1.5, 2, False)
        incoming_damage_increase = Effect("You take increased damage", "incoming_damage_modifier", 0.5, 2, False, False)
        source.add_effect(damage_increase)
        source.add_effect(incoming_damage_increase)
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
    attacks for 175% of intellect
    reduces damage dealt and healing received by 50%
    duration 1 round
    cooldown 4 rounds
    """

    @staticmethod
    def curse_of_weakness(source, target):
        message, damage = Abilities.calculate_damage(source, target, 1.75)
        if message == "(Avoided!)":
            return source, target, [["-", message]]
        damage_reduction = Effect("Deals decreased damage", "damage_modifier", -0.5, 2, False, False)
        healing_reduction = Effect("Receives reduced direct healing", "healing_modifier", -0.5, 2, False, False)
        target.add_effect(damage_reduction)
        target.add_effect(healing_reduction)
        target.stats["damage_modifier"] = damage_reduction.apply(target)
        target.stats["healing_modifier"] = healing_reduction.apply(target)
        target.take_damage(damage)
        return source, target, [["-", message]]

    """
    heals for 7.5% of caster's max hp
    heals 5% of caster's max hp per round
    lasts 2 rounds
    cooldown 6 rounds
    """

    @staticmethod
    def heal(source, target):
        heal = int(0.075 * source.stats["max_hp"])
        source.stats["current_hp"] += heal * max(0, source.stats["healing_modifier"])
        regen = Effect("Regenerate % max health", "current_hp",
                       int(0.05 * source.stats["max_hp"]), 3, True)
        source.add_effect(regen)
        return source, target, [["+", ""]]

    """
    attacks for 150% of intellect
    heals for 25% of damage dealt
    cooldown 3 rounds
    """

    @staticmethod
    def life_stealing_firebolt(source, target):
        message, damage = Abilities.calculate_damage(source, target, 1.5)
        if message == "(Avoided!)":
            return source, target, [["-", message]]
        target.take_damage(damage)
        heal = int(0.25 * damage)
        source.stats["current_hp"] += int(heal * max(0, source.stats["healing_modifier"]))
        return source, target, [["-", message], ["+", ""]]

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
                               Abilities.mana_shield, 6),
               "Crippling Poison": ("Attacks a target for 100% of strength, "
                                    "applies a poison that reduces damage dealt by 10% and "
                                    "takes damage equal to 40% of the caster's strength for 9 rounds (9 rounds "
                                    "cooldown).",
                                    Abilities.crippling_poison, 9),
               "Aim": ("Increases the damage of the next attack by 150%, "
                       "but increases damage taken by 50% for 1 round (4 rounds cooldown).",
                       Abilities.aim, 4),
               "Curse of Weakness": ("Attacks a target for 175% of intellect and "
                                     "reduces damage dealt and healing received by the target by 50% for 1 round "
                                     "(4 rounds cooldown).", Abilities.curse_of_weakness, 4),
               "Life-stealing Firebolt": ("Attacks a target for 150% of intellect and "
                                          "heals the caster for 25% of damage dealt "
                                          "(3 rounds cooldown).",
                                          Abilities.life_stealing_firebolt, 3)}


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
