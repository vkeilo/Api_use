import threading
import openai
import json

class gpt_agent():
    
    def __init__(self,model_name,key="none"):
        self.api_dic = {'chatglm2-6b':"http://localhost:8000/v1"}
        self.model = model_name
        self.messages = []
        self.origin_memery = []
        openai.api_key = key
        openai.api_base = self.api_dic[self.model]
    
    # 角色回滚
    def init_role(self):
        self.messages = self.origin_memery.copy()
        # print(self.messages)

    # 根据目标json对话中的内容进行角色扮演
    def init_messages_by_json(self,json_path):
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        self.messages = data["dialogues"]
        self.origin_memery = self.messages.copy()
        
    # 等待用户输入并与 GPT 进行交互
    def interact_with_agent(self):
        while True:
            user_input = input("You: \n")  # 等待用户输入
            if user_input.lower() == "exit":
                break  # 如果用户输入 "exit"，则退出交互
            self.prompt_add(user_input)  # 将用户输入添加到对话历史
            response = self.prompt_post()  # 获取 GPT 的回复
            print("assistant:", response)  # 打印 GPT 的回复

    def start_interact(self):
        check_thread = threading.Thread(target=self.interact_with_agent)
        check_thread.start()
            
    # 在对话历史中额外增加一句
    def history_add_one(self,role,text):
        self.messages.append({"role":role, "content": text})
         

    # 根据一段文本描述进行角色扮演
    def init_messages_by_roleplay(self,task):
        self.messages=None
        self.history_add_one("user",task)
        self.origin_memery = self.messages.copy()

    # 用户发问/出题    
    def prompt_add(self,text):
        self.history_add_one("user",text)

    # 获取回答，并更新对话历史    
    def prompt_post(self,T = 0.01,maxtokens = 200,remember_flag = True):
        # 调用API进行对话生成
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            max_tokens=maxtokens,
            temperature=T
        )
        # 提取生成的回复文本
        reply = response.choices[0].message.content
        self.history_add_one("assistant", reply)
        if not remember_flag:
            self.messages=self.messages[:-2]
        return reply