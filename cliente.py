import sys

def main():
    while True:
        try:
            fun = input("> ").split()
            if len(fun) == 0:
                continue
            if fun[0] == 'exit':
                break
            elif fun[0] == 'listar':
                listar()
            elif fun[0] == 'comprar':
                comprar()
        except EOFError:
            print('exit')
            break


def listar():
    pass

def comprar():
    pass

if __name__ == '__main__':
    main()