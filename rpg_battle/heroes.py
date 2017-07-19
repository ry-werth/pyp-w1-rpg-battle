from .exceptions import *

class Hero(object):
    
    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        self.level = level
        self.strength = 6 
        self.constitution = 6 
        self.intelligence = 6 
        self.speed = 6 
        self.xp = 0
        self.hp = 100 + 0.5 * self.constitution
        self.mp = 50 + 0.5 * self.intelligence
        self.maxhp = self.hp
        self.maxmp =self.mp
        self.strengthMod = 0
        self.intMod = 0
        self.constMod = 0
        self.speedMod = 0
        
        for x in range(1,level):
            self.level_up()
            
        self.level = level
        self.xp = 0
        
        
        
    def level_up(self):
        self.xp = self.xp - self.xp_for_next_level()
        self.level += 1 
        
        self.strength += 1 
        if (self.strengthMod > 0):
            self.strength += self.strengthMod
            
        self.constitution += 1
        if (self.constMod > 0):
            self.constitution += self.constMod
            
        self.intelligence += 1
        if (self.intMod > 0):
            self.intelligence += self.intMod
            
        self.speed += 1
        if (self.speedMod > 0):
            self.speed += self.speedMod
            
        self.maxhp += 0.5 * self.constitution
        self.maxmp +=  0.5 * self.intelligence
        self.maxhp = int(self.maxhp)
        self.maxmp = int(self.maxmp)
        self.hp = self.maxhp
        self.mp = self.maxmp
        
        

    def xp_for_next_level(self):
        """
        Returns the number of xp at which the next level is gained.
        By default this should be 10 times current level, so 10 for
        level 1, 20 for level 2, etc.
        """
        return(10*self.level)

    def fight(self, target):
        """
        Attacks target, dealing damage equal to the user's strength.
        """
        damage = self.strength
        target.take_damage(damage)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        
        while (self.xp >= self.xp_for_next_level()): 
            """is this the correct way to call xp_for_next_level?"""
            self.level_up()
        
    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage
        if (self.hp < 0):
            self.hp = 0

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp += healing
        if (self.hp > self.maxhp):
            self.hp = self.maxhp
            

    def is_dead(self):
        """
        Returns True if out of hp
        """
        return self.hp <= 0


class Warrior(Hero):
    """
    Stat modifiers:
    strength +1
    intelligence -2
    constitution +2
    speed -1
    """
    def __init__(self, level = 1):
        super(Warrior, self).__init__()
        self.strengthMod = 1
        self.intMod = -2
        self.constMod = 2
        self.speedMod = -1
        self.strength += self.strengthMod
        self.constitution += self.constMod 
        self.intelligence += self.intMod
        self.speed += self.speedMod 
        self.hp = 100 + 0.5 * self.constitution
        self.mp = 50 + 0.5 * self.intelligence
        self.hp = int(self.hp)
        self.mp = int(self.mp)
        self.maxhp = self.hp
        self.maxmp =self.mp
        self.abilities = ['fight', 'shield_slam', 'reckless_charge']
        
        for x in range(1,level):
            self.level_up()
            
        self.level = level
        self.xp = 0
        
    
    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        if (self.mp >= 5):
            self.mp -= 5
            target.take_damage(int(1.5*self.strength))
        else:
            raise InsufficientMP()

    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 1.5 * strength
        """
    
        target.take_damage(2*self.strength)
        self.hp -= 4

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    intelligence +3
    constitution -2
    """
    def __init__(self, level = 1):
        super(Mage, self).__init__()
        self.strengthMod = -2
        self.intMod = 3
        self.constMod = -2
        self.strength += self.strengthMod
        self.constitution += self.constMod 
        self.intelligence += self.intMod
        self.speed += self.speedMod 
        self.hp = 100 + 0.5 * self.constitution
        self.mp = 50 + 0.5 * self.intelligence
        self.hp = int(self.hp)
        self.mp = int(self.mp)
        self.maxhp = self.hp
        self.maxmp =self.mp
        self.abilities = ['fight', 'fireball', 'frostbolt']
        
        for x in range(1,level):
            self.level_up()
            
        self.level = level
        self.xp = 0
        
    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        if (self.mp >= 8):
            self.mp -= 8
            target.take_damage(int(6+(.5*self.intelligence)))
        else:
            raise InsufficientMP()        

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        if (self.mp >= 3):
            self.mp -= 3
            target.take_damage(3 + self.level)
        else:
            raise InsufficientMP()

class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    
    def __init__(self, level = 1):
        super(Cleric, self).__init__()
        self.constMod = 1
        self.speedMod = -1
        self.strength += self.strengthMod
        self.constitution += self.constMod 
        self.intelligence += self.intMod
        self.speed += self.speedMod  
        self.hp = 100 + 0.5 * self.constitution
        self.mp = 50 + 0.5 * self.intelligence
        self.hp = int(self.hp)
        self.mp = int(self.mp)
        self.maxhp = self.hp
        self.maxmp =self.mp
        self.abilities = ['fight', 'heal', 'smite']
        
        for x in range(1,level):
            self.level_up()
            
        self.level = level
        self.xp = 0

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        if (self.mp >= 4):
            self.mp -= 4
            target.heal_damage(self.constitution)
        else:
            raise InsufficientMP()

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        if (self.mp >= 7):
            self.mp -= 7
            target.take_damage(int(4 + (0.5 * (self.intelligence + self.constitution))))
        else:
            raise InsufficientMP()

class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    def __init__(self, level = 1):
        super(Rogue, self).__init__()
        self.level = level
        self.strengthMod = 1
        self.intMod = -1
        self.constMod = -2
        self.speedMod = 2
        self.strength += self.strengthMod
        self.constitution += self.constMod 
        self.intelligence += self.intMod
        self.speed += self.speedMod
        self.hp = 100 + 0.5 * self.constitution
        self.mp = 50 + 0.5 * self.intelligence
        self.hp = int(self.hp)
        self.mp = int(self.mp)
        self.maxhp = self.hp
        self.maxmp =self.mp
        self.abilities = ['fight', 'backstab', 'rapid_strike']
        
        for x in range(1,level):
            self.level_up()
            
        self.level = level
        self.xp = 0
        

    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        if (target.hp == target.maxhp):
            target.take_damage(2*self.strength)
        else:
            raise InvalidTarget()

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        if (self.mp >= 5):
            self.mp -= 5
            target.take_damage(4 + self.speed)
        else:
            raise InsufficientMP()

