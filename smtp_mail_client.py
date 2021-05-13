'''
Project 3: Mail Client
The goal of this programming assignment is to create a simple mail client that sends e-mail to
any recipient. Your client will need to establish a TCP connection with a mail server (e.g., a
Google mail server), dialogue with the mail server using the SMTP protocol, send an e-mail
message to a recipient (e.g., your friend) via the mail server, and finally close the TCP
connection with the mail server.
'''

import socket
import ssl
import base64
import re
import getpass
from typing import List

greeting_message = '''Welcome to the SMTP Mail Client! 
Please enter the letter of your chosen operation:
\ta) Send an email
\tb) Exit'''
option_prompt = 'Enter option: '
error_message = 'Invalid choice, please try again: '
sender_prompt = 'Enter the sender\'s email: '
num_recipients_prompt = 'Enter # of recipients: '
recipient_prompt = 'Enter the recipient\'s email: '
password_prompt = 'Password: '
message_prompt = 'Enter a message to send (Enter *END* to end the message):'
invalid_email_prompt = 'Invalid email format, please try again: '
mailserver =  'smtp.gmail.com'
end_message = '\r\n.\r\n'
email_subject = 'SMTP Mail Client'
port = 587
buffer_size = 1024

def validate_email(email: str) -> bool:
    '''
    Function to validate email input
    '''
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'   # Make a regular expression for validating an email
    if(re.search(regex, email)):
        return True
    else:
        return False

def get_message(input_prompt: str) -> str:
    '''
    Function to input user for a message to send to recipients. Message ends if *END* is typed on a blank line. 
    '''
    print(input_prompt)
    user_writing = [] 
    while True: 
        line = input() 
        if(line == '*END*'):    # end the message if *END* is entered 
            break 
        else: 
            user_writing.append(line) 
    user_writing = '\n'.join(user_writing)
    return user_writing

def get_recipients(num_recipients: int) -> List[str]:
    '''
    Prompt user for all recipient emails. Returns a list of strings
    '''
    recipients = []
    for i in range(num_recipients):
        recipient = input(recipient_prompt)
        while(not(validate_email(recipient))):
            recipient = input(invalid_email_prompt)
        recipients.append(recipient)
    return recipients

def validate_int(input_prompt: str) -> int:
    '''
    Function to validate integer input for number of recipients
    '''
    while(True):
        try:
            num_recipients = int(input(input_prompt))
            assert 0 < num_recipients
        except ValueError:
            print('Not an integer, try again.')
        except AssertionError:
            print('Enter an integer greater than 0, try again')
        else:
            return num_recipients

def mail_client():
    while(True):
        print(greeting_message)
        user_choice = input(option_prompt)
        while(not(user_choice == 'A' or user_choice == 'a' or user_choice == 'B' or user_choice == 'b')):
            user_choice = input(error_message)
        if(user_choice == 'B' or user_choice == 'b'):
            break

        # Get email & password of sender
        sender = input(sender_prompt)
        while(not(validate_email(sender))):
            sender = input(invalid_email_prompt)
        sender_password = getpass.getpass(prompt = password_prompt)

        # Get recipient emails
        num_recipients = validate_int(num_recipients_prompt)
        recipients = get_recipients(num_recipients)

        # Get message to send to all recipients
        message = get_message(message_prompt)
        message = '\r' + message

        for recipient in recipients:
            # Create socket called clientSocket and establish a TCP connection with mailserver
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((mailserver, port))

            # Receive confirmation that socket has connected to server
            recv = clientSocket.recv(buffer_size)
            print('Connecting socket to server...\nServer Response: ' + str(recv))
            if('220' not in str(recv)):
                print('220 reply not received from server.')

            # Send HELO command and print server response.
            command ='HELO there\r\n'
            heloCommand = command.encode()
            clientSocket.send(heloCommand)
            recv1 = clientSocket.recv(buffer_size)
            print('\nSending HELO command...\nServer Response: ' + str(recv1))
            if('250' not in str(recv1)):
                print('250 reply not received from server.')

            # Request an encrypted connection
            command = 'STARTTLS\r\n'.encode()
            clientSocket.send(command)
            recv = clientSocket.recv(buffer_size).decode()
            print('\nSending STARTTLS command...\nServer Response: ' + str(recv))
            if('220' not in str(recv)):
                print('220 reply not received from server.')

            # Encrypt the socket
            clientSocket = ssl.wrap_socket(clientSocket)

            # Email and password for authentication
            email = (base64.b64encode(sender.encode())+ ('\r\n').encode())
            password = (base64.b64encode(sender_password.encode())+ ('\r\n').encode())

            # Authentication 
            clientSocket.send('AUTH LOGIN \r\n'.encode())
            recv1 = clientSocket.recv(buffer_size).decode()
            print('Sending AUTH LOGIN command...\nServer Response: ' + str(recv1))
            if('334' not in str(recv1)):
                print('334 reply not received from server')
            clientSocket.send(email)
            recv1 = clientSocket.recv(buffer_size).decode()
            # print(recv1)
            if('334' not in str(recv1)):
                print('334 reply not received from server')
            clientSocket.send(password)
            recv1 = clientSocket.recv(buffer_size).decode()
            # print(recv1)
            if('235' not in str(recv1)):
                print('235 reply not received from server')

            # Send MAIL FROM command and print server response.
            clientSocket.send(f'MAIL FROM: <{sender}>\r\n'.encode())
            recv2 = clientSocket.recv(buffer_size).decode()
            print('Sending MAIL FROM command...\nServer Response: ' + str(recv2))
            if('250' not in str(recv2)):
                print('250 reply not received from server.')
            
            # Send RCPT TO command and print server response.
            clientSocket.send(f'RCPT TO: <{recipient}>\r\n'.encode())
            recv2 = clientSocket.recv(buffer_size).decode()
            print('Sending RCPT TO command...\nServer Response: ' + str(recv2))

            # Send DATA command and print server response.
            clientSocket.send('DATA\r\n'.encode())
            recv2 = clientSocket.recv(buffer_size).decode()
            print('Sending DATA command...\nServer Resposne: ' + str(recv2))

            # Send data
            clientSocket.send((f'Subject: {email_subject} \r\n').encode())
            clientSocket.send((f'To: {recipient} \r\n').encode())
            clientSocket.send(message.encode())

            # Message ends with a single period.
            clientSocket.send(end_message.encode())
            recv2 = clientSocket.recv(buffer_size).decode()

            # Send QUIT command and get server response.
            clientSocket.send('QUIT\r\n'.encode())
            recv2 = clientSocket.recv(buffer_size).decode()
            print('Sending QUIT command...\nServer Response: ' + str(recv2))

            # Close connection with client socket
            clientSocket.close()

            print('The email has been sent to ' + recipient)
        print()
        
if(__name__ == '__main__'):
    mail_client()