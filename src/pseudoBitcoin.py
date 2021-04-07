#!/usr/bin/env python3
import sys
import os
import click
from Blockchain import Blockchain


@click.command()
@click.argument('cmd', required=True)
@click.option('-n', '--name', 'name', type=str, help='create the blockchain by the given name')
@click.option('-a', '--address', 'address', type=str, help='account address')
@click.option('-u', '--username', 'username', type=str, help='create a new user one the blockchain')
@click.option('-b', '--balance', 'balance', type=int, help='value to add to or substract from account balance')
@click.option('-h', '--height', 'height', type=int, help='Print blocks with the given height in the blockchain')
@click.option('-d', '--direction', 'direction', type=str, help='The direction of print block funcion (front or back)')
@click.option('-from', 'src', type=str, help='transaction source')
@click.option('-to', 'dest', type=str, help='transaction destination')
@click.option('-amount', 'amount', type=int, help='transaction value')
@click.option('-o', '--option', 'option', type=str, help='The option for several commands, force: fire transactions')
@click.option('-r', '--repetition', 'rep', type=int, help='How many times to send a same transaction')
def main(cmd, name, address, username, balance, height, direction, src, dest, amount, option, rep):
    path = os.getcwd() + '/data'
    info_path = path + '/info'
    data_path = path + '/data'

    blockchain = Blockchain()
    cmd = cmd.lower()
    print(f'Command: {cmd}')
    print(f'Path: {path}')
    # decide whether to initialize the blockchain or read previous records
    if (not os.path.exists(data_path) or len(os.listdir(data_path))) == 0 and cmd != 'createblockchain':
        print('You haven\'t create a blockchain !!!')
        return
    elif cmd == 'createblockchain':
        # decide whether to initialize the blockchain or read previous records
        if os.path.exists(data_path) and len(os.listdir(data_path)) != 0:
            print('You had create a blockchain!!!')
            return
        else:
            wallet = blockchain.initialize(name)
            print(f'You wallet address is: {wallet.address} .')
    else:
        blockchain.read_blockchain()
        if cmd == 'createuser':
            if not username:
                print('You have to provide ad username!!!')
                return

            wallet = blockchain.create_user(username)
            print(f'User wallet address is: {wallet.address}')

        elif cmd == 'addbalance':
            if not address or not balance:
                print('You miss some argument!!!')
                return

            if balance <= 0:
                print('The amount must be greater than 0!!!')
                return

            blockchain.increment_balance(address, balance)

        elif cmd == 'send':
            if not src or not dest or not amount:
                print('You miss some argument!!!')
                return

            if not rep:
                rep = 1

            elif rep <= 0:
                print('Repetitiion must be positive!!!')
                return

            for i in range(rep):
                blockchain.add_transaction(src, dest, amount)

            if option and option == 'force':
                blockchain.fire_transactions(blockchain._root_address)

        elif cmd == 'getbalance':
            if not address:
                print('You have to give you account address!!!')
                return

            balance = blockchain.get_balance(address)
            print(f'Address: {address}')
            print(f'Balance = {balance}')

        # print the block chain with the given height
        elif cmd == 'printchain':
            blockchain.print_blocks()

        elif cmd == 'printblock':
            blockchain.print_blocks(height, direction)

        elif cmd == 'cli':
            pass


if __name__ == '__main__':
    main()
