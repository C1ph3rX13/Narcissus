# -*- coding: utf-8 -*-
import yaml
import paramiko
from log import logger


class SSH:
    def __init__(self):
        self.config_file = 'config.yaml'
        self.ssh_client = None

        try:
            with open(self.config_file, 'r', encoding='UTF-8') as f:
                data = yaml.safe_load(f)

            self.hostname = data.get('hostname')
            self.port = data.get('port')
            self.username = data.get('username')
            self.password = data.get('password')
            self.private_key = data.get('private_key')

        except FileNotFoundError:
            self._create_example_yaml()
            logger.error(f"Config file '{self.config_file}' not found. An example file has been created.")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in config file '{self.config_file}': {e}")
            raise
        except SystemExit as e:
            logger.error(f"Error parsing config file '{self.config_file}': {e}")

    def _create_example_yaml(self):
        # 创建示例 YAML 配置文件
        example_config = {
            'hostname': 'example.com',
            'port': '22',
            'username': 'root',
            'password': '1234',
            'private_key': '/path/to/private/key.pem'
        }

        with open(self.config_file, 'w', encoding='UTF-8') as f:
            yaml.dump(example_config, f, default_flow_style=False)

    def connect(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.private_key:
                # 使用私钥登录
                private_key = paramiko.RSAKey.from_private_key_file(self.private_key)
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    pkey=private_key
                )
            else:
                # 使用密码登录
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                )

        except paramiko.AuthenticationException:
            logger.error('Authentication failed, please verify your credentials.')
            raise
        except paramiko.SSHException as e:
            logger.error(f'SSH connection failed: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Others: {str(e)}')
            raise

    def exec_bash(self, command):
        if not self.ssh_client:
            raise ValueError("SSH connection is not established.")

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)

            # 处理标准输出
            output = stdout.read().decode('utf-8')
            if output:
                logger.info(command + '\n' + output)

            # 处理标准错误
            error = stderr.read().decode('utf-8')
            if error:
                logger.info(error + '\n' + output)

            return output
        except Exception as e:
            logger.error(f'Error executing command: {str(e)}')

    def close(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
