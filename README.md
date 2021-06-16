# SSL Certificates

Este projeto tem como objetivo automatizar a renovação de certificados SSL utilizados nas aplicações do cluster-tst e cluster-prd.

## Descrição

Este projeto foi desenvolvido com o intuito de evitar downtime dos produtos da Wiser Educação por problemas de expiração de certificados SSL.

A automação é responsável por verificar todos os dias, por meio de cronjob Kubernetes, se algum dos dominios contidos em [```./data/domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/data/domains.csv) (cluster-prd) e em [```./tests/.domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/tests/.domains.csv) (cluster-tst) estão próximos da data de expiração ou se já estão expirados, e em seguida adquirir novos certificados para cada um deles acessando os servidores do [Let's Encrypt](https://letsencrypt.org/). Cada certificado gerado é commitado neste repositório de maneira automática.

## Features

* Verificação das datas de expiração.
* Criação de novos certificados obtidos pela unidade certificadora [Let's Encrypt](https://letsencrypt.org/).
* Substituição da ```secret``` utilizada por cada aplicação do cluster Kubernetes que estão com data de expiração vencida ou faltando 7 dias para expirar.
* Os novos certificados gerados são adicionados automaticamente a este repositório e estão localizados no diretório [```./letsencrypt```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/letsencrypt/) neste repositório.

## Informações GCP

* Nome do cronjob no cluster-prd: [ssl-certificates](https://console.cloud.google.com/kubernetes/cronjob/us-central1/cluster-prd/default/ssl-certificates/details?project=wiseup-102030&pageState=(%22savedViews%22:(%22i%22:%221b8adbfc7809424d9c067661a01816bf%22,%22c%22:%5B%22gke%2Fus-central1%2Fcluster-prd%22%5D,%22n%22:%5B%5D)))
* Nome do cronjob no cluster-tst: [ssl-certificates](https://console.cloud.google.com/kubernetes/cronjob/us-central1-a/cluster-tst/default/ssl-certificates/details?project=wiseup-102030&pageState=(%22savedViews%22:(%22i%22:%221b8adbfc7809424d9c067661a01816bf%22,%22c%22:%5B%22gke%2Fus-central1-a%2Fcluster-tst%22%5D,%22n%22:%5B%5D)))
### Logs

Os logs referentes a cada job (POD) rodando diariamente podem ser vistos ao acessar o devido cluster Kubernetes no GCP consultando o workload [ssl-certificates](https://console.cloud.google.com/kubernetes/cronjob/us-central1/cluster-prd/default/ssl-certificates/details?project=wiseup-102030&pageState=(%22savedViews%22:(%22i%22:%221b8adbfc7809424d9c067661a01816bf%22,%22c%22:%5B%22gke%2Fus-central1%2Fcluster-prd%22%5D,%22n%22:%5B%5D))).
Os logs apresentam cada passo trilhado pelo app de automação.
O jsonPaylod apresentado no final do log de cada job é uma das informações mais importantes visto que traz informações mais detalhadas de cada certificado. O jsonPayload apresenta o seguinte formato de informações:

```
[
  {
    "domain": "buzzclub.com.br"
    "expiry_date": "2021-09-06T15:44:36",
    "is_expired": false,
    "5_days_or_less_to_expiry": false,
    "was_cert_replaced": false,
  }
]
```

### Notificações

*

## Pipelines

*

## Variáveis de Ambiente