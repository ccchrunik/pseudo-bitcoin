#!/usr/bin/env python3
import sys
import os
import click
from Blockchain import Blockchain


@click.command()
@click.argument('cmd', required=True)
@click.option('-a', '--address', 'address', help='create the blockchain')
@click.option('-t', '--transaction', 'tx', help='Add trasactions')
@click.option('-h', '--height', 'height', type=int, help='Print blocks with the given height in the blockchain')
@click.option('-d', '--direction', 'direction', help='The direction of print block funcion (front or back)')
@click.option('-from', 'src', help='transaction source')
@click.option('-to', 'dest', help='transaction destination')
@click.option('-amount', 'amount', help='transaction value')
def main(cmd, address, tx, height, direction, src, dest, amount):
    blockchain = Blockchain()
    cmd = cmd.lower()
    print(f'Command: {cmd}')
    print(f'tx = {tx}')
    # decide whether to initialize the blockchain or read previous records
    if len(os.listdir('./data')) == 0 and cmd != 'createblockchain':
        print('You haven\'t create a blockchain !!!')
        return
    elif cmd == 'createblockchain':
        # decide whether to initialize the blockchain or read previous records
        if len(os.listdir('./data')) != 0:
            print('You had create a blockchain!!!')
            return
        else:
            blockchain.initialize(address)

    blockchain.read_blocks()
    if cmd == 'addblock':
        if tx and tx[0] == '{' and tx[-1] == '}':
            print('Invalid Command: You may use "addmultiblocks -t" !!!')
        blockchain.add_block([tx])
    # print the block chain with the given height
    elif cmd == 'printchain':
        for block in blockchain._blocks:
            print(block)

    elif cmd == 'printblock':
        if height and height < 0:
            print('Invalid Command: The height must be greater than 0 !!!')
        elif height == 0:
            print('Print nothing!')
        elif height > len(blockchain._blocks):
            print(
                'Invalid Command: The height must be less than or equal to the height of the blockchain !!!')
        else:
            if direction and direction == 'back':
                length = len(blockchain._blocks)
                for i in range(length - 1, length - height - 1, -1):
                    print(blockchain._blocks[i])
            else:
                for i in range(height):
                    print(blockchain._blocks[i])
    elif cmd == 'send':
        if not src or not dest:
            print('Invalid Command: You should give two address !!!')
        else:
            pass
    elif cmd == 'cli':
        pass


if __name__ == '__main__':
    main()
