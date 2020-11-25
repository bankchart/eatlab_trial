class FoodIngredients(object):

  def __init__(self, item, quantity, unit):
    self.item = item
    self.quantity = quantity
    self.unit = unit
    self.gram = 0
  
  def get_gram(self):
    self.quantity = self.quantity.replace(' ', '+')
    if self.unit == 'ช้อนชา':
      return (float(eval(self.quantity)) * 5)
    elif self.unit == 'ช้อนโต๊ะ':
      return (float(eval(self.quantity)) * 15)
    elif self.unit == 'มิลลิลิตร':
      return (float(eval(self.quantity)) * 1)
    elif self.unit == 'ลิตร':
      return (float(eval(self.quantity)) * 1000)
    elif self.unit == 'กรัม':
      return (float(eval(self.quantity)) * 1)
    elif self.unit == 'กก' or self.unit == 'กิโลกรัม':
      return (float(eval(self.quantity)) * 1000)
    else:
      return 0

  def food_ingredients_info(self):
    return 'Item: {}, Quantity: {}, Unit: {}'.format(self.item, self.quantity, self.unit)