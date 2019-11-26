from exchange.user import Subscriber
from sys import argv


def main(sala=None):

    user = "Guest"
    if sala is None:
        list_sala = ["LE1"]
    else:
        list_sala = []

    # Pegando o username
    if len(sala) > 1:
        user = sala[1]

    # Obtendo quais salas deseja-se monitorar
    if len(sala) > 2:
        for i in range(2,len(sala)):
            list_sala.append(sala[i])
    
    # Criando o subscriber e começando a acompanhar o monitor
    m = Subscriber(sala_id_list=list_sala, username=user)
    m.listen()

if __name__ == "__main__":
    main(argv)