import paramiko

class SSHClient:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Not recommended for production
            self.client.connect(self.hostname, username=self.username, password=self.password)
            print(f"Connected to {self.hostname}")
        except Exception as e:
            print(f"Error connecting to {self.hostname}: {e}")
            self.client = None

    def execute_command(self, command):
        if not self.client:
            print("Not connected to SSH server.")
            return None

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return output, error
        except Exception as e:
            print(f"Error executing command: {e}")
            return None, str(e)

    def close(self):
        if self.client:
            self.client.close()
            print(f"Connection to {self.hostname} closed.")
            self.client = None