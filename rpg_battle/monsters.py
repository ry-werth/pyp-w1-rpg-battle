from .exceptions import *

class Monster(object):
    
    strMult = 1
    constMult = 1
    intMult = 1
    spdMult = 1
    init_hp = 10
    
    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        self.level = level
        self.strength = (7 + self.level) * self.strMult
        self.constitution = (7 + self.level) * self.constMult
        self.intelligence = (7 + self.level) * self.intMult
        self.speed = (7 + self.level) * self.spdMult
        self.maxhp = int(self.init_hp + (self.level - 1) * (0.5 * self.constitution))
        self.hp = self.maxhp
        

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        xp = (self.strength + self.constitution + self.intelligence + self.speed)/4 + self.maxhp%10
        return xp
        

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        target.take_damage(self.strength)


    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp += healing
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def is_dead(self):
        """
        Returns True if out of hp
        """
        return self.hp <= 0

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        pass


class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    constMult = 2
    init_hp = 100
    

    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        target.take_damage(self.strength + self.speed)
    
    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        damage -= 5
        if (damage > 0): 
            self.hp -= damage


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    strMult = 2
    intMult = 1.5
    command_q = ['fire_breath', 'tail_swipe', 'fight']

    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        target.take_damage(self.intelligence * 2.5)


class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    strMult = 1.5
    spdMult = 1.5
    command_q = ['poison_breath', 'tail_swipe', 'fight']
    
    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        target.take_damage((self.intelligence + self.constitution) * 1.5)


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    constMult = 0.25
        

    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        target.take_damage(self.intelligence * 1.5)
        Monster.heal_damage(self, self.intelligence * 1.5)
        
    def heal_damage(self, healing):
        """
        decreases hp by healing 
        """
        self.hp -= healing


class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    
    init_hp = 30
    intMult = 2
    command_q = ['fight', 'bite', 'life_drain']
    
    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        bite_damage = self.speed * 0.5
        target.take_damage(bite_damage)
        target.maxhp -= bite_damage
        Monster.heal_damage(self, bite_damage)
        


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    strMult = 1.25
    spdMult = 0.5
    intMult = 0.25
    command_q = ['bash', 'fight', 'life_drain']
    
    def bash(self, target):
        """
        damage: strength * 2
        """
        target.take_damage(self.strength * 2)


class Humanoid(Monster):
    
    def slash(self, target):
        """
        damage: strength + speed
        """
        target.take_damage(self.strength + self.speed)


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    """
    strMult = 1.75
    constMult = 1.5
    init_hp = 20
    command_q =  ['slash', 'fight', 'regenerate']
    
    
    def regenerate(self, *args):
        """
        heals self for constitution
        """
        self.hp += self.constitution


class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    """
    strMult = 1.75
    init_hp = 16
    command_q =  ['blood_rage', 'slash', 'fight']
    
    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        target.take_damage(self.strength * 2)
        self.hp -= (self.constitution * 0.5)
