# Terraform Operator

Manages datacenter infrastructure through Terraform directly from
Kubernetes.

## Requirements

The requirements below assume you are operating on MacOS Catalina+.

* [Kind][]:

        $ brew install kind

## Developing

Start a development Kubernetes cluster.

    $ kind create cluster --name terraform-operator
    $ kubectl cluster-info --context terraform-operator

Apply the operator CRDs.

    $ kubectl apply -f config/crd/

Start the operator.

    $ make dep run

## Similar Projects

Mostly an excuse to use [Kopf][] to implement the [Operator pattern][].

* [danisla/terraform-operator][]
* [isaaguilar/terraform-operator][]

## License

The [MIT][] License.

[Kind]: https://kind.sigs.k8s.io/
[Operator pattern]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
[Kopf]: https://github.com/nolar/kopf
[danisla/terraform-operator]: https://github.com/danisla/terraform-operator
[isaaguilar/terraform-operator]: https://github.com/isaaguilar/terraform-operator
[MIT]: LICENSE
