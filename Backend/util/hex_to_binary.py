from Backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'a' : '1010',
    'b' : '1011',
    'c' : '1100',
    'd' : '1101',
    'e' : '1110',
    'f' : '1111'
}

def hex_to_binary(hex_string):
    binary_string = ''

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION[character]
    
    
    return binary_string

def main():
    number = 43657
    hex_number = hex(number)[2:]
    binary_number = hex_to_binary(hex_number)
    print(f"hex = {hex_number} and it's binary is {hex_to_binary(hex_number)}")

    original_number = int(binary_number, 2)
    print(f'original_number : {original_number}')

    binary_crypto_hash = hex_to_binary(crypto_hash('test_data'))
    print(f'binary_crypto_hash : {binary_crypto_hash}')

if __name__ == '__main__':
    main()