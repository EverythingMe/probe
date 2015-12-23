from subprocess import Popen, PIPE

__author__ = 'danielby'


def execute_command(cmd):

    results = dict()
    cmd_res = Popen(cmd, stdout=PIPE, shell=True)

    cmd_res.wait()
    results['stdout'] = cmd_res.stdout.readlines()
    results['pid'] = cmd_res.pid

    return results