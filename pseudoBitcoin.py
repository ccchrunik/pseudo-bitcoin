#!/usr/bin/env python3
import sys
import click
from Blockchain import Blockchain


@click.command()
@click.option('-t', '--transactions')
def main(tx, ):
    print("main function")
    print(sys.argv)


if __name__ == '__main__':
    # main()
    greeting()
