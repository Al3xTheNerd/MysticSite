from typing import List
from core.models import Item, Crate
from sqlalchemy import desc
from atn import server_custom_tags
def errorMaker(errorCode: int | str = "???") -> List[Item]:
    resp = Item
    resp.ItemHTML = f"""
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
        <div><span style="color: #AAAAAA; ">Rarity: </span><span style="color: #55FF55; ">Common :(</span></div>"""
        
    return([resp]) # type: ignore


def currentCrateData():
    crates = Crate.query.order_by(desc(Crate.id))
    formattedCrates = {}
    for crate in crates.all():
        formattedCrates[crate.id] = {
            "CrateName" : crate.CrateName,
            "ReleaseDate" : crate.ReleaseDate,
            "URLTag" : crate.URLTag
        }
    if formattedCrates:
        return formattedCrates
    return None

PrettyRoutes = {
    "/" : "Home",
    "/all" : "All Items",
    "/stats" : "Item Statistics",
    "/itemtracker" : "Item Tracker",
    "/infinitetracker" : "Infinite Tracker",
    "/jobspayouts" : "Jobs Payouts",
    "/gamble" : "Gamble",
    "/tag/Armor/all" : "Armor",
    "/tag/Tools/all" : "Tools",
    "/tag/Weapons/all" : "Weapons",
    "/login" : "Login",
    "/search" : "Advanced Search"
}

tags = {
    "Armor" : [
        "Hat",
        "Helmet",
        "Chestplate",
        "Leggings",
        "Boots",
        "Elytra"
    ],
    "Tools" : [
        "Pickaxe",
        "Axe",
        "Hoe",
        "Shovel",
        "Rod",
        "Shield",
        "Shears"
    ],
    "Weapons" : [
        "Crossbow",
        "Sword",
        "Axe",
        "Bow",
        "Trident",
        "Mace"
    ]
}
nonCatTags: List[str] = [
    "Infinite",
    "Offhand",
    "Hotbar",
    "Inventory",
    "Special Block",
    "Quest",
    "Disguise",
    "Repeat Appearance",
    "Unbreakable Kit",
    "Head Dropping",
    "Egg Dropping",
    "Mob Capturing",
    "Cooker",
    "Teleportation",
    "Quest Only"
]
if server_custom_tags:
    nonCatTags += server_custom_tags
validTags = []
for category, tagList in tags.items():
    for tag in tagList:
        route = f"/tag/{category}/{tag}"
        pretty = f"{tag}"
        PrettyRoutes[route] = tag
        if tag not in validTags:
            validTags.append(tag)
for tag in nonCatTags:
    route = f"/tag/Misc/{tag}"
    pretty = f"{tag}"
    PrettyRoutes[route] = tag
    if tag not in validTags:
        validTags.append(tag)



for category, tagList in tags.items():
    for tag in tagList:
        route = f"/tag/{category}/{tag}"
        pretty = f"{tag}"
        PrettyRoutes[route] = tag

Changelog = {
    "2/19/2025" : [
        ("mc-gold", "Corrected spelling mistake on Stats page."),
        ("mc-gold", "Setup auto deployment from dev environment.")
    ],
    "2/21/2025" : [
        ("mc-gold", "Added Item Tracker! Thank you SaltyAssassin for the suggestion!")
    ],
    "2/22/2025" : [
        ("mc-gold", "Moved the page showing all items to a secondary page, in an effort to help people with less than stellar internet connections still use the site. Thank you KaylaKrow for the suggestion!"),
        ("mc-gold", "Moved changelog to the main page.")
    ],
    "3/2/2025" : [
        ("mc-gold", "Reworked Navbar to bring me more joy."),
        ("mc-gold", "Added Infinite specific item tracker."),
        ("mc-gold", "Reworked database and created a database builder to make it easier to modify items.")
        
    ],
    "3/9/2025" : [
        ("mc-gold", "Item/Infinite trackers now persistently store your items! Thank you Katie for the suggestion!")
    ],
    "3/16/2025" : [
        ("mc-gold", "Corrected a database error leading to no swords being listed under <a href=\"/tag/Weapons/Sword\">Swords</a>, thank you LostWoodsOne for bringing this to my attention!")
    ],
    "6/3/2025" : [
        ("mc-gold", "Added <a href=\"/gamble\">Gambling</a>! Thank you BR_MarkoTheGamer for the suggestion!"),
        ("mc-gold", "Removed some redundant HTML tags (why were there 47 extra &lt;/li&gt; tags in the navbar??)"),
        ("mc-gold", "Added a Page View Tracker (again)")
    ],
    "6/5/2025" : [
        ("mc-green", "<a href=\"/gamble\">Gambling</a> is now weighted as it is in-game!"),
        ("mc-light-purple", "Cleaned up the Gambling Menu."),
        ("mc-green", "Added overviews to the gambling menu, so you can see what you got at a glance instead of looking through individually."),
        ("mc-light-purple", "Added a limit to how many rolls you could do at once. (turns out things get a bit wild when you try and roll 1,000,000 items :p)"),
        ("mc-red", "Corrected a bug where the changelog would break if you didn't also search for an item."),
        ("mc-red", "Pickaxes that appear in multiple crates now appear on their crate pages, they can also be pulled during gambling.")
    ],
    "6/11/2025" : [
        ("mc-gold", "Adjusted CSS (stupid fucking bootstrap) to be a bit more consistent and readable across the site."),
        ("mc-green", f"Made it so crate summaries for <a href=\"/gamble\">Gambling</a> show the colored item names."),
        ("mc-green", "Removed the silly gap space between tiles. (I'm still unsure if I like this better or not, may be reverted :s)")
    ],
    "6/14/2025" : [
        ("mc-gold", "Cleaned up some more HTML code."),
        ("mc-gold", "Standardized the code for displaying items into one file, to be shared across the site.")
    ],
    "7/7/2025" : [
        ("mc-green", "New tagging system, all items can now have up to 2 'keywords' (Offhand, Helmet) for better organization. This should help to narrow down searches a bit more."),
        ("mc-green", "Added item type to all items(minecraft:bow), should improve readability of site."),
        ("mc-green", "Slightly more automated changelog."),
        ("mc-green", "More navbar shenanigans!"),
        ("mc-gold", "Fully rewrote backend to support adding new items directly to the site. I was fully rebuilding the database previously with the old system."),
    ],
    "7/12/2025" : [
        ("mc-green", "Items can now support Tertiary Tags"),
        ("mc-light-purple", "Gambling item limit 10,000 -> 1,000.")
    ],
    "7/19/2025" : [
        ("mc-green", "Added randomized background colors!"),
        ("mc-light-purple", "Navbar swapped over to dark mode."),
        ("mc-green", "Changelogs now use different colors to denote different types of updates, 5 free keys to the first person who correctly guesses my intent for each currently used color. (6/14 and earlier are not updated colors wise.)"),
        ("mc-light-purple", "Buffed out some corners around the site, tables are hopefully a little less jarring to look at.")
    ],
    "7/26/2025" : [
        ("mc-green", "Adjusted page titles to prettier names for each public page.")
    ],
    "8/3/2025" : [
        ("mc-gold", "Whole new addition on the backend. I can now adjust the order that items appear in if I need to make adjustments later on."),
        ("mc-red", "Disabled the Masonry tiling, decided I don't love it."),
        ("mc-gold", "Backend Dashboard is now setup to supply the Discord Bot with a different item name as needed (prom level 2 and whatnot)"),
        ("mc-green", "Clicking an item on the bot or on the website will now take you to a screen showing far more detailed item information. Including tags or other notes that I've added (currently only 2 items have notes, see if you can find them)")
    ],
    "8/6/2025" : [
        ("mc-green", "Both Infinite tracker and Item tracker now generate a Discord formatted list, to make your shopping lists that much easier!")
    ],
    "8/18/2025" : [
        ("mc-green", "<a href=\"/search\">Advanced Search</a> is now available!")
    ],
    "8/19/2025" : [
        ("mc-light-purple", "Background colors normalized, should shave off some ms during load time."),
        ("mc-light-purple", "Spacing between columns adjusted, reduces amount of html tags loaded per page as well by a wide margin. Should also reduce load time.")
    ],
    "9/17/2025" : [
        ("mc-green", "Site now supports Quantary and Quinary tags.")
    ]
}

        
Changelog = dict(reversed(list(Changelog.items())))