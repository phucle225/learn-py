from app.mongo import customers
from functools import wraps

import jwt
key = "secret"
encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")
temp = encoded.decode()
print(encoded.decode())
print(encoded.__str__())
decode = jwt.decode(temp.encode(), key, algorithms="HS256")

print(decode)