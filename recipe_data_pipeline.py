from Recipe import Recipe
from FoodIngredients import FoodIngredients
from CalcAvgApi import CalcAvgApi

import bs4
import requests
import re
import json

# Task 1

def main():
  resp = requests.get('https://food.mthai.com/food-recipe/page/3')
  selector = 'h3.entry-title'
  html_page = bs4.BeautifulSoup(resp.text, 'html.parser')
  menu_elm = html_page.select(selector)
  menus = []
  for elm in menu_elm:
    recipe = Recipe()
    found_elm = elm.findAll('a', attrs={'href': re.compile('^https://'), 'rel': 'bookmark'})

    if len(found_elm) > 0 and re.search('^(สูตร|วิธีทำ)', found_elm[0].text):
      recipe.name = found_elm[0].text.strip()
      recipe.link = found_elm[0].get('href')
      recipe.food_ingredients = find_food_ingredients(recipe.name, recipe.link)
      menus.append(recipe)

  menu_input = input('Enter menu: ')
  print('\nProcessing...\n')
  forecast_prices = find_forecast_items_price()
  for menu in menus:
    if menu.name == menu_input.strip():
      fixed_prices = read_fixed_price()
      summary_price = {
        'avg': 0,
        'min': 0,
        'max': 0
      }
      for recipe in menu.food_ingredients:
        found_forecase_item = False

        for key in forecast_prices:
          if forecast_prices[key]['success'] and re.search('(เนื้อหมู|เนื้อวัว|เนื้อไก่|นม)', forecast_prices[key]['item']):
            found_forecase_item = True
            summary_price['avg'] += (forecast_prices[key]['avg'] * recipe.get_gram()) / 1000
            summary_price['min'] += (forecast_prices[key]['min'] * recipe.get_gram()) / 1000
            summary_price['max'] += (forecast_prices[key]['max'] * recipe.get_gram()) / 1000
            break
          
          if forecast_prices[key]['success'] and re.search('ไข่', forecast_prices[key]['item']):
            found_forecase_item = True
            summary_price['avg'] += forecast_prices[key]['avg'] * recipe.quantity
            summary_price['min'] += forecast_prices[key]['min'] * recipe.quantity
            summary_price['max'] += forecast_prices[key]['max'] * recipe.quantity
            break

        if found_forecase_item:
          continue

        for item, price in fixed_prices:
          if re.search(rf"{item}", recipe.item):
            summary_price['avg'] += (price * recipe.get_gram()) / 1000
            summary_price['min'] += (price * recipe.get_gram()) / 1000
            summary_price['max'] += (price * recipe.get_gram()) / 1000
      
      print('cost average: {}, min: {}, max: {}'.format(round(summary_price['avg'], 2), round(summary_price['min'], 2), round(summary_price['max'], 2)))
      return None

  print('Your menu doesn\'t exist')

def find_food_ingredients(recipe: str, link: str):
  food_ingredients = []
  regx = '([ 0-9/ ]+)(ช้อนชา|ช้อนโต๊ะ|กรัม|มิลลิลิตร|ฟอง|ลิตร|กก|กิโลกรัม)'
  print('##### {} #####'.format(recipe))
  resp = requests.get(link)
  selector = 'p + ul'
  recipe_page = bs4.BeautifulSoup(resp.text, 'html.parser')
  items_elm = recipe_page.select_one(selector)
  
  if items_elm == None:
    print('Not found')
    print()
    return None

  cnt = 0
  for li in items_elm.findAll('li'):
    cnt += 1
    if cnt == 1:
      print('วัตถุดิบ')
    li_elm_txt = li.text.strip()
    transform_result = transform_qty_unit(regx, li_elm_txt)
    detail = transform_result is not None and ', qty: {}, unit: {}'.format(transform_result['qty'], transform_result['unit']) or ''
    print('{}. {} {}'.format(cnt, li_elm_txt, detail))

    found = re.search(regx, li_elm_txt)
    if (found):
      food_ingredients.append(FoodIngredients(li.text.strip(), transform_result['qty'], transform_result['unit']))    
    else: 
      food_ingredients.append(FoodIngredients(li.text.strip(), 'N/A', 'N/A'))

  print()
  return food_ingredients

def find_forecast_items_price():
  period_params = {
    'from': '2020-10-25',
    'to': '2020-11-25'
  }
  result = {
    'pork': CalcAvgApi.ma_avg('เนื้อหมู', period_params, 'avgPrice'),
    'beef': CalcAvgApi.ma_avg('เนื้อวัว', period_params, 'avgPrice'),
    'chicken': CalcAvgApi.ma_avg('เนื้อไก่', period_params, 'avgPrice'),
    'egg': CalcAvgApi.ma_avg('ไข่', period_params, 'avgPrice'),
    'milk': CalcAvgApi.ma_avg('นม', period_params, 'avgPrice')
  }
  return result 

def transform_qty_unit(regx, str):
  match = re.search(regx, str)
  if (match):
    return {
      'qty': match.group(1).strip(),
      'unit':  match.group(2)
    }
  else:
    return None

def read_fixed_price():
  try:
    f = open('data_unit_per_kg.json')
    item_json = json.load(f)
    return item_json.items()
  finally:
    f.close()

main()