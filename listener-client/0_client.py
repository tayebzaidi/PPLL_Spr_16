from multiprocessing.connection import Client

print 'trying to connect'
conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
print 'connection accepted'

print 'sending message'
conn.send('hello world')
print 'received message', conn.recv() 
conn.close()
