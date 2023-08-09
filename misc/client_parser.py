import argparse
from qmp_formatter import to_qmp

def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='guest-agent help', dest='command')

    guest_sync_parser = subparsers.add_parser('guest-sync')
    guest_sync_parser.add_argument("--id", type=int)

    get_osinfo_parser = subparsers.add_parser('get-osinfo')

    create_user_parser = subparsers.add_parser('create-user')
    create_user_parser.add_argument("--username", type=str)
    create_user_parser.add_argument("--groups")
    create_user_parser.add_argument("--create-home", action='store_true')

    deploy_ssh_parser = subparsers.add_parser('deploy-ssh-pubkey')
    deploy_ssh_parser.add_argument("--username", type=str)
    deploy_ssh_parser.add_argument("--ssh-key", type=str)


    parsed = parser.parse_args()
    return to_qmp(parsed)
