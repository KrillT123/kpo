class Trinket:
    Name: str = "Charm"
    HealthBonus: float = 0
    DefenseBonus: float = 0
    DamageBonus: float = 0

    def __init__( self, name, healthBonus, defenseBonus, damageBonus ):
        self.Name = name
        self.HealthBonus = healthBonus
        self.DefenseBonus = defenseBonus
        self.DamageBonus = damageBonus

    def FromDict( d: dict ):
        if ( not d ):
            return None

        self = Trinket( d.get( "Name", Trinket.Name ), d.get( "HealthBonus", Trinket.HealthBonus ), d.get( "DefenseBonus", Trinket.DefenseBonus ), d.get( "DamageBonus", Trinket.DamageBonus ) )

        return self