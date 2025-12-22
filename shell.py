import subprocess

# 启动一个Powershell会话
process = subprocess.Popen(['powershell.exe', '-NoExit'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 发送命令并获取输出
def send_command(command):
    process.stdin.write(command + '\n')
    process.stdin.flush()
    output = process.stdout.readline()
    return output

# 示例
output = send_command('Get-Process')
print(output)

# 显式关闭进程
process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()  # 等待进程结束