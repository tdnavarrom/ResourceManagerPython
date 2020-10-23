import tkinter as tk
from tkinter import ttk
from tkinter import *
import process as ps
import time

class Task_Manager():

    def __init__(self, root):
        self.root = root

        ### RAM

        self.wrapperRam = tk.LabelFrame(self.root)
        self.wrapperRam.pack(fill='both', expand='yes', padx=20, pady=10)
        
        self.labelRam = tk.Label(self.wrapperRam, text='RAM: ', fg='black', font='Times 16')
        self.labelRam.pack(side='top')

        self.varRam= StringVar()
        self.varRam.set('Total Memory: ')
        self.labelRamTotal = tk.Label(self.wrapperRam, textvariable=self.varRam, fg='black', font='Times 12')
        self.labelRamTotal.pack(side='right')

        self.varRamAvail = StringVar()
        self.varRamAvail.set('Available Memory: ')
        self.labelRam = tk.Label(self.wrapperRam, textvariable=self.varRamAvail, fg='black', font='Times 12')
        self.labelRam.pack(side='left')

        self.varRamUsed= StringVar()
        self.varRamUsed.set('Memory Used: ')
        self.labelRamTotal = tk.Label(self.wrapperRam, textvariable=self.varRamUsed, fg='black', font='Times 12')
        self.labelRamTotal.pack(side='right')

        self.varRamPercent = StringVar()
        self.varRamPercent.set('Usage Percentage: ')
        self.labelRam = tk.Label(self.wrapperRam, textvariable=self.varRamPercent, fg='black', font='Times 12')
        self.labelRam.pack(side='left')


        ### DISK

        self.wrapperDisk = tk.LabelFrame(self.root)
        self.wrapperDisk.pack(fill='both', expand='yes', padx=20, pady=10)
        self.labelDisk = tk.Label(self.wrapperDisk, text='Disk Usage: ', fg='black', font='Times 16')
        self.labelDisk.pack(side='top')

        self.varDisk = StringVar()
        self.varDisk.set('Total: ')
        self.labelDisk = tk.Label(self.wrapperDisk, textvariable=self.varDisk, fg='black', font='Times 12')
        self.labelDisk.pack(side='right')

        self.varDiskUsed = StringVar()
        self.varDiskUsed.set('Used: ')
        self.labelDisk = tk.Label(self.wrapperDisk, textvariable=self.varDiskUsed, fg='black', font='Times 12')
        self.labelDisk.pack(side='right')

        self.varDiskAvail = StringVar()
        self.varDiskAvail.set('Available: ')
        self.labelDisk = tk.Label(self.wrapperDisk, textvariable=self.varDiskAvail, fg='black', font='Times 12')
        self.labelDisk.pack(side='left')

        self.varDiskPercent = StringVar()
        self.varDiskPercent.set('Usage Percentage: ')
        self.labelDisk = tk.Label(self.wrapperDisk, textvariable=self.varDiskPercent, fg='black', font='Times 12')
        self.labelDisk.pack(side='left')


        ### PROCESSES
        
        self.wrapper1 = tk.LabelFrame(self.root)
        self.wrapper1.pack(fill='both', expand='yes', padx=20, pady=10)
        self.label = tk.Label(self.wrapper1, text='List of processes', fg='black', font='Times 20')
        self.label.pack()
        self.table = ttk.Treeview(self.wrapper1, columns=(1,2,3,4), show='headings', height='50')
        self.table.heading(1, text = "PID")
        self.table.heading(2, text = "NAME")
        self.table.heading(3, text = "% MEMORY")
        self.table.heading(4, text = "% PROCESSOR")
        self.table.pack(side='left')
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Kill")
        self.table.bind("<Button-3>", self.kill_process)
        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient='vertical', command=self.table.yview)
        self.yscrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.yscrollbar.set)
        self.list_processes()

    def get_ram_usage(self):
        m_usage = ps.get_memory()

        total_mem = m_usage[0] / 1024 / 1024 / 1024
        available = m_usage[1] / 1024 / 1024 / 1024
        percent = m_usage[2]
        used = m_usage[3] / 1024 / 1024 / 1024

        self.varRam.set('Total Memory: ' + str(round(total_mem,3)) + 'GB')
        self.varRamAvail.set('Available Memory: ' + str(round(available,3)) + 'GB')
        self.varRamUsed.set('Memory Used: ' + str(round(used,3)) + 'GB')
        self.varRamPercent.set('Usage Percentage: ' + str(percent) + '%')


    def get_disk_usage(self):
        disk = ps.get_disk_usage(ps.get_disk_paritions()[0].mountpoint)
        
        total_mem = disk[0] / 1024 / 1024 / 1024
        used = disk[1] / 1024 / 1024 / 1024
        available = disk[2] / 1024 / 1024 / 1024
        percent = disk[3]

        self.varDisk.set('Total: ' + str(round(total_mem,3)) + 'GB')
        self.varDiskUsed.set('Used: ' + str(round(used,3)) + 'GB')
        self.varDiskAvail.set('Available: ' + str(round(available,3)) + 'GB')
        self.varDiskPercent.set('Usage Percentage: ' + str(percent) + '%')

    def list_processes(self):
        r_processes = ps.get_current_processes()
        for x in r_processes:
            self.table.insert('', 'end', values=(x, r_processes[x]['name'],round(r_processes[x]['memory_percent'],1),r_processes[x]['cpu_percent']))
        self.root.after(1000, self.refresh)

    def kill_process(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
            curItem = self.table.focus()
            pid = self.table.item(curItem)['values'][0]
            ps.kill_process(pid)
            self.table.delete(curItem)
        finally:
            self.menu.grab_release()

    def refresh(self):
        self.get_ram_usage()
        self.get_disk_usage()

        for row in self.table.get_children():
            self.table.delete(row)
        self.list_processes()

if __name__== "__main__":
    root = tk.Tk()
    root.title('Task Manager')
    root.geometry('900x700')
    root.resizable(False, False)
    app = Task_Manager(root)
    root.mainloop()