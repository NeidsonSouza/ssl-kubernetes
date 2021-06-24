# SSL Certificates

Este projeto tem como objetivo automatizar a renovação de certificados SSL utilizados nas aplicações do cluster-tst e cluster-prd.

## Descrição

Este projeto foi desenvolvido com o intuito de evitar downtime dos produtos da Wiser Educação por problemas de expiração de certificados SSL.

A automação é responsável por verificar todos os dias, por meio de um CronJob Kubernetes, se algum dos certificados listados em [```./data/domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/data/domains.csv) (cluster-prd) e em [```./tests/.domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/tests/.domains.csv) (cluster-tst) estão próximos da data de expiração ou se estão expirados. Em seguida a automação adquire novos certificados para cada um dos domínios listados acessando os servidores da [Let's Encrypt](https://letsencrypt.org/).

Cada certificado gerado é comitado neste repositório e substituído, nos clusters citados, de maneira automática.

O novo certificado configurado no cluster só será válido após a atualização do Ingress. Esta automação não faz atualização do Ingress, deixando isso por conta do agendamento nativo de atualização do mesmo tanto no cluster-tst quanto no cluster-prd.

## Features

* Verificação das datas de expiração.
* Criação de novos certificados obtidos por meio da unidade certificadora [Let's Encrypt](https://letsencrypt.org/).
* Substituição das ```secrets```, contidas no namespace ```proxy```, utilizadas por cada aplicação dos clusters, caso este armazene certificado com data de expiração que esteja dentro dos próximos 20 dias ou que já esteja expirado.
* Os novos certificados gerados são adicionados automaticamente a este repositório e estão localizados no diretório [```./letsencrypt```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/letsencrypt/).

## Base de dados

A automação utiliza dois arquivos CSV como base de dados:

* [```./data/domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/data/domains.csv) (clsuter-prd)
* [```./tests/.domains.csv```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/tests/.domains.csv) (cluster-tst)

No bloco de código abaixo podemos ver o tipo de conteúdo contido nesses dois arquivos:

```csv
secret,domain,domain_manager
buzzclub-certificate,buzzclub.com.br,cloudflare
wup.onl-certificate,wup.onl,aws
```
A primeira linha se refere ao cabeçalho:

* secret: se refere ao nome da secret configurada no namespace proxy do cluster kubernetes.

* domain: se refere ao domínio que está relacionado com a respectiva secret.

* domain_manager: se refere ao serviço responsável por gerenciar o domínio (cloudfare ou aws são os únicos valores reconhecidos).

Na segunda linha temos como exemplo os dados do domínio ```buzzclub.com.br``` configurado no cluster-prd e esses dados estão diretamente ligados com a ordem referenciada no cabeçalho. Ou seja:

* ```buzzclub-certificate```: secrets
* ```buzzclub.com.br```: domain
* ```cloudflare```: domain_manager

A mesma lógica se aplica a terceira linha do código acima:

* ```wup.onl-certificate```: secrets
* ```wup.onl```: domain
* ```aws```: domain_manager

OBS: É importante deixar claro que, na maioria das vezes, o nome das secrets no cluster-prd possuem padrões diferentes das secrets no cluster-tst mesmo quando se referem ao mesmo domínio e utilizam o mesmo certificado. Ex.:

* ```buzzclub-certificate```: cluster-prd
* ```buzzclub.com.br-certificate```: cluster-tst


## Informações GCP

* Nome do CronJob no cluster-prd: [ssl-certificates](https://console.cloud.google.com/kubernetes/cronjob/us-central1/cluster-prd/default/ssl-certificates/)
* Nome do CronJob no cluster-tst: [ssl-certificates](https://console.cloud.google.com/kubernetes/cronjob/us-central1-a/cluster-tst/default/ssl-certificates/)
### Logs

Os logs referentes à cada job (POD) rodado diariamente podem ser vistos ao acessar o CronJob ```ssl-certificates``` de cada cluster.

O jsonPaylod apresentado no final do log, traz informações mais detalhadas de cada certificado e possui o seguinte formato:

```json
[
  {
    "domain": "buzzclub.com.br",
    "expiry_date": "2021-09-06T15:44:36",
    "is_expired": false,
    "5_days_or_less_to_expiry": false,
    "was_cert_replaced": false,
  }
]
```
Neste log podemos ver os dados referente à um certificado:

* ```domain```: se refere ao domínio ao qual o certificado está atrelado.
* ```expiry_date```: data de expiração do certificado.
* ```is_expired```: informa se o certificado está expirado ou não.
* ```5_days_or_less_to_expiry```: Informa se o certificado está para expirar dentro de 5 dias ou menos. Quando o valor é ```true``` isso significa que houve falha na atualização, visto que a automação foi construída para atualizar os certificados faltando 20 dias para a data de expiração. Este dado é usado para enviar alerta de falha na atualização. Falaremos adiante sobre configuração de notificações.
* ```was_cert_replaced```: informa se o certificado foi atualizado naquele job em específico.

Um segundo ponto importante do log no GCP é a visualização de quais certificados serão atualizados, conforme mostrado no bloco de código abaixo:

```bash
Secrets to be upgraded: ['wiseupcorp.com-certificate', 'numberone.com.br-certificate', 'powerhouse.pro-certificate', 'wiser.cloud-certificate', 'wiseuplive.com.br-certificate']
```

Podemos ver no log acima quais secrets serão atualizadas por estar prestes a alcançar a data de expiração (faltando 20 dias ou menos).

### Métricas

Métricas configuradas no GCP:

* [was-cert-replaced-metric](https://console.cloud.google.com/logs/metrics?project=wiseup-102030): coleta dados referentes à atualização de certificado. Essa métrica está vinculada ao alerta [SSL - Atualizado](https://console.cloud.google.com/monitoring/alerting/policies/3457280891500976040?project=wiseup-102030).
* [is-there-expired-ssl-metric](https://console.cloud.google.com/logs/metrics?project=wiseup-102030): coleta dados referente à certificados expirados (em teoria esta métrica deve apresentar sempre o valor 0). Essa métrica está vinculada ao alerta [SSL - Expirado](https://console.cloud.google.com/monitoring/alerting/policies/12911683693827560920?project=wiseup-102030).
* [ssl-replaced-failed](https://console.cloud.google.com/logs/metrics?project=wiseup-102030): coleta dados referentes à certificados que faltam 5 dias ou menos para expirar. Isso significa que houve falha ao tentar atualizar o certificado, visto que cada certificado deve ser atualizado quando faltar 20 dias para expiração (em teoria esta métrica deve apresentar sempre o valor 0). Essa métrica está vinculada ao alerta [SSL - Falha na atualização](https://console.cloud.google.com/monitoring/alerting/policies/1567324046487602294?project=wiseup-102030).
### Notificações

A lista de emails que recebem os alertas é definida no ambiente de configuração dos mesmos.
## Pipelines

O [```bitbucket-pipelines.yml```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/bitbucket-pipelines.yml) roda o script [```./.build/build.sh```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/.build/build.sh/) passando o nome da deployment como argumento de entrada.

```yaml
script:
  - ./.build/build.sh $BITBUCKET_DEPLOYMENT_ENVIRONMENT
```

O pipeline faz o papel de criar o CronJob caso ele ainda não exista, e se ele já existir é feito apenas o upgrade do mesmo.
O processo de build utiliza o arquivo [```./.build/ssl-certificates-cronjob.yml```](https://bitbucket.org/wisereducacao/ssl-certificates/src/master/.build/ssl-certificates-cronjob.yml), que é um template yaml do tipo CronJob para ser utilizado pelo Kubernetes.

O pipeline ```upgrade-proxy-to-test```, do tipo custom, faz o deploy para o cluster-tst usando o arquivo ```./tests/.domains.csv``` como base de dados conforme pode ser visto nesse bloco de código do arquivo ```./.build/build.sh```:

```bash
cat tests/.domains.csv > data/domains.csv
```

O pipeline da branch ```master``` realiza o deploy para o cluster-prd e utiliza o arquivo original ```data/domains.csv``` como base de dados, não fazendo nenhuma alteração no mesmo.

## Variáveis de Ambiente

* ```SERVER```: Recebe a URL utilizada para acessar os servidores da [Let's Encrypt](https://letsencrypt.org/). Possíveis valores:

    * https://acme-v02.api.letsencrypt.org/directory: Utilizado para gerar certificados válidos para serem usados em produção.

    * https://acme-staging-v02.api.letsencrypt.org/directory: Utilizado para gerar certificados de teste. Útil para ser usando durante o desenvolvimento de apps.

* ```CLOUDFLARE_TOKEN```: Token de acesso a Cloudflare. Utilizado para  validar permissão para gerar certificados referentes à domínios hospedados na Cloudflare.

* ```AWS_ACCESS_KEY_ID```: ID de acesso a AWS. Utilizado juntamente com a senha (```AWS_SECRET_ACCESS_KEY```), a fim de validar permissão para gerar certificados referentes à domínios hospedados na AWS.

* ```AWS_SECRET_ACCESS_KEY```: Senha de acesso a AWS. Utilizado juntamente com o ID (```AWS_ACCESS_KEY_ID```), a fim de validar permissão para gerar certificados referentes à domínios hospedados na AWS.

* ```SERVICE_ACCOUNT```: Conteúdo do arquivo json referente à account service que autoriza a automação a executar comandos no cluster-tst e cluster-prd no GCP.

* ```BITBUCKET_USER```: Usuário de acesso a este repositório. Utilizado juntamente com a senha (```BITBUCKET_PASSWORD```) para realizar commit dos certificados gerados.

* ```BITBUCKET_PASSWORD```: Senha de acesso a este repositório. Utilizado juntamente com o usuário (```BITBUCKET_USER```) para realizar commit dos certificados gerados.
## Dependências

* Linux
* Python 3.6+
* Módulos Python:
    - pyOpenSSL:20.0.1
    - certbot-dns-cloudflare:1.13.0
* Docker
* Cluster Kubernetes
* Conta Letsencrypt
* Conta Cloudflare e/ou AWS
* Conta GCP

## Autor

Nome: Neidson Souza

Email: neidson.ds.souza@gmail.com
