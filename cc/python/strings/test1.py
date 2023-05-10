import re

s = "sand1-web-aurora-db-aurora-node-0"

# s1 = re.sub('(\d+)(?!\d)', lambda x: str(int(x.group(0)) + 1), s)
print(s[-1])
if s[-1] == '0':
    new_s = s[:-1] + '1'
    print(new_s)
elif s[-1] == '1':
    new_s = s[:-1] + '0'
    print(new_s)

# print(s1)