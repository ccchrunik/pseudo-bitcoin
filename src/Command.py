from Blockchain import Blockchain
import os


def singledispatch(fn):
    """The dispatcher function for command line

    Parameters:
    ----------
    fn : function pointer
        the function entry point for the execution

    Returns:
    ----------
    decorator : function pointer
        the wrapper inner function to automatically dispatch based on the command
    """
    registry = dict()

    registry['error'] = fn

    # Register different commands
    def register(cmd):
        def inner(fn):
            registry[cmd] = fn
            return fn
        return inner

    # Dispatch different commands
    def decorator(arg):
        fn = registry.get(arg['cmd'], registry['error'])
        return fn(arg)

    # Get dispatch command function
    def dispatch(arg):
        return registry.get(arg['cmd'], registry['error'])

    decorator.register = register
    decorator.registry = registry.keys()
    decorator.dispatch = dispatch

    return decorator


@ singledispatch
def execute(arg):
    """General entry point of the command line execution function"""
    print('Invalid command!!!')
    return


@ execute.register('createblockchain')
def execute_create_blockchain(arg):
    """Create a blockchain

    Parameters:
    ----------
    name : str
        the root user name
    """
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
        if name is None:
            print('You have to provide the root user name!!!')
            return

        wallet = blockchain.initialize(name)
        print(f'You wallet address is: {wallet.address} .')

    return


@ execute.register('createuser')
def execute_create_user(arg):
    """Create a new user

    Parameters:
    ----------
    username : str
        the name of the new user
    """
    blockchain = Blockchain()
    blockchain.read_blockchain()

    username = arg['username']

    if username is None:
        print('You have to provide an username!!!')
        return

    wallet = blockchain.create_user(username)
    print(f'User wallet address is: {wallet.address}')


@ execute.register('addbalance')
def execute_add_balance(arg):
    """Add some value to a wallet

    Parameters:
    ----------
    address : Wallet.address (str)
        the wallet address

    balance : int
        the amount of value to be added to the wallet
    """
    blockchain = Blockchain()
    blockchain.read_blockchain()

    address = arg['address']
    balance = arg['balance']

    if address is None:
        print('You have to give you account address!!!')

    elif balance is None:
        print('You have to give the balance!!!')

    elif not blockchain._wallet_pool.has_address(address):
        print(f'The address {address} does not exist!!!')

    elif balance <= 0:
        print('The amount must be greater than 0!!!')

    else:
        blockchain.increment_balance(address, balance)
        print(f'Add value {balance} to {address}!!!')

    return


@ execute.register('getbalance')
def execute_get_balance(arg):
    """Print the balance of the wallet

    Parameters:
    ----------
    address : Wallet.address (str)
        the wallet address
    """
    blockchain = Blockchain()
    blockchain.read_blockchain()

    address = arg['address']

    if address is None:
        print('You have to give you account address!!!')

    elif not blockchain._wallet_pool.has_address(address):
        print(f'The address {address} does not exist!!!')

    else:
        balance = blockchain.get_balance(address)
        print(f'Address: {address}')
        print(f'Balance = {balance}')

    return


@ execute.register('send')
def execute_send(arg):
    """Add a transaction to the blockchain

    Parameters:
    ----------
    src : Wallet.address (str)
        the sender wallet address

    dest : Wallet.address (str)
        the receiver wallet address

    amount : int
        the amount of value to be transferred

    rep : int
        the number of the same transactions to be added

    option : str
        the additional option for this transaction (only have 'force' now)
    """
    blockchain = Blockchain()
    blockchain.read_blockchain()

    src = arg['src']
    dest = arg['dest']
    amount = arg['amount']

    if src is None:
        print('You have to provide sender address!!!')
        return

    elif dest is None:
        print('You have to provide receiver address!!!')
        return

    elif amount is None:
        print('You have to provide amount of value to be transferred!!!')
        return

    elif amount <= 0:
        print('Amount of value must be greater than 0!!!')
        return

    rep = arg['rep']

    if rep is None:
        rep = 1

    elif rep <= 0:
        print('Repetition must be positive!!!')
        return

    for i in range(rep):
        blockchain.add_transaction(src, dest, amount)
        print('Add a transaction to the blockchain!!!\n')

    option = arg['option']

    # Force the blockchain to group transactions into a block
    if option is not None and option == 'force':
        blockchain.fire_transactions(blockchain._root_address)
    elif option is not None and option != 'force':
        print('The additional option is invalid!!!')


@ execute.register('printchain')
def execute_print_chain(arg):
    """Print the whole blockchain"""
    blockchain = Blockchain()
    blockchain.read_blockchain()
    blockchain.print_blocks()


@ execute.register('printblock')
def execute_print_block(arg):
    """Print part of the blockchain

    Parameters: 
    ----------
    height : int
        the number of the blocks to be printed

    direction : str
        the direction to print the blocks (only have 'front' and 'back')
    """
    blockchain = Blockchain()
    blockchain.read_blockchain()

    height = arg['height']
    direction = arg['direction']

    if height is None:
        print('You must provide the height!!!')

    else:
        blockchain.print_blocks(height, direction)

    return


if __name__ == '__main__':
    execute('error', dict())
