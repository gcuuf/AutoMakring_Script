import time
import netmiko
import re
from config import CML_CONTROLLER, CML_USERNAME, CML_PASSWORD, ENABLE_SECRET, LAB_NAME


# 用于缓存已连接的会话，避免重复登录
_connection_pool = {}

class NetworkConnector:
    def __init__(self, host):
        self.host = host
        self.conn = None

    def connect(self):
        if self.host in _connection_pool:
            self.conn = _connection_pool[self.host]
            return self

        self.conn = netmiko.ConnectHandler(
            device_type='terminal_server',
            host=CML_CONTROLLER,
            username=CML_USERNAME,
            password=CML_PASSWORD,
            secret=ENABLE_SECRET,
            timeout=30,
            fast_cli=False,
        )

        time.sleep(0.3)
        output = self.conn.read_channel()

        if "consoles>" not in output:
            self.conn.write_channel("\r")
            time.sleep(0.2)
            output = self.conn.read_channel()
            if "consoles>" not in output:
                raise Exception("CML console prompt 'consoles>' not detected.")

        open_cmd = f"open /{LAB_NAME}/{self.host}/0"
        self.conn.write_channel(open_cmd + "\r")
        time.sleep(1)

        output = self.conn.read_channel()
        if not re.search(r"[>#]\s*$", output, re.M):
            self.conn.write_channel("\r\r")
            time.sleep(0.3)
            output = self.conn.read_channel()
            if not re.search(r"[>#]\s*$", output, re.M):
                raise Exception("Failed to enter device console.")

        netmiko.redispatch(self.conn, device_type='cisco_ios')
        time.sleep(0.2)

        try:
            self.conn.enable()
        except Exception:
            pass

        try:
            self.conn.send_command_timing("terminal length 0", read_timeout=2)
            self.conn.send_command_timing("terminal width 511", read_timeout=2)
        except Exception:
            pass

        _connection_pool[self.host] = self.conn
        return self

    def execute_commands(self, commands):
        if not self.conn:
            raise Exception("Not connected. Call connect() first.")

        cmds = commands if isinstance(commands, list) else [commands]
        full_output = ""

        for cmd in cmds:
            cmd = cmd.strip()
            if not cmd:
                continue
            try:
                output = self.conn.send_command(cmd, expect_string=r"#", read_timeout=10)
                full_output += f"{self.host}#{cmd}\n{output}\n"
            except Exception as e:
                full_output += f"[ERROR executing '{cmd}']: {e}\n"

        return full_output

    def close(self):
        if self.conn:
            try:
                self.conn.write_channel("\r")
                self.conn.disconnect()
            except Exception:
                pass
        if self.host in _connection_pool:
            del _connection_pool[self.host]


def connect(host, command):
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            connector = NetworkConnector(host).connect()
            output = connector.execute_commands(command)
            return True, output
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(1)
    return False, f"Connection failed to {host}"


def close_all_connections():
    for host, conn in list(_connection_pool.items()):
        try:
            conn.write_channel("\r")
            conn.disconnect()
        except Exception:
            pass
        del _connection_pool[host]
