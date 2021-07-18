"""Additional information to be presented for curious viewers."""


def more_info() -> str:
    return """
    **Background:** I have a coffee subscription to [Black Rifle Coffee Company](http://blackriflecoffee.com).
    I currently order two bags of coffee every two weeks.

    **The problem:** Recently, I have noticed that I often finish my two bags before the arrival of my next order.

    **The solution:** To solve this problem, I have collected data on my coffee consumption, specifically, tracking the lifetimes' of coffee bags and when I brew a cup of coffee with each.
    I will then use this data to identify the optimal subscription frequency.

    **Implementation:** I have created a [web API](https://a7a9ck.deta.dev/docs) ([source](https://github.com/jhrcook/coffee-counter-api); using [FastAPI](https://fastapi.tiangolo.com) and [Deta](https://www.deta.sh)) to store the data and allow simple and fast access from anywhere.
    I then created a [SwiftBar](https://swiftbar.app) plugin to allow me to [register a cup of coffee from my computers menu bar](https://github.com/jhrcook/SwiftBar-Plugins/blob/master/coffee-tracker.1h.py) and am working on an iOS application to let me register a cup from my phone.
    """


def notes() -> str:
    return """
    ## Notes

    Below are some notes that I have added to keep in mind while interpreting the data presented above:

    1. I changed from 17 g per cup to 11 g per cup when using the AeroPress around April 21, 2021.
    2. When I go on vacation, my normal routine is disrupted, and thus, so if my coffee consumption.
    I often use other coffee and drink at different rates.
    Therefore, periods of irregular (or no use) should be viewed with caution.
    """


def recipes() -> str:
    return """
    ## Recipes

    ### AeroPress

    Currently, my preferred method for brewing with the AeroPress is the [recipe](https://youtu.be/j6VlT_jUVPc) published by James Hoffman.

    1. grind 11 g of coffee beans and pour into the AeroPress
    2. add 200 g of boiling water to the coffee
    3. wait 2 minutes
    4. swirl and wait for 30 additional seconds
    5. press down the plunger with a very weak force

    ### French Press

    Again, I follow the [instructions](https://youtu.be/st571DYYTR8) from James Hoffman, though I am less careful than he seems to want me to be.

    1. grind 30 grams of coffee and pour into the press
    2. add 500 g of boiling water to the coffee
    3. wait for 4 minutes
    4. disrupt the top layer of coffee grinds by gently swirling with a spoon and remove the foam and floaters
    5. wait an additional 7 minutes
    6. add the plunger, but do not press it through, just place it at the top of the coffee and use it as a filter
    7. pour out the coffee, gently so as not to disrupt the coffee bed

    ### Pour Over

    Unsurprisingly, I use the [method](https://youtu.be/AI4ynXzkSQo) prescribed by James Hoffman for my pour overs.
    The only difference is that at home (but not in the office), I use a Melitta because it was offered to me by a friend instead of throwing it out.

    1. rinse the paper filter *very* well
    2. grind 30 g of coffee and add to the cone
    3. "bloom" the coffee by soaking it in 60 g of boiling water, wait for about 30 seconds
    4. disrupt the coffee bed by (relatively) quickly pouring in 300 g of water
    5. swirl the coffee to gently mix
    6. slowly add the remaining 200 g of water (for a total of 500 g of water) slowly to maintain the height of the water in the funnel near the top of the filter
    7. allow the last water to drain through, but do *not* wait for every drop — the last bit is not desirable
    """
