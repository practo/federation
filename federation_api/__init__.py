modules = [
    {
        'app': {
            'api': [
                'defaults'
            ]
        }
    }
]

for module in modules:
    for battalion, battalion_classes in module.iteritems():
        for squadron, squadron_classes in battalion_classes.iteritems():
            for squadron_class in squadron_classes:
                __import__('federation_api.{0}.{1}.{2}'.format(battalion,
                                                               squadron,
                                                               squadron_class))
