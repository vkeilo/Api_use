import subprocess
import threading



############################
# • PlatformSpecific: 1
# • Created: 2
# • Updated: 4
# • Removed: 8
# • Renamed: 16
# • OwnerModified: 32
# • AttributeModified: 64
# • MovedFrom: 128
# • MovedTo: 256
# • IsFile: 512
# • IsDir: 1024
# • IsSymLink: 2048
# • Link: 4096
##########################

class dir_scanner():
    def __init__(self,dir_path) -> None:
        self.scanpath = dir_path
        self.logger = []
        self.process = None
        self.log_id = 0
        self.needcheck_list = []
        self.lock = threading.Lock()

    def run_log(self):
        fswatch_command = f'fswatch -n {self.scanpath}'
        self.process = subprocess.Popen(fswatch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            for line in self.process.stdout:
                # 检查fswatch输出中的每一行
                line = line.strip()
                split_line = line.split(' ')
                append_datas = {'id':self.log_id, 'path':split_line[0], 'event':int(split_line[1]) }
                self.log_id += 1
                with self.lock:
                    self.logger.append(append_datas)
                    self.start_check([4,1,4,4],self.logger.copy())
                    self.start_check([2],self.logger.copy())
        except KeyboardInterrupt:
            # 当用户按下Ctrl+C时，停止fswatch进程
            self.process.terminate()
        finally:
            self.process.stdout.close()
            self.process.stderr.close()
    
    def event_list_check(self,event_list,logger_list):
        # 如果记录长度不够或最后一位事件都没有对上就直接pass
        if len(logger_list) < len(event_list):
            return 
        if logger_list[-1]['event'] != event_list[-1]:
            return
        now_file = logger_list[-1]['path']
        for i in range(len(event_list)):
            if event_list[-i-1] != logger_list[-i-1]['event'] or now_file != logger_list[-i-1]['path']:
                return
        # print(f'find it {now_file}')
        self.needcheck_list.append(now_file) 

    def start_log(self):
        print('目录监测启动')
        log_thread = threading.Thread(target=self.run_log)
        log_thread.start()

    def start_check(self,event_list,logger_list):
        check_thread = threading.Thread(target=self.event_list_check,args=(event_list,logger_list))
        check_thread.start()

    def need_check_remove(self,path):
        with self.lock:
            self.needcheck_list = [item for item in self.needcheck_list if item != path]

# test_scanner = dir_scanner('.')
# test_scanner.start_log()
# print('started')
