# Segundo trabalho da disciplina de Sistemas Distribuídos

Este trabalho tem o objetivo de desenvolver um sistema em python que implemente uma espaço de dados compartilhado persistente, nos moldes do Linda Tuplespace (com as operações in, rd e out) que permita a implementação de um mini-blog com postagens de conteúdos por tópicos, sua leitura por tópicos e a retirada da mensagem somente por quem postou. Além disso, tem o objetivo de escrever um wrapper usando REST api neste sistema que permita a conexão de clientes remotos a este microblog se conectarem  através de REST. 

## Instruções

### Execução
Para executar o projeto você deve clonar o repositório e executar os seguintes comandos:
```sh
$ cd trab2SD
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install pyzmq
```
#### No primeiro terminal
```sh
$ python world.py
```
#### No segundo terminal
```sh
$ python start_sensores.py
```

### No terceiro terminal
```sh
$ python manager.py
```

### No quarto terminal
```sh
$ python subscriber.py username [id_sala]
```
Obs: é possível visualizar mais de uma sala simultaneamente passando-as por parâmetro.

----------------------------------------------------------------------
**Mariana Cavichioli Silva - 726568**

**Rafael Bastos Saito - 726580**
