local products = {'0PUK6V6EV0','1YMWWN1N4O','2ZYFJ3GM2N','66VCHSJNUP','6E92ZMYYFZ','9SIQT8TOJO','L9ECAV7KIM','LS4PSXUNUM','OLJCESPC7Z'}
request = function()
  local method = "GET"
  local headers = {}
  local product = products[math.random(1,#products)]
  local path = "http:///10.102.243.173:80/product/" .. product
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  return wrk.format(method, path, headers, body)
end
