# 2PL017
Effectively search the Exploit-DB

This script opens a GUI, written in python, to help find exploits from the exploit database, located in Kali linux in /usr/share/exploitdb. There is a video tutorial in https://www.youtube.com/watch?v=ysRmz4s58jM&t=700s

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


*** FORMATS ACCEPTED BY THE SEARCH TOOL FOR LINUX KERNEL EXPLOITS (as they are in /usr/share/exploitdb/files.csv) ***

- Exact kernel version (example: "Linux Kernel 2.6.10 - Local Denial of Service")
- Exploits under a certain value (example: "Linux Kernel < 2.6.16.18 - Netfilter NAT SNMP Module Remote Denial of Service")
- Exploits with "x" in the kernel version (example: "Linux Kernel 2.6.x - 'sys_timer_create()' Local Denial of Service"). In this case, "x" is accepted as the value we need if all the other non-x fields in the exploit version match.
- Exploit for kernels with release candidates, etc (example: "Linux Kernel 2.6.12-rc4 - 'ioctl_by_bdev' Local Denial of Service"). In this case, the extra stuff (-rc4, etc, is removed for simplicity)
- Exploit for a kernel version lower than some version (example: "Linux Kernel < 2.4.36.9/2.6.27.5 - Unix Sockets Local Kernel Panic (Denial of Service)",2008-11-11,"Andrea Bittau")
- Exploit for alternative versions (example: "Linux Kernel 2.6.27.7-generic/2.6.18/2.6.24-1 - Local Denial of Service"). Each alterntive is presented in a new line in the exploit list, with an index between parenthesis indicating which alternative is for a given version, like (1), (2), etc. This simplifies the program.
- Exploits for kernels lying inside a range of kernels (example: "Linux Kernel 2.6.9 < 2.6.25 (RHEL 4) - utrace and ptrace Local Denial of Service (1)",2008-06-25,"Alexei Dobryanov")

or any combination of the former.

======================================   SHORT TUTORIAL   ============================================
Last update: 14 Jan 2018

You can search exploits based on different criteria. For each of them, there is a certain filter. Most of the filters have the "negative" option. Checking the "neg?" box to the right side of a filter will apply negatively the filter. That is, excluding the matched results. To apply a filter, simply type on the corresponding field what you want to filter, and press enter.

- Name filter: show exploits containing the searched string in their name.
- Type filter: show exploits of a given type (dos, remote, local, etc).
- Format filter: show exploits of a given format (py, txt, c, etc).
- Index filter: show the exploit of the given exploit-db index.
- Kernel filter: show the "linux kernel" exploits that are compatible with the given exploit. As explained above, there are several ways of specifying kernel exploits in the exploit database. Using regular expresions, all the exploits relevant to the kernel version you type (it can have any number of "fields" separated by a dot ".", from one to four (that is, from x to x.x.x.x)).

Clicking on the selected exploit in the listbox display its contents in the large text field below. The contents of it can be directly edited in the text field, and a local copy can be created, both of the original exploit, or of the modified one, with the options at the bottom. 

The compilation command actually can also execute python scripts, or perl, etc. It uses a special syntax, where $out is the output path specified in the "output path" to the left of the compilation command, and $in is the input file, either the original one or the modified, as indicated by us.
