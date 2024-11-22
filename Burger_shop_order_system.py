#-------------------------------------------------------------------------------
# HA2
# Student Name: Jeremy Southern
# Python version: 3.9
#-------------------------------------------------------------------------------

class AddToCart(list):
    tax_rate = 0.07

    def calc_subtotal(self):
        subtotal = 0
        for item in self:
            subtotal += item.calculate()
        return subtotal

    def calc_tax(self):
        subtotal = self.calc_subtotal()
        return subtotal * self.tax_rate

    def calc_total(self):
        subtotal = self.calc_subtotal()
        tax = self.calc_tax()
        return subtotal + tax

class SimpleBurger(object):
    cart = AddToCart()
    simple_burger_price = {'single': 7.99, 'double': 10.99}

    def __init__(self, bun, patty_count):
        self.bun = bun
        self.patty_count = patty_count
        SimpleBurger.cart.append(self)

    def calculate(self):
        if self.patty_count == 1:
            price = self.simple_burger_price['single']
        elif self.patty_count == 2:
            price = self.simple_burger_price['double']
        else:
            extra_patties = self.patty_count - 2
            price = self.simple_burger_price['double'] + extra_patties * 2.00
        return price

    def __str__(self):
        return F"Simple Burger with {self.patty_count} patty(ies) on a {self.bun} bun - ${self.calculate():.2f}"

class CheeseBurger(SimpleBurger):
    cheese_type_price = {'american': 1.99, 'pepper jack': 0.99}

    def __init__(self, bun, patty_count, cheese_type):
        super().__init__(bun, patty_count)
        self.cheese_type = cheese_type

    def calculate(self):
        base_price = super().calculate()
        cheese_price = self.cheese_type_price.get(self.cheese_type.lower(), 0)
        return base_price + cheese_price

    def __str__(self):
        return F"Cheese Burger with {self.cheese_type} cheese, {self.patty_count} patty(ies) on a {self.bun} bun - ${self.calculate():.2f}"

class VeggieBurger(SimpleBurger):
    topping_price = 0.50

    def __init__(self, bun, patty_count, veggie_toppings):
        super().__init__(bun, patty_count)
        self.veggie_toppings = veggie_toppings

    def calculate(self):
        base_price = super().calculate()
        toppings_price = len(self.veggie_toppings) * self.topping_price
        return base_price + toppings_price

    def __str__(self):
        toppings = ', '.join(self.veggie_toppings) if self.veggie_toppings else 'no toppings'
        return F"Veggie Burger with {toppings}, {self.patty_count} patty(ies) on a {self.bun} bun - ${self.calculate():.2f}"

choice = 'yes'
print('******** Welcome to 209 Burger ******** \n\n')
while choice.lower() != 'no':
    burger_type = input('\tEnter type of Burger (simple/cheese/veggie): ')
    bun = input('\tEnter type of Bun (white/wheat/gluten-free): ')
    patty_count = int(input('\tEnter number of patties: '))

    if burger_type.lower() == 'simple':
        burger = SimpleBurger(bun, patty_count)
        print(F"Added to cart: {burger}")
    elif burger_type.lower() == 'cheese':
        cheese_type = input('\tEnter type of Cheese (american/pepper jack): ')
        burger = CheeseBurger(bun, patty_count, cheese_type)
        print(F"Added to cart: {burger}")
    elif burger_type.lower() == 'veggie':
        toppings_input = input('\tEnter veggie toppings separated by commas: ')
        veggie_toppings = [t.strip() for t in toppings_input.split(',')] if toppings_input else []
        burger = VeggieBurger(bun, patty_count, veggie_toppings)
        print(F"Added to cart: {burger}")
    else:
        print('Invalid burger type.')

    choice = input('Would you like to add another burger to your order? (yes/no): ')

print('\n\n\t******** Printing Receipt *******\n')
cart = SimpleBurger.cart
for item in cart:
    print(item)
subtotal = cart.calc_subtotal()
tax = cart.calc_tax()
total = cart.calc_total()
print(F"\nSubtotal: ${subtotal:.2f}")
print(F"Tax: ${tax:.2f}")
print(F"Total: ${total:.2f}")
print("Thank you for your order!")



