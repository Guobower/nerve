# Nerve Project #
is a **SYSTEM** 
that aims to **MONITOR** 
the health of each **COMPUTER** 
in a **NETWORK**
written in pure python

## Requirements ##
Nerve as 2 main components namely **Brain** that acts as the server and **Sense** that acts as the client

### Brain (Server) ###
 - Python 3.6.3
    - paramiko      2.3.1
    - cryptography  2.1.3

### Sense (Client) ###
 - Python 3.6.3
    - cryptography  2.1.3
    - psutil        5.4.0


## Installation ##
### Brain (Server) ###
Install python 3.6.3
 - [Windows](https://www.python.org/downloads/release/python-363/)
 - [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/#)
 - or if Ubuntu use the included shell script in the Source

       Source/bootstrap.sh

Install dependencies

    pip install -r Source/requirement.txt 
 
### Sense (Client) ###
Enable SSH (openSSH)
 - [Windows](https://winscp.net/eng/docs/guide_windows_openssh_server)
 - [Linux](https://www.tecmint.com/disable-or-enable-ssh-root-login-and-limit-ssh-access-in-linux/)

Install python 3.6.3
 - [Windows](https://www.python.org/downloads/release/python-363/)
 - [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/#)
 - or if Ubuntu use the included shell script to provision

       Source/bootstrap.sh

## Usage ##
    python runserver.py --database=sample.db --smtp-ip=127.0.0.1 --smtp-port=1025 --client-config=brain/config.xml \ 
                        --cipher-key KEY
    
# Simulation #
## Requirement ##
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Mailcatcher](https://mailcatcher.me/) _this will be install automatically once we ran the provisions_

Step 1: 
Create a Intranet Simulation in our case we use Vagrant to provision few clients.
_this my take few minutes to finish_
    
    vagrant up

Step 2:
run the server

    python runserver.py --database=sample.db --smtp-ip=192.168.100.200 --smtp-port=1025 \
                        --client-config=brain/config.xml --cipher-key KEY

Step 3:
open your favorite browser and open the below url to see the sent emails.

     http://192.168.100.200:1080/
     
### Output ###

    ============================================
    NERVE APPLICATION version 1
    BY Marc Philippe de Villeres
    ============================================
    ssh and sftp connection to 192.168.100.101:22 established
    client script sent
    message decrypted
    logs stored
    connection closed
    ============================================
    ssh and sftp connection to 192.168.100.102:22 established
    client script sent
    message decrypted
    logs stored
    connection closed
    ============================================
    sending email to client01@example.com
    Successfully sent email
    sending email to client02@example.com
    Successfully sent email


# Unittest #
## Requirement ##
Step 1: 
Assuming python 3.6 is available install the dependencies.

    pip install paramiko==2.3.1 cryptography==2.1.3 psutil==5.4.0 

Step 2: 
Run unittest

    python -m unittest discover -v

### Output ###

    ----------------------------------------------------------------------
    Ran 15 tests in 0.079s
    
    OK
 
# Note #
WINDOWS LOGS WERE NOT ADDRESS IN THIS IMPLEMENTATION AS WE DID NOT SPIN A WINDOWS MACHINE

# Reference Worth Reading #
 - [fstrings](https://cito.github.io/blog/f-strings/) is new to python 3.6 and deemed to perform better
 - [encryption and decryption](https://www.blog.pythonlibrary.org/2016/05/18/python-3-an-intro-to-encryption/) 

# Personal Assumptions and Remarks #
    1. decided to use python 3 as it is the new de facto of python and makes the code base ready for future improvements
    2. decided to not use an orm to demonstrate SQL knowledge
    3. decided to use sqlite as it is more than enough for the use case at hand
    4. decided to use cryptography as crypto is not actively maintained anymore, plus cryptography is easy to install 
       and use, and I think it is more than enough for the use case
    5. as I lack time to complete the unittests, I added # TODO for the functions that I think should have been tested
    6. decided to use mock for some functions in the test to make it easier to test.
    7. decided to use (VM) Vagrant instead of (Containers) Docker to automate the process of provisioning a simulation,
       as VM is the closest simulation of individual machines in the intranet. and I'm afraid that docker internal 
       networking mechanism might complicate everything.
    8. I think it is more inspiring and fun to name the project, that's why I named it Nerve :)
    9. I think the time allotted was too constraint. but still doable. 
    10.Overall the assignment/activity was fun. 
    
    I might have forgotten some of the comments and assumptions that I have.
    But let me say THANK YOU as it was fun and refreshing activity.
