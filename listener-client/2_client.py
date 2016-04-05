from multiprocessing.connection import Client

for i in range(5):
    print 'trying to connect'
    conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
    print 'connection accepted'
    message = raw_input('Message to send? ')
    print 'sending message'
    conn.send(message)
    print 'received message', conn.recv() 
    conn.close()

