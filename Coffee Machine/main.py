MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}
money = 0
total = 0
resources_full = True


def check_resources(req_water, req_milk, req_coffee):
    global resources_full
    if resources["water"] < req_water:
        resources_full = False
        print("Sorry there is not enough water.")
    elif resources["coffee"] < req_coffee:
        resources_full = False
        print("Sorry there is not enough coffee.")
    elif resources["milk"] == req_milk:
        resources_full = False
        print("Sorry there is not enough milk.")


def coins(req_cost):
    global total
    global resources_full
    print("Please insert coins.")
    quarters = input("how many quarters?:")
    dimes = input("how many dimes?:")
    nickles = input("how many nickles?:")
    pennies = input("how many pennies?:")
    total = (int(quarters) * 0.25 + int(dimes) * 0.10 + int(nickles) * 0.05 + int(pennies) * 0.01)
    if req_cost > total:
        resources_full = False
        print("Sorry that's not enough money. Money refunded.")


while resources_full:
    coffee: str = input("What would you like? (espresso/latte/cappuccino):").lower()
    if coffee == 'report':
        print(f'Water: {resources["water"]} ml')
        print(f'Milk: {resources["milk"]} ml')
        print(f'Coffee: {resources["water"]} g')
        print(f'Money: ${money}')
    elif coffee == "off":
        resources_full = False
    elif coffee == "espresso":
        check_resources(MENU["espresso"]["ingredients"]["water"], 0, MENU["espresso"]["ingredients"]["coffee"])
        if resources_full:
            coins(MENU["espresso"]["cost"])
        if resources_full:
            resources["water"] -= 50
            resources["coffee"] -= 18
            money += 1.5
            refund = total - 1.5
            print(f'Here is ${str(round(refund, 2))} dollars in change.')
    elif coffee == "latte":
        check_resources(MENU["latte"]["ingredients"]["water"], MENU["latte"]["ingredients"]["milk"],
                        MENU["latte"]["ingredients"]["coffee"])
        if resources_full:
            coins(MENU["latte"]["cost"])
        if resources_full:
            resources["water"] -= 200
            resources["milk"] -= 150
            resources["coffee"] -= 24
            money += 2.5
            refund = total - 2.5
            print(f'Here is ${str(round(refund, 2))} dollars in change.')
    elif coffee == "cappuccino":
        check_resources(MENU["cappuccino"]["ingredients"]["water"], MENU["cappuccino"]["ingredients"]["milk"],
                        MENU["cappuccino"]["ingredients"]["coffee"])
        if resources_full:
            coins(MENU["cappuccino"]["cost"])
        if resources_full:
            resources["water"] -= 250
            resources["milk"] -= 100
            resources["coffee"] -= 24
            money += 3.0
            refund = total - 3.0
            print(f'Here is ${str(round(refund, 2))} dollars in change.')
            print("Here is your latte. Enjoy!")
