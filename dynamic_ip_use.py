import requests
f = open("proxy.txt")

lines = f.readlines()

proxy_array = []

for i in lines:
    proxy_array.append(i.strip("\n"))

url = "http://ip.chinaz.com/getip.aspx"
for item in proxy_array:
    try:
        resp = requests.get(url,proxies={
            'http':item
        })
        print(resp.content.decode())
    except Exception as e:
        print(e)
        continue
