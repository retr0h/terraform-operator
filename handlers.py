import kopf


@kopf.on.create("kopfexamples")
def create_fn(spec, name, meta, status, **kwargs):
    print(f"And here we are! Created {name} with spec: {spec}")
