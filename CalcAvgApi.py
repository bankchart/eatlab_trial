import requests

class CalcAvgApi(object):

  @staticmethod
  def __endpoint():
    return 'https://kasetpricev2.azurewebsites.net/api/product/getByNameIncludePrices/'

  @staticmethod
  def ma_avg(item, params, field):
    resp = requests.get(CalcAvgApi.__endpoint() + '/' + item, params)
    result = {}
    try:
      n = len(resp.json()['data']['prices'])
      unit = len(resp.json()['data']['subProducts']) > 0 and resp.json()['data']['subProducts'][0]['unit'] or 'N/A'
      tmp = []
      for obj in resp.json()['data']['prices']:
        tmp.append(obj[field])
      result['item'] = item
      result['unit'] = unit
      result['avg'] = round(sum(tmp)/n, 2)
      result['min'] = min(tmp)
      result['max'] = max(tmp)
      result['success'] = True
    except Exception as e:
      result = {
        'item': item,
        'success': False
      }
    return result