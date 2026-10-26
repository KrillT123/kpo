from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from field import Field
    from monster import IMonster

import time
import random
import json
from character import Character
from monster import *
from weapon import Weapon
from trinket import Trinket
import glob, os

class Scene:
    def Start( self, game: Game ):
        pass

    def Update( self, game: Game ):
        pass

'''
"1. Величина подземелья и количество жизней хранятся в двух переменных типа int, уровень сложности – в string.
Необходимо сохранять все введённые настройки величины подземелья в файл, которые будут считываться в контейнер типа Stack.
Также необходимо добавить опцию «Вернуть предыдущий размер», который будет работать с этим контейнером."
- бред сумасшедшего
'''

class Settings:
    FileName: str = "GAME.SAVE"
    Lives: int = 10 # ✅ Величина подземелья
    Size: int = 5 # ✅ и количество жизней хранятся в двух переменных типа int
    Difficulty: str = "0" # ✅ , уровень сложности – в string.

    def __init__( self ):
        self.Lives = 10
        self.Size = 5
        self.Difficulty = "0"

    def FromDict( d: dict ):
        if ( not d ):
            return None

        self = Settings()

        self.FileName = d.get( "FileName", self.FileName )
        self.Difficulty = d.get( "Difficulty", self.Difficulty )
        self.Size = d.get( "Size", self.Size )
        self.Lives = d.get( "Lives", self.Lives )

        return self

class MainMenuScene( Scene ):
    class Options:
        NEW_GAME = 1
        CONTINUE = 2
        SETTINGS = 3
        RETURN_PREVIOUS_SIZE = 4
        ABOUT = 5
        EXIT = 6

    _SettingsStack: List[ Settings ] = [] # ✅ , которые будут считываться в контейнер типа Stack.

    def __init__( self ):
        # self._Settings = Settings()
        self._SettingsStack: List[ Settings ] = []

        try:
            with open( "settings.json", "r" ) as f:
                data = json.load( f )
                for d in data:
                    self._SettingsStack.append( Settings.FromDict( d ) )
        except OSError:
            with open( "settings.json", "w" ) as f:
                self._SettingsStack.append( Settings() )
                json.dump( self._SettingsStack, f, default = lambda obj : obj.__dict__, indent = 2 )
                

    def Start( self, game: Game ):
        pass

    def Update( self, game: Game ):
        action: int = int( input( "Приключения в подземелье\n1.Новая игра\n2.Загрузить игру\n3.Настройки\n4.Вернуть предыдущий размер\n5.О программе\n6.Выход\n" ) )

        if ( action == self.Options.NEW_GAME ):
            self.NewGame( game )
            return

        if ( action == self.Options.CONTINUE ):
            self.Continue( game )
            return

        if ( action == self.Options.SETTINGS ):
            self.Settings( game )
            return

        if ( action == self.Options.RETURN_PREVIOUS_SIZE ):
            self.ReturnPreviousSize( game )
            return

        if ( action == self.Options.ABOUT ):
            self.About( game )
            return

        if ( action == self.Options.EXIT ):
            self.Exit( game )
            return

    def NewGame( self, game: Game ):
        fileName: str = input( "Введите название файла сохранения: " )
        fileName += ".SAVE"

        settings: Settings = None

        if ( len( self._SettingsStack ) > 0 ):
            settings = self._SettingsStack[ -1 ]
        else:
            settings = Settings()

        settings.FileName = fileName

        game.SetScene( MainScene.FromSettings( settings ) )
        return

    def Continue( self, game: Game ):
        files: List[ str ] = []

        for k, file in enumerate( glob.glob("*.SAVE") ):
            files.append( file )

        if ( len( files ) == 0 ):
            print( "Файлы сохранений не найдены" )
            return

        print( "Выберете файл сохранения:" )
        for k, file in enumerate( files ):
            print( f"{k + 1}) {file}" )

        file: int = 0

        while True:
            file = int( input( "" ) )

            if ( file >= 1 and file <= len( files ) ):
                break

        with open( files[ file - 1 ], "r" ) as f:
            data: dict = json.load( f )

        game.SetScene( MainScene.FromDict( data ) )

    def Settings( self, game: Game ):
        new: Settings = Settings()

        while True:
            difficulty: int = int( input( "Введите сложность [0-100]: " ) )
            if ( difficulty >= 0 and difficulty <= 100 ):
                new.Difficulty = str( difficulty )
                break

        while True:
            size: int = int( input( "Введите величину подземелья [1-inf]: " ) )
            if ( size >= 1 ):
                new.Size = size
                break

        while True:
            lives: int = int( input( "Введите количество жизней [1-inf]: " ) )
            if ( lives >= 1 ):
                new.Lives = lives
                break

        self._SettingsStack.append( new )

        # ✅ Необходимо сохранять все введённые настройки величины подземелья в файл
        with open( "settings.json", "w" ) as f:
            json.dump( self._SettingsStack, f, default = lambda obj : obj.__dict__, indent = 2 )

    def ReturnPreviousSize( self, game: Game ):
        if ( len( self._SettingsStack ) > 0 ):
            self._SettingsStack.pop() # ✅ Также необходимо добавить опцию «Вернуть предыдущий размер», который будет работать с этим контейнером.
            # (не написано, что должно происходить с остальными опциями)

            with open( "settings.json", "w" ) as f:
                json.dump( self._SettingsStack, f, default = lambda obj : obj.__dict__, indent = 2 )

    def About( self, game: Game ):
        print( "ПРИКЛЮЧЕНИЯ В ПОДЗЕМЕЛЬЕ v5.0.0\n@COPYLEFT 20026 БИЛЛ ДОТКОМ\nВСЕ ЛЕВА ЗАЩИЩЕНЫ" )

    def Exit( self, game: Game ):
        game.Exit()


class MainScene( Scene ):
    _Field: Field = None
    _Settings: Settings = None
    _Floor: int = 0

    def __init__( self ):
        from field import Field
        self._Field = Field()
        self._Field.Character = Character()
        self._Settings = Settings()

    def FromSettings( settings: Settings ):
        self = MainScene()
        self._Settings = settings
        self._Field.Character.SetMaxHealth( settings.Lives )
        self._Field.Character.SetHealth( settings.Lives )
        return self

    def FromDict( save: dict ):
        from field import Field
        self = MainScene()
        self._Floor = save.get( "_Floor", self._Floor )
        self._Field = Field.FromDict( save[ "_Field" ] )
        self._Settings = Settings.FromDict( save[ "_Settings" ] )

        return self

    def Start( self, game: Game ):
        pass

    def Save( self ):
        with open( self._Settings.FileName, "w" ) as f:
            json.dump( self, f, default = lambda obj : obj.__dict__, indent = 4 )

    def Update( self, game: Game ):
        if ( not self._Field.Monster ):
            while True:
                choice: int = int( input( "What do you want to do?\n1.Descend\n2.Save and quit\n3.Give up (DELETE SAVE)\n" ) )
                if ( choice == 1 ):
                    self._Field.Monster = self.GenerateMonster()
                    self._Floor += 1

                    if ( self._Floor > self._Settings.Size ):
                        print( "You win" )
                        try:
                            os.remove( self._Settings.FileName )
                        except OSError:
                            pass
                        game.SetScene( MainMenuScene() )
                        return

                    print( f"[FLOOR {self._Floor}/{self._Settings.Size}]" )
                    print( f"Encountered {self._Field.Monster.GetName()}!" )
                    break

                if ( choice == 2 ):
                    self.Save()
                    game.SetScene( MainMenuScene() )
                    return

                if ( choice == 3 ):
                    print( "You gave up." )
                    os.remove( self._Settings.FileName )
                    game.SetScene( MainMenuScene() )
                    return

        if ( not self.CheckCombatantsStatus( game ) ):
            return

        print( "" )

        self._Field.Character.TakeTurn( self._Field )

        print( "" )
        time.sleep( 0.5 )

        if ( not self.CheckCombatantsStatus( game ) ):
            return

        self._Field.Monster.TakeTurn( self._Field )

        time.sleep( 0.5 )

        if ( not self.CheckCombatantsStatus( game ) ):
            return


    def CheckCombatantsStatus( self, game: Game ) -> bool:
        if ( not self._Field.Character.IsAlive() ):
            print( "You died..." )
            time.sleep( 1 )
            input( "Press Enter to return to main menu" )
            game.SetScene( MainMenuScene() )

            return False

        if ( not self._Field.Monster.IsAlive() ):
            print( f"{self._Field.Monster.GetName()} perishes!" )

            time.sleep( 0.5 )

            self.ChooseReward()

            self._Field.Monster = None

            return False

        return True

    def ChooseReward( self ) -> None:
        weapon: Weapon = self.GenerateWeapon()
        trinket: Trinket = self.GenerateTrinket()

        while True:
            choice: int = int( input( f"Choose your reward:\n1.{weapon.Name}\n2.{trinket.Name}\n3.Heal 5 HP\n" ) )

            if ( choice == 1 ):
                self._Field.Character.EquipWeapon( weapon )
                break

            if ( choice == 2 ):
                while True:
                    slot: int = int( input( "Choose the slot to put the charm in [1,2]\n" ) )

                    if ( slot >= 1 and slot <= 2 ):
                        self._Field.Character.EquipTrinket( slot - 1, trinket )
                        break

                break

            if ( choice == 3 ):
                self._Field.Character.SetHealth( self._Field.Character.GetHealth() + 5 )
                break

    def GenerateMonster( self ) -> IMonster:
        if ( random.randint( 1, 100 ) <= int( self._Settings.Difficulty ) ):
            return BlackSlime()
        return GreenSlime()

    _Trinkets: List[ Trinket ] = [
        Trinket( "Charm of health", 3, 0, 0 ),
        Trinket( "Amulet of vitality", 5, 0, 0 ),
        Trinket( "Ring of life", 7, 0, 0 ),

        Trinket( "Charm of defense", 0, 1, 0 ),
        Trinket( "Amulet of toughness", 0, 2, 0 ),
        Trinket( "Ring of unyielding", 0, 3, 0 ),

        Trinket( "Charm of damage", 0, 0, 2 ),
        Trinket( "Amulet of harming", 0, 0, 3 ),
        Trinket( "Ring of power", 0, 0, 4 ),

        Trinket( "Cursed ring", 0, -1, 5 ),
        Trinket( "Pacifism ring", 9, 0, -1 ),
        Trinket( "Ring of gluttony", 12, -1, -1 ),
        Trinket( "Ring of divine protection", -7, 4, 0 ),

        Trinket( "Small charm", 1, 1, 1 ),
        Trinket( "Large charm", 2, 2, 2 ),
        Trinket( "Ultimate charm", 3, 3, 3 )
    ]

    def GenerateTrinket( self ) -> Trinket:
        return random.choice( self._Trinkets )

    _Weapons: List[ Weapon ] = [
        Weapon( "Wooden stick", 2 ),
        Weapon( "Copper shortsword", 3 ),
        Weapon( "Bag of pebbles", 3 ),
        Weapon( "Rusty sword", 3 ),
        Weapon( "Morning star", 4 ),
        Weapon( "Iron battleaxe", 4 ),
        Weapon( "Steel longsword", 5 )
    ]

    def GenerateWeapon( self ) -> Weapon:
        return random.choice( self._Weapons )
