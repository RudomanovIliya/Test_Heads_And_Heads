import random

print('Enter the max hp of creatures:')
N = int(input())

BOUNDS_MIN = 1
BOUNDS_MAX = 30


class CreaturesError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{}'.format(self.value)


def is_alive_decorator(func):
    def wrapper(self, *args, **kwargs):
        if (self._hp <= 0):
            raise CreaturesError('{} is dead'.format(self._name))
        func(self, *args, **kwargs)

    return wrapper


class Creatures:

    def __init__(self, name, hp, attack, defence, min_dmg, max_dmg):
        if (attack > BOUNDS_MAX) or (attack < BOUNDS_MIN):
            raise CreaturesError('Attack value is out bounds')
        if (defence > BOUNDS_MAX) or (defence < BOUNDS_MIN):
            raise CreaturesError('Defence value is out bounds')
        if (hp < 0) or (hp > N):
            raise CreaturesError('HP value is out bounds')
        self._name = name
        self._hp = hp
        self._max_hp = hp
        self._attack = attack
        self._defence = defence
        self._min_dmg = min_dmg
        self._max_dmg = max_dmg

    @is_alive_decorator
    def attack(self, enemy):
        attack_mult = max(self._attack - enemy.get_defence(), 0) + 1
        cube = 0
        while cube < 5 and attack_mult > 0:
            cube = random.randint(1, 6)
            attack_mult -= 1
        if cube >= 5:
            enemy.change_hp(-random.randint(self._min_dmg, self._max_dmg))
        else:
            print(self._name, 'miss')

    @is_alive_decorator
    def change_hp(self, chp):
        self._hp += chp
        self._hp = max(self._hp, 0)
        self._hp = min(self._hp, self._max_hp)
        if chp < 0:
            print(self._name, 'lost', chp, 'hp')
        else:
            print(self._name, 'recover', chp, 'hp')
        if self._hp == 0:
            print(self._name, ' died')

    def get_hp(self):
        return self._hp

    def get_defence(self):
        return self._defence

    def get_max_hp(self):
        return self._max_hp


class Player(Creatures):
    heal_limit = 4

    def __init__(self, name, hp, attack, defence, min_dmg, max_dmg):
        super().__init__(name, hp, attack, defence, min_dmg, max_dmg)

    @is_alive_decorator
    def heal(self):
        if self.heal_limit > 0:
            self.change_hp(self._max_hp * 0.3)
            self.heal_limit -= 1
        else:
            print(self._name, 'out of usages heal')


class Monster(Creatures):
    def __init__(self, name, hp, attack, defence, min_dmg, max_dmg):
        super().__init__(name, hp, attack, defence, min_dmg, max_dmg)


player1 = Player('Player', 20, 10, 5, 1, 6)
goblin1 = Monster('Goblin', 30, 10, 10, 1, 6)

while player1.get_hp() > 0 and goblin1.get_hp() > 0:
    if player1.get_hp() < (player1.get_max_hp() / 2) and player1.get_hp() > 0:
        player1.heal()
    if player1.get_hp() > 0 and goblin1.get_hp() > 0:
        goblin1.attack(player1)
    if goblin1.get_hp() > 0 and player1.get_hp() > 0:
        player1.attack(goblin1)
