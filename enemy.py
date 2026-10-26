import character
import field
import random
import time

class IEnemy:
    def GetName( self ):
        return "MissingNo"

    def TakeDamage( self, damage: float ):
        pass

    def TakeTurn( self, field: Field ):
        print( self.Name + " does nothing!" )

    def IsAlive( self ):
        return False

class BaseEnemy( IEnemy ):
    _Name: str = "Base Enemy"
    _Health: float = 1
    _MaxHealth: float = 1
    _MinDamage: float = 1
    _MaxDamage: float = 2

    def GetName( self ):
        return self._Name

    def BasicAttack( self, char: Character ):
        print( "{name} attacks!".format( name = self.Name ) )
        time.sleep( 0.5 )
        char.TakeDamage( random.randint( self._MinDamage, self._MaxDamage ) )

    def TakeDamage( self, damage: float ):
        print( "{name} takes {damage} damage!".format( name = self._Name, damage = damage ) )
        self._Health -= damage

    def TakeTurn( self, field: Field ):
        self.BasicAttack( field.Character )

    def IsAlive( self ):
        return self._Health <= 0

class GreenSlime( BaseEnemy ):
    _Name: str = "Green Slime"
    _Health: float = 5
    _MaxHealth: float = 5
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

        if ( _Charged ):
            self._Charged = False
            self._ChargeCooldown = 3
            print( "{name} explodes violently!".format( name = self.Name ) )
            time.sleep( 0.5 )
            char.TakeDamage( 5 )
            return

        if ( math.randint( 1, 2 ) == 1 and self._ChargeCooldown <= 3 ):
            self._Charged = True
            print( "{name} is swelling up...".format( name = self.Name ) )
            time.sleep( 1 )
        else:
            self.BasicAttack( field.Character )

