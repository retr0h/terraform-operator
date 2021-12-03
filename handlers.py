import kopf
import pykube


class Example(pykube.objects.NamespacedAPIObject):
    version = "tfo.retr0h.github.com/v1"
    endpoint = "kopfexamples"
    kind = "KopfExample"



@kopf.on.create("tfo.retr0h.github.com", "v1", "kopfexamples")
def create_fn(spec, **kwargs):
    job = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        # "metadata": {
        #     "name": "pi-with-ttl",
        # },
        "spec": {
            "ttlSecondsAfterFinished": 100,
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "pi",
                            "image": "perl",
                            "command": ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"],
                        }
                    ],
                    "restartPolicy": "Never",
                }
            },
        },
    }

    # objs = [{"kind": "Job"}]
    # kopf.harmonize_naming(objs, forced=True, strict=True)
    kopf.harmonize_naming(job)
    kopf.label(job, {"label1": "value1", "label2": "value2"})
    print("#" * 20)
    print(job)
    print("#" * 20)

    api = pykube.HTTPClient(pykube.KubeConfig.from_env())
    j = pykube.objects.Job(api, job)
    kopf.adopt(j)
    j.create()

    return {
        "status": {
            "children": j.metadata["uid"],
        }
    }


# @kopf.on.event(
#     "",
#     "batch/v1",
#     "jobs",
#     labels={"label1": "value1", "label2": "value2"},
# )
# def create_shiz_fn(spec, **kwargs):
#     parent_name = meta["labels"]


# @kopf.on.event(
#     "",
#     "v1",
#     "configmaps",
#     labels={"some-label": "somevalue"},
# )
# def cru_fn(body, event, logger, **kwargs):
#     print(f"Body: {body}")
#     print(f"Event: {event}")
#     print(f"Logger: {logger}")
#     print(f"kwargs: {kwargs}")
#     return {"message": "hello world"}

###

@kopf.on.create(
    "batch",
    "v1",
    "jobs",
    field="status.active",
    value=1,
    labels={"label1": "value1", "label2": "value2"},
)
def my_job_complete_fn(meta, name, namespace, status, **_):
    print("HERE")
    print("HERE")
    print("HERE")
    print("HERE")

    owner_reference = meta["ownerReferences"][0]

    api = pykube.HTTPClient(pykube.KubeConfig.from_env())
    parent = Example.objects(api).get_by_name(owner_reference["name"])
    statuses = parent.obj['status']
    # statuses["conditions"] = []
    # statuses["conditions"].append(status)
    parent.patch({"status": statuses})

    #print(f"statuses: {statuses}")

@kopf.on.update(
    "batch",
    "v1",
    "jobs",
    field="status.succeeded",
    value=1,
    labels={"label1": "value1", "label2": "value2"},
)
def my_job_update_fn(meta, name, namespace, status, **_):
    print("UPDATE")
    print("UPDATE")
    print("UPDATE")
    print(f"meta: {meta}")
    print(f"name: {name}")
    print(f"namespace: {namespace}")
    print(f"status: {status}")

    owner_reference = meta["ownerReferences"][0]

    api = pykube.HTTPClient(pykube.KubeConfig.from_env())
    parent = Example.objects(api).get_by_name(owner_reference["name"])
    statuses = parent.obj['status']
    # statuses["conditions"] = []
    # s = status["conditions"][0]
    # statuses["conditions"].append(s)

    # print(f"statuses: {statuses}")


# @kopf.on.event(
#    "batch/v1",
#    "jobs",
#    labels={"label1": "value1", "label2": "value2"},
# )
# def my_handler(event, meta, name, namespace, status, **spec):
#    print(f"DEWEY : {event}")
#    #owner_reference = meta["ownerReferences"][0]
#    #api = pykube.HTTPClient(pykube.KubeConfig.from_env())
#    #parent = Example.objects(api).get_by_name(owner_reference["name"])

#    #statuses = parent.obj['status']
#    #statuses["conditions"] = [{"status": "pending"}]
#    ##statuses["conditions"].append({"status": "one"})
#    ##statuses["conditions"].append({"status": "two"})

#    #print(f"parent : {parent.obj['status']}")
#    ## parent.patch({"status": {"conditions": [{"status": "pending"}]}})
#    ## status : {'startTime': '2021-07-19T22:41:19Z', 'active': 1}
#    ## parent.patch({"status": {"conditions": [{"status": "one"}]}})
#    ## parent.patch({"status": {"conditions": [{"status": "two"}]}})

#    #try:
#    #    status["conditions"][0]["type"]
#    #    # parent.patch({"status": {"conditions": [{"status": "completed"}]}})
#    #except KeyError:
#    #    pass


## status:
##   conditions:
##     - lastProbeTime: null
##       lastTransitionTime: "2021-07-19T06:01:09Z"
##       status: "True"
##       type: Initialized

## status:
##   completionTime: "2021-07-19T21:03:08Z"
##   conditions:
##     - lastProbeTime: "2021-07-19T21:03:08Z"
##       lastTransitionTime: "2021-07-19T21:03:08Z"
##       status: "True"
##       type: Complete
##   startTime: "2021-07-19T21:02:58Z"
##   succeeded: 1
