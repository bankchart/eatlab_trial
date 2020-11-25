from FoodIngredients import FoodIngredients

class Recipe(object):

  def __init__(self):
    self.name = ''
    self.link = ''
    self.food_ingredients: FoodIngredients = []

  def recipe_info(self):
    return 'Recipe: {}, Link: {}'.format(self.name, self.link)