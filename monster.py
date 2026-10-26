from __future__ import annotations
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character
    from field import Field

class IMonster:
    def GetName( self ):
        return "MissingNo"

    def TakeDamage( self, damage: float ):
        pass

    def TakeTurn( self, field: Field ):
        print( f"MissingNo does nothing!" )

    def IsAlive( self ):
        return True

class BaseMonster( IMonster ):
    _Name: str = "Base Monster"
    _Health: float = 1
    _MaxHealth: float = 1
    _MinDamage: float = 1
    _MaxDamage: float = 2

    def GetName( self ):
        return self._Name

    def BasicAttack( self, char: Character ):
        print( f"{self._Name} attacks!" )
        time.sleep( 0.5 )
        char.TakeDamage( random.randint( self._MinDamage, self._MaxDamage ) )

    def TakeDamage( self, damage: float ):
        damage = round( damage )
        print( f"{self._Name} takes {damage} damage!" )
        self._Health -= damage

    def TakeTurn( self, field: Field ):
        self.BasicAttack( field.Character )

    def IsAlive( self ):
        return self._Health > 0

class GreenSlime( BaseMonster ):
    _Name: str = "Green Slime"
    _Health: float = 3
    _MaxHealth: float = 3
    _MinDamage: float = 1
    _MaxDamage: float = 2

class BlackSlime( GreenSlime ):
    _Name: str = "Black Slime"
    _Health: float = 10
    _MaxHealth: float = 10

    _ChargeCooldown: int = 3
    _Charged: bool = False

    def TakeTurn( self, field: Field ):
        self._ChargeCooldown -= 1

        if ( self._Charged ):
            self._Charged = False
            self._ChargeCooldown = 3
            print( f"{self._Name} explodes violently!" )
            time.sleep( 0.5 )
            field.Character.TakeDamage( 5 )
            return

        if ( random.randint( 1, 2 ) == 1 and self._ChargeCooldown <= 0 ):
            self._Charged = True
            print( f"{self._Name} is swelling up..." )
            time.sleep( 1 )
        else:
            self.BasicAttack( field.Character )

