# 2PL017
Effectively search the Exploit-DB

This script opens a GUI, written in python, to help find exploits from the exploit database, located in Kali linux in /usr/share/exploitdb.

At present, there are some limitations in the available tool "searchsploit", and the online search, including:
- Having to solve super annoying captchas.
- Needing to know the exact version for which the exploit is desinged. This makes searching for exploits a not very effective task, as it is very easy to overlook exploits, especially linux kernel exploits for privilege escalation.
- Having to concatenate several greps in super long commands to get the exploit needed.
- Having to use locate, cat, etc, a lot, just to determine if this exploit is what we are looking for.
- Failing to do the former, in an attempt to save time, sometimes results in compilation errors, for not reading the instructions on what flags to use for compilation.
- Wasting time when it is hard to find a working exploit from among many candidates, as it may be hard to keep track of which exploites were unsuccessful already, making us try the same exploit several times.
- Etc.
- For Linux Kernel exploits, the naming conventions are not very unified, and it is easy to overlook exploits that work for versions lower than a given version, or between a range of versions.

The goal of this tool is to simplify this process and is especially targeted towards kernel exploits, making an extensive use of regular expressions to capture all possible types of version nomenclatures, and automatically determining if the version we are looking for fits any exploits. Doing this by hand is a process full of potential errouneously discarded exploits. 

It also allows to read the content of each exploit in real time by just clicking on their name, and to easily copy or compile them to any location in our filesystem. Candidate exploits can be discarded by just clicking a button, so when we determine an exploit is not interesting for our case, it will not bother us anymore.

This program is a single python file, and the dependencies used are included in the standard python distribution. Tkinter is used for the GUI, so there is no need to install anything, it runs out of the box. The only requirement is that exploit database is located in /usr/share/exploitdb. This script scans the files.csv file to find exploits, and then looks for particular exploits in their corresponding location, normally in the subfolders under this same directory in Kali Linux.
