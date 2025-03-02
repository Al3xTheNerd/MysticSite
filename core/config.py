validCrates = {
    "Season 1: Origins" : "Origins",
    "Valerie Collection" : "Valerie",
    "Season 2: Legends" : "Legends",
    "Infinite Glass" : "Glass",
    "Summer Tiki" : "SummerTiki",
    "Season 3: Nature" : "Nature",
    "Halloween" : "Halloween",
    "Infinite Terracotta" : "Terracotta",
    "Winter" : "Winter",
    "Season 4: Lunar" : "Lunar",
    "Infinite Wool" : "Wool",
    "St Patricks" : "StPatricks",
    "Galaxy" : "Galaxy",
    "Season 5: Runic" : "Runic",
    "Infinite Concrete" : "Concrete",
    "Fantasy" : "Fantasy",
    "Infinite Paint" : "Paint",
    "Season 6: Shogun" : "Shogun",
    "Fright Night" : "FrightNight",
    "Snowfall" : "Snowfall",
    "Season 7: Olympus" : "Olympus",
    "Multi" : "Multi"
}
weaponTypes = [
    "All",
    "Sword",
    "Axe",
    "Bow",
    "Crossbow",
    "Trident",
    "Mace"
]
toolTypes = [
    "All",
    "Axe",
    "Hoe",
    "Shovel",
    "Pickaxe",
    "Rod",
    "Miscellaneous"
]
armorTypes = [
    "All",
    "Helmet",
    "Chestplate",
    "Leggings",
    "Boots",
    "Elytra"
]
def errorMaker(errorCode: int = "???"):
    return {
        "itemHTML" : f"""
                        <div><span style="color: #FF6CE9; ">☆ </span><span style="color: #CE9DDA; ">O</span><span style="color: #B6B6D3; ">o</span><span style="color: #9DCECC; ">p</span><span style="color: #85E7C4; ">s</span><span style="color: #6CFFBD; ">i</span><span style="color: #89E2C6; ">e</span><span style="color: #A7C4CF; ">s</span><span style="color: #C4A7D7; ">! </span><span style="color: #FF6CE9; ">☆</span></div>
                        <div><span style="color: #55FF55; ">Sadness 420</span></div>
                        <div><span style="color: #55FF55; ">Hope 69</span></div>
                        <div><span style="color: #55FF55; ">Error Code {errorCode}</span></div>
                        <div><span style="color: #AAAAAA; ">- - - - - ▶ </span><span style="color: #E289E0; ">E</span><span style="color: #D398DC; ">r</span><span style="color: #C4A7D7; ">r</span><span style="color: #B6B6D3; ">o</span><span style="color: #A7C4CF; ">r </span><span style="color: #89E2C6; ">C</span><span style="color: #7BF0C1; ">o</span><span style="color: #6CFFBD; ">l</span><span style="color: #7CEFC2; ">l</span><span style="color: #8DDEC7; ">e</span><span style="color: #9DCECC; ">c</span><span style="color: #ADBED1; ">t</span><span style="color: #BEADD5; ">i</span><span style="color: #CE9DDA; ">o</span><span style="color: #DE8DDF; ">n </span><span style="color: #AAAAAA; ">◀ - - - - -</span></div>
                        <div><br></div>
                        <div><span style="color: #FFFF55; ">Error, no results found :(</span></div>
                        <div><span style="color: #FFFF55; ">If you believe the site is broken,</span></div>
                        <div><span style="color: #FFFF55; ">please contact AlexTheNerd on discord!</span></div>
                        <div><br></div>
                        <div><span style="color: #AAAAAA; ">- - - - - - - - - - - - - - - - - - - - - -</span></div>
                        <div><span style="color: #AAAAAA; ">Rarity: </span><span style="color: #55FF55; ">Common :(</span></div>

        """
    }