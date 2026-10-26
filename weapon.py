class Weapon:
    Name: str = "Stick"
    Damage: float = 1

    def __init__( self, name, damage ):
        self.Name = name
        self.Damage = damage

    def FromDict( d: dict ):
        if ( not d ):
            return None

        self = Weapon( d.get( "Name", Weapon.Name ), d.get( "Damage", Weapon.Damage ) )

        return self