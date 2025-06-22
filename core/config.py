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

tags = {
    "Armor" : [
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
        "Rod"
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
nonCatTags = [
    "Infinite",
    "Offhand",
    "Hotbar",
    "Inventory",
    "Quest",
    "Repeat Appearance"
]
validTags = []
for category, tagList in tags.items():
    for tag in tagList:
        if tag not in validTags:
            validTags.append(tag)
for tag in nonCatTags:
    if tag not in validTags:
        validTags.append(tag)



Changelog = {
    "2/19/2025" : [
        ("mc-gold", "Added missing Olympus Quests."),
        ("mc-gold", "Corrected spelling mistake on Stats page."),
        ("mc-gold", "Setup auto deployment from dev environment.")
    ],
    "2/21/2025" : [
        ("mc-gold", "Added Item Tracker! Thank you SaltyAssassin for the suggestion!"),
        ("mc-gold", "Added Missing item (Mystic Boots)")
    ],
    "2/22/2025" : [
        ("mc-gold", "Moved the page showing all items to a secondary page, in an effort to help people with less than stellar internet connections still use the site. Thank you KaylaKrow for the suggestion!"),
        ("mc-gold", "Moved changelog to the main page.")
    ],
    "3/2/2025" : [
        ("mc-gold", "Reworked Navbar to bring me more joy."),
        ("mc-gold", "Added Infinite specific item tracker."),
        ("mc-gold", "Reworked database and created a database builder to make it easier to modify items."),
        ("mc-gold", "Added Elysium Pickaxe."),
        
    ],
    "3/8/2025" : [
        ("mc-gold", "Cosmic/Arcane Picks Win Chance 0.1%->0.06%")
    ],
    "3/9/2025" : [
        ("mc-gold", "Item/Infinite trackers now persistently store your items! Thank you Katie for the suggestion!")
    ],
    "3/16/2025" : [
        ("mc-gold", "Corrected a database error leading to no swords being listed under <a href=\"{{ url_for('weapon', type='Sword') }}\">Swords</a>, thank you LostWoodsOne for bringing this to my attention!")
    ],
    "3/30/2025" : [
        ("mc-gold", "Added a <a href=\"{{ url_for('jobspayouts') }}\">Jobs Payout Calculator</a>!"),
        ("mc-gold", "Added the new <a href=\"{{ url_for('crate', crateName='Trickster') }}\">Trickster Crate</a>!"),
        ("mc-gold", "Updated the Eternal Icesight to the new version!")
    ],
    "5/11/2025" : [
        ("mc-gold", "Added the new <a href=\"{{ url_for('crate', crateName='Bloomfall') }}\">Bloomfall Crate</a>!")
    ],
    "6/3/2025" : [
        ("mc-gold", "Added <a href=\"{{ url_for('gamble') }}\">Gambling</a>! Thank you BR_MarkoTheGamer for the suggestion!"),
        ("mc-gold", "Removed some redundant HTML tags (why were there 47 extra &lt;/li&gt; tags in the navbar??)"),
        ("mc-gold", "Added a Page View Tracker (again)")
    ],
    "6/5/2025" : [
        ("mc-gold", "<a href=\"{{ url_for('gamble') }}\">Gambling</a> is now weighted as it is in-game!"),
        ("mc-gold", "Cleaned up the Gambling Menu."),
        ("mc-gold", "Added overviews to the gambling menu, so you can see what you got at a glance instead of looking through individually."),
        ("mc-gold", "Added a limit to how many rolls you could do at once. (turns out things get a bit wild when you try and roll 1,000,000 items :p)"),
        ("mc-gold", "Corrected a bug where the changelog would break if you didn't also search for an item."),
        ("mc-gold", "Pickaxes that appear in multiple crates now appear on their crate pages, they can also be pulled during gambling.")
    ],
    "6/11/2025" : [
        ("mc-gold", "Added the new <a href=\"{{ url_for('crate', crateName='Astral') }}\">Season 8: Astral</a> crate!"),
        ("mc-gold", "Corrected Bunny Helmet not showing up under <a href=\"{{ url_for('armor', type='Helmet') }}\">Helmets</a>."),
        ("mc-gold", "Adjusted CSS (stupid fucking bootstrap) to be a bit more consistent and readable across the site."),
        ("mc-gold", "Made it so crate summaries for <a href=\"{{ url_for('gamble') }}\">Gambling</a> show the colored item names."),
        ("mc-gold", "Removed the silly gap space between tiles. (I'm still unsure if I like this better or not, may be reverted :s)")
    ],
    "6/14/2025" : [
        ("mc-gold", "Cleaned up some more HTML code."),
        ("mc-gold", "Standardized the code for displaying items into one file, to be shared across the site.")
    ],
    "6/17/2025" : [
        ("mc-gold", "Adding Item Type to all Item Displays")
    ]
    
}
Changelog = dict(reversed(list(Changelog.items())))