# RandSploit

Experimental modular CLI toolkit for network and system operations featuring an interactive interpreter inspired by Metasploit

## Description

RandSploit is a project created as an attempt to build a flexible and extensible environment for working with infrastructure, networking, and cybersecurity tools.
The main goal was to design a custom CLI interpreter that allows dynamic loading of modules ("plugins") at runtime, along with unified management of their configuration and parameters.
The project is no longer actively developed and remains a proof-of-concept.
Further development has been moved to a new toolkit currently maintained in a private repository.

## Implemented Modules

- DNS Resolver
- TCP ECHO Server
- TCP ECHO Client
- TCP Proxy Server

## Example Usage

```
root@rand-sploit:~/RandSploit# ./randconsole.sh
Starting setup...
Ignoring pyreadline3: markers 'sys_platform == "win32"' don't match your environment
Collecting tabulate>=0.9.0 (from -r requirements.txt (line 2))
  Using cached tabulate-0.10.0-py3-none-any.whl.metadata (40 kB)
Collecting dnspython (from -r requirements.txt (line 3))
  Using cached dnspython-2.8.0-py3-none-any.whl.metadata (5.7 kB)
Using cached tabulate-0.10.0-py3-none-any.whl (39 kB)
Using cached dnspython-2.8.0-py3-none-any.whl (331 kB)
Installing collected packages: tabulate, dnspython
Successfully installed dnspython-2.8.0 tabulate-0.10.0
All done.
rand>help
╒═════════╤══════════════════════════════════════════════════╕
│ help    │ Print this page.                                 │
├─────────┼──────────────────────────────────────────────────┤
│ cls     │ Undocumented.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ session │ Undocumented.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ run     │ Run the chosen module.                           │
├─────────┼──────────────────────────────────────────────────┤
│ set     │ Set an option for the chosen module.             │
├─────────┼──────────────────────────────────────────────────┤
│ call    │ Call an OS command.                              │
├─────────┼──────────────────────────────────────────────────┤
│ back    │ Unchoose the module.                             │
├─────────┼──────────────────────────────────────────────────┤
│ reload  │ Reload the current module.                       │
├─────────┼──────────────────────────────────────────────────┤
│ opts    │ Get a list of all options for the chosen module. │
├─────────┼──────────────────────────────────────────────────┤
│ fg      │ Undocumented.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ mods    │ Get a list of all modules.                       │
├─────────┼──────────────────────────────────────────────────┤
│ edit    │ Undocumented.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ use     │ Use a module.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ search  │ Search for a module.                             │
├─────────┼──────────────────────────────────────────────────┤
│ dev     │ Enable developer mode (verbose exceptions).      │
├─────────┼──────────────────────────────────────────────────┤
│ exit    │ Quit the program.                                │
├─────────┼──────────────────────────────────────────────────┤
│ bg      │ Undocumented.                                    │
├─────────┼──────────────────────────────────────────────────┤
│ deps    │ Undocumented.                                    │
╘═════════╧══════════════════════════════════════════════════╛
rand>mods
╒═══╤═════════════════════════════════════════╕
│ 0 │ /root/RandSploit/Mods/EchoTCPServ.py    │
├───┼─────────────────────────────────────────┤
│ 1 │ /root/RandSploit/Mods/EchoTCPCli.py     │
├───┼─────────────────────────────────────────┤
│ 2 │ /root/RandSploit/Mods/DNSResolver.py    │
├───┼─────────────────────────────────────────┤
│ 3 │ /root/RandSploit/Mods/SimpleTCPProxy.py │
╘═══╧═════════════════════════════════════════╛
rand>use 2
DNSResolver>opts
╒════════╤═════════╤═══════════╤════════════╕
│ name   │ descr   │ value     │ required   │
╞════════╪═════════╪═══════════╪════════════╡
│ RHOST  │         │ localhost │ True       │
╘════════╧═════════╧═══════════╧════════════╛
DNSResolver>set RHOST google.com
DNSResolver>run
142.250.120.138
142.250.120.139
142.250.120.100
142.250.120.101
142.250.120.102
142.250.120.113
2a00:1450:4025:802::8a
2a00:1450:4025:802::8b
2a00:1450:4025:802::66
2a00:1450:4025:802::71
10 smtp.google.com.
The DNS response does not contain an answer to the question: google.com. IN CNAME
DNSResolver>call ls
Interpreter   Mods             OptionTemplate  Util             randconsole.py    setup.bat
ModBuilder    Option           README.en.md    randconsole.bat  randconsole.sh    setup.sh
ModInterface  OptionInterface  README.pl.md    randconsole.ps1  requirements.txt
DNSResolver>exit
```
