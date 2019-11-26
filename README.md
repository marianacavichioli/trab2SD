# Segundo trabalho da disciplina de Sistemas Distribuídos

Este trabalho tem o objetivo de desenvolver um sistema em python de coleta e monitoramenfo de temperatura para todas salas do DC.

## Passos
- Construa um nó coletor de dados (processo) (simule a variação de temperatura) que colete dados a cada segundo,
- Empacote os dados em um envelope (xml ou json), e publique em um broker (ZeroMQ) (topico = temp, n.sala).
- Crie processos recipientes (pelo menos 1 para cada coletor) ("subscribers" do topico) responsáveis por armazenar a média  das últimas 10 leituras em formato "log historico" <sala n, time stamp, temp>.
- Monitore monitore um minimo de 8 salas. Publicadores e consumidores (subscribers)  devem rodar em maquinas diferentes.
- Ao final do projeto crie um cliente de visualização da temperatura das salas, incluindo histórico  (gráfico ou txt).

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

#### No terceiro terminal
```sh
$ python manager.py
```

#### No quarto terminal
```sh
$ python subscriber.py username [id_sala]
```

### Observação: 
É possível monitorar mais de uma sala simultaneamente passando-as por parâmetro.

- Salas disponíveis:
  - LE1
  - LE2
  - LE3
  - LE4
  - LE5
  - LE6
  - LE7
  - LE8
  
Também será gerado um arquivo para cada sala com o histórico de atualizações de temperaturas.

----------------------------------------------------------------------
**Mariana Cavichioli Silva - 726568**

**Rafael Bastos Saito - 726580**
