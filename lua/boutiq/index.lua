request = function()
  local method = "GET"
  local path = "http:///10.102.243.173:80/"
  local headers = {}
  local body
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  return wrk.format(method, path, headers, body)
end
