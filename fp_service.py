import winrm

# 配置 WS-Management 连接信息
# 注意：这里假设你的目标服务器支持 Kerberos 认证，并且你的机器已经加入了相应的域
url = "http://192.168.1.114:5985/wsman"
server_22 = '192.168.1.22'
server_114 = '192.168.1.114'
username = r'admin'
password = 'Kd62522989.'

cn_username = r'TPTWKD\administrator'
cn_password = 'fmp6ej;284x.6'

# program_name = 'javaw'
# # 定义要检查的进程名称
#
# powershell_command = f"""
# $processes = Get-Process -Name {program_name} -ErrorAction SilentlyContinue
# if ($processes -ne $null) {{
#     echo "0"
# }} else {{
#     echo "1"
# }}
# """

command_process = '''
# 定义要检查的进程名称  
$processName = "javaw"  

# 使用Get-Process检查进程是否存在  
$process = Get-Process -Name $processName -ErrorAction SilentlyContinue  

# 检查变量$process是否为空  
if ($process -ne $null)  
{  
    #Write-Host "process '$processName' is running."  
    Write-Host '0'
    # 如果你想获取更多关于该进程的信息，可以打印$process变量  
    # $process | Format-List  
}  
else  
{  
    #Write-Host "process '$processName' is not running."  
    Write-Host "1"
}
'''

command_service = '''
$serviceName = "FileZilla Server" # 将YourServiceName替换为你想要检查的服务名  
$service = Get-Service -Name $serviceName  
  
if ($service.Status -eq "Running") {  
    Write-Host "0"  
} else {  
    Write-Host "1"  
}
'''


def process_is_running(ip,program_name,type = 'Process'):
    powershell_command = f"""  
    $process = "Process"
    $service = "Service"
    $processes = Get-{type} -Name {program_name} -ErrorAction SilentlyContinue  
    if ($processes -ne $null) {{  
            echo "0"  
        }} else {{  
            echo "1"  
        }}
      
    """

    try:
        s = winrm.Session(ip, auth=(username, password))
        #s.run_ps(cmd_process1)
        result = s.run_ps(powershell_command).std_out.decode('utf-8').strip()
        #response = s.run_ps(powershell_command)
        # 检查命令执行结果
        print(f'{program_name}返回结果为：',result)
        return int(result)
    except Exception as e:
        print('执行异常',e)
        return 2

#fp_is_running()

def service_is_running(ip,program_name):
    cmd_service = f'''
    $service = Get-Service -Name '{program_name}' -ErrorAction SilentlyContinue

    if ($service.Status -eq "Running") {{
        Write-Host "0"  
    }} else {{  
        Write-Host "1"  
    }}
    '''

    try:
        s = winrm.Session(ip, auth=(username, password))
        result = s.run_ps(cmd_service).std_out
        is_running = str(result)[2]
        print(f'{program_name}返回结果为：',is_running)
        return int(result)
    except Exception as e:
        print(e)
        return 2

# service_is_running('192.168.1.114',"W32Time")


#process_is_running('192.168.1.223','kd_ems')

def process_or_service(ip,program_name,type='Process'):
    if type == 'Process':
        process_is_running(ip,program_name)
    elif type == 'Service':
        service_is_running(ip,program_name)
    else:
        print('无效类型，请输入Process or Service')
        return 3

# process_or_service('192.168.1.114','W32Time','Service')

def ProcessAndService_isrunning(ip, program_name, type='Process'):
    powershell_command = f"""  
    if ({type} -eq 'Service') {{  
        # 检查服务  
        $service = Get-Service -Name {program_name} -ErrorAction SilentlyContinue
        if ($service) {{
            if ($service.Status -eq 'Running') {{
                Write-Host "1"
            }} else {{
                Write-Host "2"
            }}
        }} else {{
            Write-Host "3"
        }}
    }} elseif ({type} -eq 'Process') {{
        # 检查进程
        $processes = Get-Process | Where-Object {{ $_.ProcessName -eq {program_name} }}
        if ($processes) {{
            foreach ($process in $processes) {{
                Write-Host "4"
            }}
        }} else {{
            Write-Host "5"
        }}
    }} else {{
        Write-Host "6"
    }}
    """

    try:
        s = winrm.Session(ip, auth=(username, password))
        # s.run_ps(cmd_process1)
        result = s.run_ps(powershell_command)
        # response = s.run_ps(powershell_command)
        # 检查命令执行结果
        print(f'{program_name}返回结果为：', result)
        return int(result)
    except Exception as e:
        print('执行异常', e)
        return 2

# ProcessAndService_isrunning('192.168.1.22','javaw')