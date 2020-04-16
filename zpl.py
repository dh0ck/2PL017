#!/usr/bin/python

# 2PL017, 2017
# I used some of this stuff to start building the GUI:
# https://www.daniweb.com/programming/software-development/code/216827/working-with-a-tkinter-listbox-python
'''MIT License

Copyright (c) 2017 dh0ck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

logo = ("")
'''"                                    \n" +
"               __                   \n" +
"              /\ \                  \n" +
"             / /\ \                 \n" +
"            / /  \ \                \n" +
"           / /____\_\               \n" +
"          /_/________\              \n")'''


import subprocess
from Tkinter import *
import tkFileDialog
import re
import glob
import random
import os.path

ALL = W+E+N+S

root = Tk()
root.title("2PL017")

row_logo = 0
row_filters = 1
row_filters1 = 2
row_filters = 3
row_filters_a=4
row_listbox = 5
row_buttons_top = 6
row_title = 7
rowcontents = 8
row_new_name = 9
row_buttons_bottom = 10

main_width = 50

f1 = re.compile('Kernel ((\d+|x)\.)*(\d+|x)') # extact kernel version match
f2 = re.compile('Kernel < ((\d+|x)\.)*(\d+|x)') # only upper limit
f3 = re.compile('Kernel ((\d+|x)\.)*(\d+|x) < ((\d+|x)\.)*(\d+|x)') # between lower and upper version
f4 = re.compile('Kernel (((\d+|x)\.)*(\d+|x)/)+((\d+|x)\.)*(\d+|x)') # alternative versions
f4a = re.compile('((\d+|x)\.)+(\d+|x)-') # to remove release candidates, etc from list
f5 = re.compile('(((\d+|x)\.)*(\d+|x)/)+((\d+|x)\.)*(\d+|x)') # alternative versions (used for replacing all alternatives with just one when generating the initial list)
f6 = re.compile('Kernel (< )*((((\d+|x)(-\d+)*\.)+(\d+|x)((-[a-zA-Z]*[0-9]*(\+)*)*)*((( )*\/( )*| )((\d+|x)\.)+(\d+|x)(-[a-zA-Z]*[0-9]*)*)*)*( < )*)*') #all possible complex combinations I could find
f7 = re.compile('(-|_)([a-zA-Z]*[0-9]*\+*)*')


class Application(Frame):
        def __init__(self, master=None):
                Frame.__init__(self, master)
                self.grid(sticky=ALL)
                for r in range(8):
                        if r == row_listbox or r == rowcontents:
                                self.master.rowconfigure(r,weight=1)
                for c in range(1):
                        self.master.columnconfigure(c, weight=1)
                colors = ['red','orange','blue','green','yellow','salmon']
                l0 = Label(root, text=logo, font=("Monospace",6), fg=random.choice(colors))
                l0.grid(row=row_logo, column=0)

                frame1 = Frame(root, width=main_width)
                frame1.grid(row=row_filters, column=0, sticky=E+W)

                self.name_filter = Entry(frame1)
                self.name_filter.insert(END, "Name")
                self.name_filter.pack(fill=X,side=LEFT, expand=True)
                self.name_filter.bind('<Return>', self.apply_name_filter)
                self.name_filter.bind('<KP_Enter>', self.apply_name_filter)

                self.var_name = IntVar()
                self.neg_name = Checkbutton(frame1, text="neg?", variable=self.var_name)
                self.neg_name.pack(fill=X,side=LEFT)



                self.type_filter = Entry(frame1)
                self.type_filter.bind('<Return>', self.apply_type_filter)
                self.type_filter.bind('<KP_Enter>', self.apply_type_filter)
                self.type_filter.insert(END, "Type")
                self.type_filter.pack(fill=X,side=LEFT,expand=True) 
                self.var_type = IntVar()
                self.neg_type = Checkbutton(frame1, text="neg?", variable=self.var_type)
                self.neg_type.pack(fill=X,side=LEFT)

                self.button_kernel = Button(frame1,text="Kernel",command=self.kernel_name)
                self.button_kernel.pack(side=LEFT)

                self.version_filter = Entry(frame1)
                self.version_filter.bind('<Return>', self.apply_version_filter)
                self.version_filter.bind('<KP_Enter>', self.apply_version_filter)
                self.version_filter.insert(END, "Linux Kernel Version")
                self.version_filter.pack(fill=X,side=LEFT, expand=True)

                frame_a = Frame(root, width=main_width)
                frame_a.grid(row=row_filters_a, column=0, sticky=E+W)

                self.index_filter = Entry(frame_a)
                self.index_filter.bind('<Return>', self.apply_index_filter)
                self.index_filter.bind('<KP_Enter>', self.apply_index_filter)
                self.index_filter.insert(END, 'E-DB index')
                self.index_filter.pack(fill=X, side=LEFT, expand=True)


                self.format_filter = Entry(frame_a)
                self.format_filter.bind('<Return>', lambda event, fmt='$check': self.apply_format_filter(fmt))
                self.format_filter.bind('<KP_Enter>', lambda event, fmt='$check': self.apply_format_filter(fmt))
                self.format_filter.insert(END, 'Format')
                self.format_filter.pack(fill=X, side=LEFT, expand=True)

                self.button_py = Button(frame_a,text=".py",command=lambda fmt='py': self.apply_format_filter(fmt))
                self.button_py.pack(side=LEFT, expand=True, fill=X)

                self.button_pl = Button(frame_a,text=".pl",command=lambda fmt='pl': self.apply_format_filter(fmt))
                self.button_pl.pack(side=LEFT, expand=True, fill=X)

                self.button_c = Button(frame_a,text=".c",command=lambda fmt='c': self.apply_format_filter(fmt))
                self.button_c.pack(side=LEFT, expand=True, fill=X)

                self.button_rb = Button(frame_a,text=".rb",command=lambda fmt='rb': self.apply_format_filter(fmt))
                self.button_rb.pack(side=LEFT, expand=True, fill=X)

                self.button_sh = Button(frame_a,text=".sh",command=lambda fmt='sh': self.apply_format_filter(fmt))
                self.button_sh.pack(side=LEFT, expand=True, fill=X)

                self.button_php = Button(frame_a,text=".php",command=lambda fmt='php': self.apply_format_filter(fmt))
                self.button_php.pack(side=LEFT, expand=True, fill=X)

                self.button_java = Button(frame_a,text=".java",command=lambda fmt='java': self.apply_format_filter(fmt))
                self.button_java.pack(side=LEFT, expand=True, fill=X)

                self.button_txt = Button(frame_a,text=".txt",command=lambda fmt='txt': self.apply_format_filter(fmt))
                self.button_txt.pack(side=LEFT, expand=True, fill=X)

                self.button_txt = Button(frame_a,text=".html",command=lambda fmt='html': self.apply_format_filter(fmt))
                self.button_txt.pack(side=LEFT, expand=True, fill=X)

                self.var_fmt = IntVar()
                self.neg_fmt = Checkbutton(frame_a, text="neg?", variable=self.var_fmt)
                self.neg_fmt.pack(fill=X,side=LEFT)                
                
                '''____________________________________________'''

                frame2 = Frame(root, width=main_width)
                frame2.grid(row=row_buttons_top, column=0, sticky=E+W)

                self.label_count = Label(frame2, text='')
                self.label_count.pack(side=LEFT)
                # button to modify filter list
                                
                self.button1 = Button(frame2, text='Save lines to file', command=self.save_list)
                self.button1.pack(fill=X,side=RIGHT,expand=True)

                # button to delete a line from listbox
                self.button2 = Button(frame2, text='Discard exploit', command=self.delete_item)
                self.button2.pack(fill=X,side=RIGHT,expand=True)

                '''____________________________________________'''

                frame3 = Frame(root, width=main_width)
                frame3.grid(row=row_filters1, column=0,sticky=E+W)

                filt_label = Label(frame3,text='Applied filters: ')
                filt_label.pack(side=LEFT)
                # use entry widget to display filters
                self.enter1 = Entry(frame3)
                self.enter1.pack(fill=X,side=LEFT, expand=True)
                
                # pressing the return key will update the filters
                ####HACER ESTO, QUE PUEDA COGER EL TEXTO DE AQUI, DETECTAR SI SE HA BORRADO ALGUN FILTRO, Y ACTUALIZAR LISTA
                #enter1.bind('<Return>', set_filters)
                # or double click left mouse button to update line
                #enter1.bind('<Double-1>', list_filters)
                self.clr_but = Button(frame3, text='Clear filters', command=self.clr_filters)
                self.clr_but.pack(side=LEFT)

                '''____________________________________________'''

                # create the listbox (note that size is in characters)
                self.listbox1 = Listbox(root)#, width=50, height=6)
                self.listbox1.grid(row=row_listbox, column=0,columnspan=1,sticky="ew")

                # create a vertical scrollbar to the right of the listbox
                yscroll = Scrollbar(command=self.listbox1.yview, orient=VERTICAL)
                yscroll.grid(row=row_listbox, column=1, sticky=N+S)
                self.listbox1.configure(yscrollcommand=yscroll.set)

                # left mouse click on a list item to display selection
                self.listbox1.bind('<ButtonRelease-1>', self.get_list)

                '''____________________________________________'''
                
                frame_title = Frame(root, width=main_width)
                frame_title.grid(row=row_title, column=0,columnspan=1,sticky=E+W)
                title_label=Label(frame_title, text='Selected exploit: ')
                title_label.pack(side=LEFT)
                self.title_box = Entry(frame_title)
                self.title_box.pack(side=LEFT, expand=True, fill=X)

                frame_text=Frame(root,width=main_width)
                frame_text.grid(row=rowcontents,column=0,columnspan=1,sticky='ewns')
                self.contents = Text(frame_text)
                #self.contents.grid(row=rowcontents, column=0, columnspan=1,sticky='ewns')
                self.contents.pack(side=LEFT, expand=True, fill=X)
                coltext=0
                yscroll1 = Scrollbar(command=self.contents.yview, orient=VERTICAL)
                yscroll1.grid(row=rowcontents, column=coltext+1, sticky=N+S)
                self.contents.configure(yscrollcommand=yscroll1.set)
                xscroll1 = Scrollbar(command=self.contents.xview, orient=HORIZONTAL)
                xscroll1.grid(row=rowcontents+1, column=coltext, sticky=W+E)
                self.contents.configure(xscrollcommand=xscroll1.set)

                '''___________________________________________'''

                frame4 = Frame(root, width=main_width)
                frame4.grid(row=row_new_name, column=0,sticky=E+W)

                self.var_tmp = IntVar()
                self.neg_fmt = Checkbutton(frame4, text="Use temp?", variable=self.var_tmp)
                self.neg_fmt.pack(side=LEFT)
                
                self.output_button = Button(frame4,text='Output path: ',command=self.set_out)
                self.output_button.pack(side=LEFT)
                suggested_path = '/var/www/html/'
                self.enter2 = Entry(frame4)
                self.enter2.insert(END, suggested_path)
                self.enter2.pack(side=LEFT, fill=X, expand=True)

                self.compile_label = Label(frame4,text='Compilation command: ')
                self.compile_label.pack(side=LEFT)
                suggested_gcc = 'gcc path -o name'
                self.enter3 = Entry(frame4)
                self.enter3.insert(END, suggested_gcc)
                self.enter3.pack(side=LEFT, fill=X, expand=True)

                frame5 = Frame(root, width=main_width)
                frame5.grid(row=row_buttons_bottom, column=0,sticky=E+W)

                self.but_copy = Button(frame5, text="Copy", command=self.copy_file)
                self.but_copy.pack(side=LEFT, fill=X, expand=True)

                self.but_compile = Button(frame5, text="Compile", command = self.compile_file)
                self.but_compile.pack(side=LEFT, fill=X, expand=True)


                self.curr_index = 0
                db_path = "/usr/share/exploitdb/"
                path1 = "/usr/share/exploitdb/files.csv"
                if not os.path.isfile(path1):
                        path1 = "/usr/share/exploitdb/files_exploits.csv"
                path = path1
                filters = []
                f = open(path, 'r')
                self.lines = f.readlines()
                f.close()

                self.filtered_old = self.lines
                self.filtered_new = []

                self.currently_selected = '' #keeps in memory what exploit has last been selected

                self.index_index = {} #dictionary to make the correspondence between exploit id and position in list
                #clean_rc_etc()
                self.fill_with_all()
                #self.count = self.count_zploits()
                #self.label_count = Label(frame2, text=self.count)
                #self.label_count.pack(side=LEFT)

        def fill_with_all(self):
                self.listbox1.delete(0,END)
                for k, line in enumerate(self.lines):
                        if k >0:
                                alts = self.alternatives(line)
                                for j, alt in enumerate(alts):
                                        index = alt.split(',')[0].strip('"')
                                        file_name = alt.split(',')[1].strip('"')
                                        format_type = file_name.split('.')[-1]
                                        title = alt.split(',')[2].strip('"')
                                        type_ = alt.split(',')[6].strip('"')
                                        self.index_index[index]=k
                                        if j == 0:
                                                t=1
                                                self.listbox1.insert(END, index + '  [{}] --- '.format(format_type)  + title + ' [Type: {}]'.format(type_))

                                        else:
                                                self.listbox1.insert(END, index  + ' ({}) [{}] --- '.format(j, format_type)  + title + ' [Type: {}]'.format(type_))
                self.count_zploits()



        def delete_item(self):
            """
            delete a selected line from the listbox
            """
            try:
                # get selected line index
                try:
                        index = self.listbox1.curselection()[0]#get(ANCHOR)[0]#curselection()[0]
                        self.curr_index = index
                except:
                        pass
                self.listbox1.delete(self.curr_index)
                self.contents.delete(1.0, END)
                seltext = self.listbox1.get(self.curr_index)#index)
                ind = str(int(seltext.split('(')[0].split('[')[0].replace("'","")))###
                db_index = self.index_index[ind]
                file_loc=self.lines[db_index].split(',')[1] 
                try:
                    loc1 = db_path + file_loc
                    cat_file = subprocess.Popen(['cat', loc1], stdout=subprocess.PIPE)
                except:
                    locate1=subprocess.Popen(['locate',file_loc], stdout=subprocess.PIPE)
                    loc1=locate1.communicate()[0].rstrip('\n')
                    cat_file = subprocess.Popen(['cat',loc1], stdout=subprocess.PIPE)
                cat=cat_file.communicate()
                self.currently_selected = loc1
                self.enter3.delete(0,END)
                cs = self.currently_selected.split('/')[-1]
                self.enter3.insert(END, 'gcc $in -o $out/{}'.format(cs.split('.')[0]))

                self.title_box.delete(0,END)
                self.title_box.insert(END, seltext + ' ---> ')
                self.title_box.insert(END, loc1 )
                #self.title_box.insert(END, '\n' + '-'*max(len(loc1),len(seltext)) + '\n\n' )
                #self.contents.insert(END, seltext + '\n')
                #self.contents.insert(END, loc1 )
                #self.contents.insert(END, '\n' + '-'*max(len(loc1),len(seltext)) + '\n\n' )
                self.contents.insert(END, cat[0] )
            except IndexError:
                pass
            self.count_zploits()

        def alternatives(self,name):
                global f4
                global f5
                global f6
                global f7
                alternatives = []
                m = f6.search(name)
                if m:
                        alts = m.group(0).split('Kernel ')[1].split('/')
                        for alt in alts:
                                alt_name = re.sub(f6, 'Kernel ' + alt, name)
                                n = f7.search(alt_name)
                                alternatives.append(alt_name)
                else:
                        alternatives.append(name)
                return alternatives

        def set_out(self):
                out_path = tkFileDialog.askdirectory()
                self.enter2.delete(0, END)
                self.enter2.insert(END,out_path)
                
        def count_zploits(self):
                count = str(self.listbox1.size()) + ' exploits'
                self.label_count['text'] = count
                return count
        
        def kernel_name(self):
                self.use_name_filter("Linux Kernel", 0)

        def use_name_filter(self,name, neg): #called by apply_name_filter
            self.filtered_old = self.listbox1.get(0,END)
            self.filtered_new = []
            for line in self.filtered_old:
                        if neg == 0:
                                if name.lower() in line.split('--- ')[1].strip('"').lower():
                                        self.filtered_new.append(line)
                        else:
                                if name.lower() not in line.split('--- ')[1].strip('"').lower():
                                        self.filtered_new.append(line)
            self.filtered_old = self.filtered_new
            self.listbox1.delete(0, END)
            for item in self.filtered_new:
                self.listbox1.insert(END, item)
            self.filtered_new = []
            self.count_zploits()
            return self.filtered_old

        def use_type_filter(self, type_, neg): #called by apply_type_filter
            self.filtered_old = self.listbox1.get(0,END)
            self.filtered_new = []
            for line in self.filtered_old:
                        if neg == 0:
                                if type_.lower() in line.split('[Type: ')[1].strip(']').lower():
                                        self.filtered_new.append(line)
                        else:
                                if type_.lower() not in line.split('[Type: ')[1].strip(']').lower():
                                        self.filtered_new.append(line)
            self.filtered_old = self.filtered_new
            self.listbox1.delete(0, END)
            for item in self.filtered_new:
                self.listbox1.insert(END, item)
            self.filtered_new = []
            self.count_zploits()
            return self.filtered_old

        def compare_version(self, target, test):
                for j in range(4-len(target.split('.'))):
                        target += '.0'
                for j in range(4-len(test.split('.'))):
                        test += '.0'
                C=''
                for i in range(4):
                        a_split = target.split('.')[i].strip()
                        if a_split != 'x':
                                a = int(a_split)

                        b_split = test.split('.')[i].strip()
                        if b_split != 'x':
                                b = int(b_split)

                        if a < b:    # target < test
                                c = 0
                        elif a == b: # target = test
                                c = 1
                        elif b == 'x':
                                c = 'x'
                        else:        # target > test
                                c = 2
                        C += str(c) 
                return C

        def use_exact_version_filter(self, version):
                global f1
                self.filtered_new = []
                self.filtered_old = self.listbox1.get(0,END)

                for l, line in enumerate(self.filtered_old):
                        discard = False
                        if "Linux Kernel" in line:
                                m = f1.search(line)
                                if m:
                                        test = m.group(0).split('Kernel')[1].strip(' ')
                                        compare = self.compare_version(version, test)
                                        for i in range(4):
                                                if compare[i] == '1' or compare[i] == 'x':
                                                        discard = False
                                                else:
                                                        discard = True
                                                        break
                                        if discard == False:
                                                self.filtered_new.append(line)
                self.count_zploits()
                return self.filtered_new

        def use_upper_version_filter(self, f_version):
                global f2
                self.filtered_new = []
                self.filtered_old = self.listbox1.get(0,END)
                target = f_version
                for l, line in enumerate(self.filtered_old):
                        m = f2.search(line)
                        if m:
                                test = m.group(0).split('Kernel < ')[1].split(' ')[0]
                                compare = self.compare_version(target, test)

                                #compare = 0 --> target < test
                                #compare = 1 --> target = test
                                #compare = 2 --> target > test
                                #compare = x --> accept test
                                if compare[0] == '0' or compare[0] == 'x':
                                        self.filtered_new.append(line)
                                        continue
                                elif compare[0] == '1':
                                        if compare[1] == '0' or compare[0] == 'x':
                                                self.filtered_new.append(line)
                                                continue
                                        elif compare[1] == '1':
                                                if compare[2] == '0' or compare[0] == 'x':
                                                        self.filtered_new.append(line)
                                                        continue
                                                elif compare[2] == '1':
                                                        if compare[3] < '2' or compare[0] == 'x':
                                                                self.filtered_new.append(line)
                self.count_zploits()
                return self.filtered_new

        def use_interval_version_filter(self, f_version):
                global f3
                self.filtered_new = []
                self.filtered_old = self.listbox1.get(0,END)
                target = f_version
                for l, line in enumerate(self.filtered_old):
                        m = f3.search(line)
                        if m:
                                lower = m.group(0).split('Kernel ')[1].split('<')[0]
                                upper = m.group(0).split('<')[1]
                                comp_lower = self.compare_version(target, lower)
                                comp_upper = self.compare_version(target, upper)

                                if comp_upper[0] == '0' or comp_upper[0] == 'x':
                                        test_lower = True
                                elif comp_upper[0] == '1':
                                        if comp_upper[1] == '0' or comp_upper[1] == 'x':
                                                test_lower = True
                                        elif comp_upper[1] == '1':
                                                if comp_upper[2] == '0' or comp_upper[2] == 'x':
                                                        test_lower =  True
                                                elif comp_upper[2] == '1':
                                                        if comp_upper[3] < '2' or comp_upper[3] == 'x':
                                                                test_lower = True
                                                        else:
                                                                test_lower = False
                                                else:
                                                        test_lower = False
                                        else:
                                                test_lower = False
                                else:
                                        test_lower = False

                                #if the upper limit was actually higher than the target, check now the lower limit
                                if test_lower == True:
                                        if comp_lower[0] == '2' or comp_lower[0] == 'x':
                                                self.filtered_new.append(line)
                                                continue
                                        elif comp_lower[0] == '1':
                                                if comp_lower[1] == '2' or comp_lower[1] == 'x':
                                                        self.filtered_new.append(line)
                                                        continue
                                                elif comp_lower[1] == '1':
                                                        if comp_lower[2] == '2' or comp_lower[2] == 'x':
                                                                self.filtered_new.append(line)
                                                                continue
                                                        elif comp_lower[2] == '1':
                                                                if comp_lower[3] > '0' or comp_lower[3] == 'x':
                                                                        self.filtered_new.append(line)
                self.count_zploits()
                return self.filtered_new			

        def get_list(self,event):
            """
            function to read the listbox selection
            and put the result in an entry widget
            """
            self.currently_selected
            index = self.listbox1.curselection()[0]
            # get the line's text
            seltext = self.listbox1.get(index)

            self.contents.delete(1.0, END)
            # now display the selected text
            ind = str(int(seltext.split('(')[0].split('[')[0].replace("'","")))
            db_index = self.index_index[ind]
            file_loc=self.lines[db_index].split(',')[1] 
            try:
                loc1 = db_path + file_loc
                cat_file = subprocess.Popen(['cat', loc1], stdout=subprocess.PIPE)
            except:
                locate1=subprocess.Popen(['locate',file_loc], stdout=subprocess.PIPE)
                loc1=locate1.communicate()[0].rstrip('\n')
                cat_file = subprocess.Popen(['cat',loc1], stdout=subprocess.PIPE)
            cat=cat_file.communicate()
            self.currently_selected = loc1
            self.enter3.delete(0,END)
            cs = self.currently_selected.split('/')[-1]
            self.enter3.insert(END, 'gcc $in -o $out/{}'.format(cs.split('.')[0]))

            self.title_box.delete(0,END)
            self.title_box.insert(END, seltext + ' ---> ')
            self.title_box.insert(END, loc1 )
            #self.contents.insert(END, seltext + '\n')
            #self.contents.insert(END, loc1 )
            #self.contents.insert(END, '\n' + '-'*max(len(loc1),len(seltext)) + '\n\n' )
            self.contents.insert(END, cat[0] )

        def clr_filters(self):
                self.enter1.delete(0, 'end')
                self.fill_with_all()

        def apply_index_filter(self, event):
                self.filtered_old = self.listbox1.get(0, END)
                self.filtered_new = []
                edb_index = self.index_filter.get()
                filter='I: ' + edb_index 
                for line in self.filtered_old:
                        if edb_index == line.split(' ')[0]:
                                self.listbox1.delete(0, END)
                                self.listbox1.insert(END, line)
                                self.enter1.insert(END, filter)
                                break
               

        def apply_format_filter(self, format):
                neg = self.var_fmt.get()
                if format == '$check':
                        format = self.format_filter.get()
                if format == 'Format':
                        filter = ''
                else:
                        filter = 'F: ' + format + ' (n)'*neg + ', '

                self.filtered_old = self.listbox1.get(0,END)
                self.filtered_new = []
                
                for line in self.filtered_old:
                        if neg == 0:
                                if format.lower() == line.split('[')[1].split(']')[0].lower():
                                        self.filtered_new.append(line)
                        else:
                                if format.lower() != line.split('[')[1].split(']')[0].lower():
                                        self.filtered_new.append(line)
                self.filtered_old = self.filtered_new
                self.listbox1.delete(0, END)
                for item in self.filtered_new:
                        self.listbox1.insert(END, item)
                self.filtered_new = []
                self.count_zploits()
                self.enter1.insert(END,filter)
                return self.filtered_old
                
        def apply_name_filter(self, event):
                neg_name = self.var_name.get()
                f_name = self.name_filter.get()
                if f_name == 'Name':
                        filter = ''
                else:
                        if f_name == 'lk':
                                f_name = 'Linux Kernel'
                        filter = 'N: ' + f_name + ' (n)'*neg_name + ', '
                self.enter1.insert(END, filter)
                if filter != '':
                        self.use_name_filter(f_name, neg_name)

        def apply_type_filter(self, event):
                neg_type = self.var_type.get()
                f_type = self.type_filter.get()
                if f_type == 'Type':
                        filter = ''
                else:
                        filter = 'T: ' + f_type + ' (n)'*neg_type + ', '
                self.enter1.insert(END, filter)
                if filter != '':
                        self.use_type_filter(f_type, neg_type)

        def apply_version_filter(self, event):
                f_version = self.version_filter.get()
                if f_version == 'Version':
                        filter = ''
                else:
                        filter = 'V: ' + f_version + ', '
                self.enter1.insert(END, filter)

                filtered_exact = self.use_exact_version_filter(f_version)
                filtered_upper = self.use_upper_version_filter(f_version)
                filtered_interval = self.use_interval_version_filter(f_version)
                

                filtered = sorted(list(set(filtered_exact + filtered_upper + filtered_interval)))
                self.listbox1.delete(0, END)
                for item in filtered:
                        self.listbox1.insert(END, item)
                self.count_zploits()

        def sort_list():
            """
            function to sort listbox items case insensitive
            """
            temp_list = list(listbox1.get(0, END))
            temp_list.sort(key=str.lower)
            # delete contents of present listbox
            listbox1.delete(0, END)
            # load listbox with sorted data
            for item in temp_list:
                listbox1.insert(END, item)

        def save_list(self):
            """
            save the current listbox contents to a file
            """
            self.filename_save = tkFileDialog.asksaveasfilename(initialdir = "/home/", title="Save exploits to file", filetypes = (("text files","*.txt"),("all files","*.*")))
            print 'ooi', self.filename_save
            # get a list of listbox lines
            temp_list = list(self.listbox1.get(0, END))
            # add a trailing newline char to each line
            temp_list = [item + '\n' for item in temp_list]
            # give the file a different name
            fout = open(self.filename_save, "a")
            fout.writelines(temp_list)
            fout.close()

        def save_tmp_copy(self):
            tmp_files = glob.glob('/tmp/*')
            name = self.currently_selected.split('/')[-1].split('.')
            while True:
                    name1 = name[0] + '_' + str(random.randint(1,999)).zfill(3) + '.' + name[1].lstrip('[').rstrip(']')[0]
                    if name1 not in tmp_files:
                            break
            file = self.currently_selected
            tx = self.contents.get("1.0",END)
            filename = '/tmp/' + name1
            f = open(filename, 'w')
            f.write(tx)
            f.close()
            return filename
            
        def copy_file(self):
            filename = self.currently_selected.split('/')[-1]
            if self.enter2.get().endswith('/'):
                    out_file = self.enter2.get() + filename
            else:
                    out_file = self.enter2.get() + '/' + filename
            if self.var_tmp.get()==0:
                    copy_cmd=subprocess.Popen(['cp', self.currently_selected, out_file], stdout=subprocess.PIPE)
                    out_copy=copy_cmd.communicate()[0].rstrip('\n')
                    print 'Output of copy command: ',out_copy
            else:
                    tx = self.contents.get("1.0",END)
                    print tx
                    f = open(out_file, 'w')
                    f.write(tx)
                    f.close()

        def compile_file(self):
            filename = self.currently_selected.split('/')[-1]
            if self.enter2.get().endswith('/'):
                out_file = self.enter2.get()
            else:
                out_file = self.enter2.get() + '/'
            gcc_cmd = self.enter3.get()

            if self.var_tmp.get()==0:
                    if '$in' in gcc_cmd:
                            gcc_cmd = gcc_cmd.replace('$in', self.currently_selected)
            else:
                    filename = self.save_tmp_copy()
                    if '$in' in gcc_cmd:
                            gcc_cmd = gcc_cmd.replace('$in', filename) 
            if '$out' in gcc_cmd:
                    gcc_cmd = gcc_cmd.replace('$out/', out_file)

            compile_cmd=subprocess.Popen(gcc_cmd.split(' '), stdout=subprocess.PIPE)
            out_compile=compile_cmd.communicate()[0].rstrip('\n')
            print 'Output of compile command: ', out_compile


app = Application(master = root)
app.mainloop()


