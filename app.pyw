from configparser import ConfigParser
import subprocess
from tkinter import *
from tkinter import messagebox, filedialog, Text
import time
import psutil

root = Tk()
root.geometry("500x340")
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


def dot_trick(handle):
    if handle == "":
        return
    f = lambda s: s[11:] and [s[0] + w + x for x in f(s[1:]) for w in ('.', '')] or [s]
    mail_list = f(handle)
    file = open("scripts/emails.txt", "w")
    file.write("\n".join(map(lambda x: str(x), mail_list)))
    return


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
        input_mail = i_mail.get("1.0", "end-1c")
        input_token = i_token.get("1.0", "end-1c")

        if input_token == "" and input_mail == "":
            pass
        elif input_token != "" and input_mail != "":
            configur["email"] = input_mail
            configur["token"] = input_token
            dot_trick(input_mail)
        else:
            out.set("Output and Progress: Please set both email and token or leave them empty")
            return

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
        process_list.append(subprocess.Popen(["python",
                                              "scripts/main.py"]))  # , stdout=subprocess.PIPE, shell=True, bufsize=0, universal_newlines=True))
        out.set("Output and Progress: Starting Downloads, Opening Download window with progress")
    else:
        on_close()


out = StringVar()
out.set("Output and Progress: ")
l_info = Label(text="Leave Email and Token empty if you already set them in another run")
l_res = Label(text="Choose Resolution")
l_out = Label(root, textvariable=out)
inputtxt = Text(root, height=3,
                width=61)
i_mail = Text(root, height=1,
              width=30)
i_token = Text(root, height=1,
               width=30)
l_mode = Label(root, text="Input Mode")
l_mail = Label(root, text="Input Mail")
l_token = Label(root, text="Input Token")
cp = ConfigParser()
cp.read(filenames="scripts/config.ini")
configurations = cp["CONFIGURATIONS"]
path = StringVar()
path.set(configurations["folder_path"])
l_path = Label(root, textvariable=path)
l_mode_2 = Label(root, text="If you selected [Insert Manually], insert Film Name:")
end = Button(root, height=1,
             width=33,
             text="Terminate Downloads",
             command=lambda: take_config(False))
start = Button(root, height=1,
               width=33,
               text="Start Downloads",
               command=lambda: take_config(True))
folder = Button(root, height=1,
                width=69,
                text="Chose Download Folder",
                command=lambda: folder_diag())

l_res.grid(row=0, column=0, sticky=W, pady=2, padx=2)
drop_res.grid(row=0, column=1, sticky=E, pady=2, padx=2)
l_mode.grid(row=1, column=0, sticky=W, pady=2, padx=2)
drop_mode.grid(row=1, column=1, sticky=E, pady=2, padx=2)
l_info.grid(row=5, columnspan=2, sticky=W, pady=2, padx=2)
l_mail.grid(row=6, column=0, sticky=W, pady=2, padx=2)
i_mail.grid(row=7, column=0, sticky=E, pady=2, padx=2)
l_token.grid(row=6, column=1, sticky=W, pady=2, padx=2)
i_token.grid(row=7, column=1, sticky=E, pady=2, padx=2)
l_mode_2.grid(row=3, columnspan=2, sticky=W, pady=2, padx=2)
inputtxt.grid(row=4, columnspan=2, sticky=W, pady=2, padx=2)
folder.grid(row=8, columnspan=2, pady=2, padx=2)
l_path.grid(row=9, columnspan=2, sticky=W, pady=2, padx=2)
start.grid(row=10, column=0, pady=2, padx=2)
end.grid(row=10, column=1, pady=2, padx=2)
l_out.grid(row=11, columnspan=2, sticky=W, pady=2, padx=2)

mainloop()
