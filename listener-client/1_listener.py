from multiprocessing.connection import Listener

listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
print 'listener starting'
while True:
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    m = conn.recv()
    print 'received message:', m
    conn.send('ok')
    conn.close()
    print 'connection closed'
listener.close()
