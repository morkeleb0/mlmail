'''
- Initial goals
-- open an IMAP box
-- Fetch messages
-- Read headers
-- Perform statistical analysis of IPs and URLs and decide if they're malicious
-- Take actions based on results (respond, delete, bin, etc)

'''
import imaplib, getpass, re
from pprint import pprint

def open_connection(verbose=False):

    # Login to our account
    hostname = 'imap.gmail.com'
    username = 'wlefevers@gmail.com'
    message = "Password for user "+username+"?"
    password = getpass.getpass(message)
    
    if verbose: print 'Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname, 993)

    if verbose: print 'Logging in as', username
    connection.login(username, password)
    return connection

def parse_list_response(line):
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)

def list_inbox(c, verbose=False):
    unused, data = c.list()
    folders = []
    for line in data: 
        flags, delimiter, mailbox_name = parse_list_response(line)
        folders.append(c.status(mailbox_name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)') )
    return folders

def read_message(c):
    ret, data = c.select('INBOX',readonly=True)
    typ, msg_data = c.fetch('1', '(BODY.PEEK[HEADER] FLAGS)')
    pprint(msg_data)
    return msg_data

if __name__ == '__main__':
    connection = open_connection(verbose=True)
    try:
        folders = list_inbox(connection)
        read_message(connection)
    finally:
        connection.logout()
