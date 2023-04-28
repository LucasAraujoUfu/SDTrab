import sys


def main():
    while True:
        try:
            fun = input("> ").split()
            if len(fun) == 0:
                continue
            if fun[0] == 'exit':
                break
            elif fun[0] == 'cadastrar':
                if len(fun) < 4:
                    print('numero invalido de argumentos')
                    continue
                elif fun[1] == 'cliente':
                    cadastrarCliente()
                elif fun[1] == 'produto':
                    cadastrarProduto()
            elif fun[0] == 'apagar':
                if len(fun) < 3:
                    print('numero invalido de argumentos')
                    continue
                elif fun[1] == 'cliente':
                    apagarClient()
                elif fun[1] == 'produto':
                    apagarProduto()
            elif fun[0] == 'update':
                if len(fun) < 3:
                    print('numero invalido de argumentos')
                    continue
                elif fun[1] == 'cliente':
                    updateClient()
                elif fun[1] == 'produto':
                    updateProduto()
            else:
                print('Operação invalida')
        except EOFError:
            print('exit')
            break


def cadastrarCliente():
    pass

def cadastrarProduto():
    pass

def updateClient():
    pass

def updateProduto():
    pass

def apagarClient():
    pass

def apagarProduto():
    pass


if __name__ == '__main__':
    main()