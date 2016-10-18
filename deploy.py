import os
import tarfile
import subprocess
import paramiko
from const import (
    USER,
    IP,
    PROJECT_FOLDER,
    DEPLOY_PACK,
    REMOTE_PATH,
    PROJECT_DIR
)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def upload_deploy():
    result = subprocess.call(['scp', DEPLOY_PACK, '{}@{}:{}'.format(USER, IP, REMOTE_PATH)])
    if result < 0:
        raise Exception("Upload failed")


def create_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(IP, username=USER)
    return ssh_client


def remote_deploy(ssh_client, cmd):
    _, stdout, stderr = ssh_client.exec_command(cmd)
    err = stderr.readlines()
    print(''.join(stdout.readlines()))


def run(ssh_client):
    _, so, se =ssh_client.exec_command('cd /data/kid ; uwsgi --ini vegetable.ini')
    print(so.readlines())
    print(se.readlines())

def main():
    cmd = [
        "cd {}".format(REMOTE_PATH),
        'rm -r -f {}'.format(os.path.join(REMOTE_PATH, PROJECT_FOLDER)),
        'tar -xvf {}'.format(DEPLOY_PACK),
        "ps aux | grep uwsgi | grep vegetable | awk '{print $2}' | xargs kill",
    ]
    cmd = ' ; '.join(cmd)

    print(cmd)

    make_tarfile(DEPLOY_PACK, PROJECT_DIR)
    upload_deploy()

    ssh_client = create_ssh_client()
    remote_deploy(ssh_client, cmd)
    run(ssh_client)

if __name__ == "__main__":
	main()
	
