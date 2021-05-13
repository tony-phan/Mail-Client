'''
Project 3: Mail Client
The goal of this programming assignment is to create a simple mail client that sends e-mail to
any recipient. Your client will need to establish a TCP connection with a mail server (e.g., a
Google mail server), dialogue with the mail server using the SMTP protocol, send an e-mail
message to a recipient (e.g., your friend) via the mail server, and finally close the TCP
connection with the mail server.

https://wiki.eecs.yorku.ca/course_archive/2012-13/W/3214/_media/socket_programming_jan2013.pdf
https://pythonprogramming.net/sockets-tutorial-python-3/
'''

import socket
import ssl
import base64
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver =  'smtp.gmail.com'
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((mailserver, 587))
recv = clientSocket.recv(1024)
print (recv)
if recv[:3] != '220':
    print ('220 reply not received from server.')

# Send HELO command and print server response.
command ='HELO Alice\r\n'
heloCommand = command.encode()
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print (recv1)

if recv1[:3] != '250':
    print ('250 reply not received from server.')

#Request an encrypted connection

command = 'STARTTLS\r\n'.encode()
clientSocket.send(command)
recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print ('220 reply not received from server')

#Encrypt the socket
clientSocket = ssl.wrap_socket(clientSocket)

# email and password for authentication
email = (base64.b64encode('jd2344813@gmail.com'.encode())+ ('\r\n').encode())
password= (base64.b64encode('qazxsw1357@'.encode())+ ('\r\n').encode())

#Authentication 
clientSocket.send('AUTH LOGIN \r\n'.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '334':
    print ('334 reply not received from server')

clientSocket.send(email)
recv1 = clientSocket.recv(1024).decode()
print(recv1)

if recv1[:3] != '334':
    print ('334 reply not received from server')

clientSocket.send(password)
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '235':
    print ('235 reply not received from server')


# Send MAIL FROM command and print server response.
clientSocket.send("MAIL FROM: <jd2344813@gmail.com>\r\n".encode())
recv2 = clientSocket.recv(1024).decode()
if recv2[:3] != '250':
    print ('250 reply not received from server.')

# Send RCPT TO command and print server response.
clientSocket.send("RCPT TO: <atranphan@cpp.edu>\r\n".encode())
recv2 = clientSocket.recv(1024).decode()
print (recv2)

# Send DATA command and print server response.
clientSocket.send("DATA\r\n".encode())
recv2 = clientSocket.recv(1024).decode()
print (recv2)

#Send data
clientSocket.send(("Subject: SMTP Email Test! \r\n").encode())
clientSocket.send(("To: atranphan@cpp.edu \r\n").encode())
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

# Send QUIT command and get server response.
clientSocket.send("QUIT\r\n".encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

#Close connection with client socket
clientSocket.close()

print('Mail sent and connection closed')