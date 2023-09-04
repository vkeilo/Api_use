import subprocess
import tkinter as tk
from pynput import keyboard
from agent_use import gpt_agent

class Assistant:
    def __init__(self):
        self.agent = gpt_agent('chatglm2-6b')
        self.agent.init_messages_by_json('assistant.json')
        self.tasks = {'translate': "翻译以下内容:\n", 'explain': "介绍或者解释以下内容：\n"}
        self.know_reply = None
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+1': self.run_translate,
            '<ctrl>+<alt>+2': self.run_explain
        })
        self.init_gui()

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Assistant Tool")
        self.textbox = tk.Text(self.root)
        # custom_font = tk. (family="Helvetica", size=14)
        # self.textbox = tk.Text(self.root, font=custom_font)
        self.textbox.configure(font=("Helvetica", 16, "normal"))
        self.textbox.pack()
        self.root.wm_attributes("-topmost", 1)

    def run_translate(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.textbox.insert(tk.END, "选中的文本: " + selected_text + "\n")
            self.root.update_idletasks()
            self.agent.prompt_add(self.tasks['translate'] + selected_text)
            reply = self.agent.prompt_post(T=0)
            self.know_reply = reply
            self.show_reply()

    def run_explain(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.textbox.insert(tk.END, "选中的文本: " + selected_text + "\n")
            self.root.update_idletasks()
            self.agent.prompt_add(self.tasks['explain'] + selected_text)
            reply = self.agent.prompt_post(T=0)
            self.know_reply = reply
            self.show_reply()

    def show_reply(self):
        self.textbox.insert(tk.END, "回复: " + self.know_reply + "\n")
        self.root.update_idletasks()

    def start_work(self):
        self.listener.start()
        self.root.mainloop()

    def get_selected_text(self):
        try:
            # 使用xsel命令获取鼠标当前选中的文本
            selected_text = subprocess.check_output(['xsel', '-o'], universal_newlines=True).strip()
            return selected_text
        except subprocess.CalledProcessError:
            return None

if __name__ == "__main__":
    app = Assistant()
    app.start_work()
