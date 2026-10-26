from __future__ import annotations
import weapon
from trinket import Trinket
import math
import time
from typing import TYPE_CHECKING, Tuple, List, Dict

if TYPE_CHECKING:
    from field import Field
    from monster import Monster

class Character:
    _EquippedWeapon: weapon.Weapon = None
    _Health: float = 10
    _MaxHealth: float = 10
    _Defense: float = 0
    _DamageBonus: float = 0
    _Trinkets: List[ Trinket ] = []
    _Defending: bool = False

    def __init__( self ):
        self._Trinkets = [ None ] * 2

    def FromDict( d: dict ):
        self = Character()

        self._EquippedWeapon = weapon.Weapon.FromDict( d.get( "_EquippedWeapon" ) )
        self._Health = d.get( "_Health", self._Health )
        self._MaxHealth = d.get( "_MaxHealth", self._MaxHealth )
        self._Defense = d.get( "_Defense", self._Defense )
        self._DamageBonus = d.get( "_DamageBonus", self._DamageBonus )
        self._Trinkets = [ Trinket.FromDict( d[ "_Trinkets" ][ 0 ] ), Trinket.FromDict( d[ "_Trinkets" ][ 1 ] ) ]
        self._Defending = d.get( "_Defending", self._Defending )

        return self

    def SetHealth( self, newHealth: float ) -> None:
        self._Health = min( self._MaxHealth, newHealth )

    def GetHealth( self ) -> float:
        return self._Health

    def SetMaxHealth( self, newMaxHealth: float ) -> None:
        self._MaxHealth = newMaxHealth

    def GetMaxHealth( self ) -> float:
        return self._MaxHealth

    def IsAlive( self ) -> bool:
        return self._Health > 0

    def GetTrinket( self, slot: int ) -> Trinket:
        return self._Trinkets[ slot ]

    def EquipTrinket( self, slot: int, trinket: Trinket ) -> None:
        self.UnequipTrinket( slot )

        self._MaxHealth += trinket.HealthBonus
        self._Defense += trinket.DefenseBonus
        self._DamageBonus += trinket.DamageBonus

        self._Health = min( self._MaxHealth, self._Health )

        self._Trinkets[ slot ] = trinket


    def UnequipTrinket( self, slot: int ) -> Trinket:
        if ( not self._Trinkets[ slot ] ):
            return None

        trinket: Trinket = self._Trinkets[ slot ]

        self._MaxHealth -= trinket.HealthBonus
        self._Defense -= trinket.DefenseBonus
        self._DamageBonus -= trinket.DamageBonus

        self._Health = min( self._MaxHealth, self._Health )

        self._Trinkets[ slot ] = None

        return trinket

    def EquipWeapon( self, weapon: weapon.Weapon ) -> None:
        self._EquippedWeapon = weapon

    def TakeDamage( self, damage: float ) -> None:
        finalDamage: float = max( 0, damage - self._Defense )
        if ( self._Defending ):
            finalDamage *= 0.25
        finalDamage = round( finalDamage )
        print( f"You take {finalDamage} damage!" )
        self._Health -= finalDamage

    def TakeTurn( self, field: Field ) -> None:
        self._Defending = False

        while True:
            action = int( input( f"You have {self._Health}/{self._MaxHealth} HP\nChoose your action\n1.Attack\n2.Guard\n" ) )

            if ( action == 1 ):
                print( f"You attack {field.Monster.GetName()}!" )

                time.sleep( 0.5 )

                damage: int = 1

                if ( self._EquippedWeapon ):
                    damage = self._EquippedWeapon.Damage

                damage += self._DamageBonus

                field.Monster.TakeDamage( damage )

                return

            if ( action == 2 ):
                print( "You take guard..." )

                self._Defending = True

                return
