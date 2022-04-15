local currencies = {'EUR', 'USD', 'JPY', 'CAD'}
request = function()
  local method = "POST"
  local path = "http:///10.102.243.173:80/setCurrency"
  local headers = {}
  local currency = currencies[math.random(1,#currencies)]
  local body   = "currency_code=" ..  currency
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  return wrk.format(method, path, headers, body)
end
