modules = [
    "app"
]

for module in modules:
    __import__('federation_api.%s.api' % module)
