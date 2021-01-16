import fabric
from fabric import Connection
c = Connection(
    host='ec2-52-86-239-251.compute-1.amazonaws.com', 
    user='cobotrobot', 
    port=22,
    connect_kwargs={
        "key_filename": "/home/runner/.ssh/id_rsa",
    },)
result = c.run('uname -s')
print (result)