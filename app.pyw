from configparser import ConfigParser
import subprocess
from tkinter import *
from tkinter import messagebox, filedialog, Text
import time
import psutil
import scripts.main as prc

root = Tk()
root.geometry("400x600")
root.title(" Film Downloader")
res = StringVar()
res.set("4K")
mode = StringVar()
mode.set("Read list from File")
process_list = []
lista_res = ["4K", "2K", "1080p", "720p"]
lista_mode = ["Read list from File", "Search For The Film", "Insert Manually"]
drop_res = OptionMenu(root, res, *lista_res)
drop_mode = OptionMenu(root, mode, *lista_mode)


def folder_diag():
    folder_path = str(filedialog.askdirectory())
    path.set(f"{folder_path}")
    conf = ConfigParser()
    conf.read(filenames="scripts/config.ini")
    configur = conf["CONFIGURATIONS"]
    configur["folder_path"] = folder_path
    with open('scripts/config.ini', 'w') as confi:
        conf.write(confi)


def on_close():
    # custom close options, here's one example:

    close = messagebox.askokcancel("Close", "Would you like to close the program and Stop Downloads?")
    if close:
        for p in process_list:
            try:
                kill(p.pid)
            except psutil.NoSuchProcess:
                pass
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def take_config(var):
    if var:
        selected_res = res.get()
        selected_mode = mode.get()

        conf = ConfigParser()
        conf.read(filenames="scripts/config.ini")
        configur = conf["CONFIGURATIONS"]
        configur["resolution"] = selected_res
        configur["headless"] = "True"
        # Write changes back to file

        if selected_mode == lista_mode[2]:
            with open("film_list.txt", 'w') as file:
                file.write(inputtxt.get("1.0", "end-1c"))
        elif selected_mode == lista_mode[1]:
            configur["headless"] = "False"
        else:
            configur["headless"] = "True"

        with open('scripts/config.ini', 'w') as confi:
            conf.write(confi)
        time.sleep(1)
        process_list.append(subprocess.Popen(["python", "scripts/main.py"]))#, stdout=subprocess.PIPE, shell=True, bufsize=0, universal_newlines=True))
        '''for line in process_list[-1].stdout:
            root.update()
            progress.insert(END, f"{str(line)}")
            root.update()
        process_list[-1].stdout.close()'''
    else:
        on_close()


l_res = Label(text="Choose Resolution")
inputtxt = Text(root, height=3,
                width=49)

l_mode = Label(root, text="Input Mode")
cp = ConfigParser()
cp.read(filenames="scripts/config.ini")
configurations = cp["CONFIGURATIONS"]
path = StringVar()
path.set(configurations["folder_path"])
l_path = Label(root, textvariable=path)
l_mode_2 = Label(root, text="If you selected [Insert Manually], insert Film Name:")
end = Button(root, height=1,
             width=26,
             text="Terminate Downloads",
             command=lambda: take_config(False))
start = Button(root, height=1,
               width=26,
               text="Start Downloads",
               command=lambda: take_config(True))
folder = Button(root, height=1,
                width=55,
                text="Chose Download Folder",
                command=lambda: folder_diag())

progress = Text(root, height=10,
                width=49,
                )

l_res.grid(row=0, column=0, sticky=W, pady=2, padx=2)
drop_res.grid(row=0, column=1, sticky=E, pady=2, padx=2)
l_mode.grid(row=1, column=0, sticky=W, pady=2, padx=2)
drop_mode.grid(row=1, column=1, sticky=E, pady=2, padx=2)
l_mode_2.grid(row=2, columnspan=2, sticky=W, pady=2, padx=2)
inputtxt.grid(row=3, columnspan=2, sticky=W, pady=2, padx=2)
folder.grid(row=4, columnspan=2, pady=2, padx=2)
l_path.grid(row=5, columnspan=2, sticky=W, pady=2, padx=2)
start.grid(row=6, column=0, pady=2, padx=2)
end.grid(row=6, column=1, pady=2, padx=2)
progress.grid(row=7, columnspan=2, sticky=W, pady=2, padx=2)

mainloop()
