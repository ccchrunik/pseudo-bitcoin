from Blockchain import Blockchain
import os


def singledispatch(fn):
    registry = dict()

    registry['error'] = fn

    def register(cmd):
        def inner(fn):
            registry[cmd] = fn
            return fn  # we do this so we can stack register decorators!
        return inner

    def decorator(arg):
        fn = registry.get(arg['cmd'], registry['error'])
        return fn(arg)

    def dispatch(arg):
        return registry.get(arg['cmd'], registry['error'])

    decorator.register = register
    decorator.registry = registry.keys()
    decorator.dispatch = dispatch
    return decorator


@ singledispatch
def execute(arg):
    print('Invalid command!!!')
    return


@ execute.register('createblockchain')
def execute_create_blockchain(arg):
    path = os.getcwd() + '/data'
    info_path = path + '/info'
    data_path = path + '/data'

    blockchain = Blockchain()
    # Decide whether to initialize the blockchain or read previous records
    if os.path.exists(data_path) and len(os.listdir(data_path)) != 0:
        print('You had create a blockchain!!!')

    else:
        name = arg['name']
        # Check the argument has the name option
        if not name:
            print('You have to provide the root user name!!!')
            return

        wallet = blockchain.initialize(name)
        print(f'You wallet address is: {wallet.address} .')

    return


@ execute.register('createuser')
def execute_create_user(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()

    username = arg['username']
    print(arg)

    if not username:
        print('You have to provide an username!!!')
        return

    wallet = blockchain.create_user(username)
    print(f'User wallet address is: {wallet.address}')


@ execute.register('addbalance')
def execute_add_balance(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()

    address = arg['address']
    balance = arg['balance']

    if not address or not balance:
        print('You miss some argument!!!')

    elif balance <= 0:
        print('The amount must be greater than 0!!!')

    else:
        blockchain.increment_balance(address, balance)

    return


@ execute.register('getbalance')
def execute_get_balance(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()

    address = arg['address']

    if not address:
        print('You have to give you account address!!!')
        return

    balance = blockchain.get_balance(address)
    print(f'Address: {address}')
    print(f'Balance = {balance}')


@ execute.register('printchain')
def execute_print_chain(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()
    blockchain.print_blocks()


@ execute.register('printblock')
def execute_print_block(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()

    height = arg['height']
    direction = arg['direction']

    blockchain.print_blocks(height, direction)


@ execute.register('send')
def execute_send(arg):
    blockchain = Blockchain()
    blockchain.read_blockchain()

    src = arg['src']
    dest = arg['dest']
    amount = arg['amount']
    option = arg['option']

    if not src or not dest or not amount:
        print('You miss some argument!!!')
        return

    if not rep:
        rep = 1

    elif rep <= 0:
        print('Repetition must be positive!!!')
        return

    for i in range(rep):
        blockchain.add_transaction(src, dest, amount)

    if option and option == 'force':
        blockchain.fire_transactions(blockchain._root_address)


if __name__ == '__main__':
    execute('error', dict())
