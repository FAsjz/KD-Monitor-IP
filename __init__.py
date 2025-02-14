import ping3
from ping3 import ping, verbose_ping

def domain_ping_test(domain):
    try:
        response_time = ping(domain,timeout=5)
        if response_time is not None:
            # print("Ping测试结果：{} 的平均响应时间为 {:.2f}ms".format(domain, response_time))
            print(f"Ping测试结果：{response_time}")
            if response_time == 0.0:
                print(111)

        else:
            print("Ping测试结果：{} 无法到达或超时".format(domain))
    except Exception as e:
        print("Ping测试出现错误，请检查域名输入是否正确以及网络连接是否正常",e)


def ping_ip(ip, timeout=1, count=5):
    for _ in range(count):
        try:
            response = ping3.ping(ip, timeout)
            print(response)
            if response is None:
                continue  # No response received, try again
            elif response >= 0 and response is not False:
                # return True  # IP is reachable
                print('true')  # IP is reachable
        except Exception as e:
            print(f"Warning: Exception occurred while pinging {ip}: {e}")
            continue  # Ignore this ping and try again
    # return False  # IP is not reachable after multiple attempts
    print('False')   # IP is not reachable after multiple attempts

# 域名Ping测试
# domain_ping_test("192.168.1.217")
ping_ip("192.168.19.83")
# domain_ping_test("192.168.1.239")
# domain_ping_test("192.168.15.200")

# verbose_ping("192.168.31.254")
