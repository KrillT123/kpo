from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from character import Character
    from monster import IMonster

class Field:
    Character: Character = None
    Monster: IMonster = None

    def FromDict( d: dict ):
        if ( not d ):
            return None

        from character import Character

        self = Field()
        self.Character = Character.FromDict( d.get( "Character" ) )

        return self