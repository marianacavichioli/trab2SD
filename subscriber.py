from exchange.user import Subscriber
from sys import argv

"""
To run this code use:

python3 subscriber.py username [sala1] [sala2] .. [salaN]

"""

def main(sala=None):
    # Setting default values
    user = "Guest"
    if sala is None:
        list_sala = ["LE1"]
    else:
        list_sala = []

    # Getting the username
    if len(sala) > 1:
        user = sala[1]

    # Getting which salas it wants to monitor
    if len(sala) > 2:
        for i in range(2,len(sala)):
            list_sala.append(sala[i])
    
    # Creating the subscriber and start listening to this monitor
    m = Subscriber(sala_id_list=list_sala, username=user)
    m.listen()

if __name__ == "__main__":
    main(argv)