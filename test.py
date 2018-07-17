import dns.resolver

res = dns.resolver.Resolver()
res.nameservers = ['8.8.8.8']
ans = res.query('google.com', 'A')
for data in ans:
    print(data)

