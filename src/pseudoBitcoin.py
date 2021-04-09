#!/usr/bin/env python3
import sys
import os
import click
from Blockchain import Blockchain
from Command import execute


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

    # if :
    #     print("You haven't create a blockchain!!!")
    #     return

    cmd = cmd.lower()

    arg = {'cmd': cmd,
           'name': name,
           'address': address,
           'username': username,
           'balance': balance,
           'height': height,
           'direction': direction,
           'src': src,
           'dest': dest,
           'amount': amount,
           'rep': rep,
           'option': option}

    execute(arg)


if __name__ == '__main__':
    main()
