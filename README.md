# Sistema distribuido de controle de estoque com GRPC

Para instalar o sistema primeiro é necessario instalar o python.

Caso esteja em um sistema windows siga o seguinte passo a passo [aqui](https://wiki.python.org/moin/BeginnersGuide/Download)

A maioria das distribuições linux já ve com linux pre instalado, todavia em distribuições baseadas em debian basta executar 

```commandline
 sudo apt install python3
```

Caso sua distribuição não seja baseada em debian faça uma busca rapida de como instalar o python em sua distro

Com python devidamente instalado será necessario instalar também alguma bibliotecas:

* grpc
* lmdb
* pysybcobj

para isso execute os seguinte comandos

```commandline
pip install grpcio-tools
```

```commandline
pip install lmdb
```

```commandline
pip install pysyncobj
```

Com as bibliotecas já instaladas agora você deve clonar este projeto em sua maquina. Para isso instale e configure o git (você pode seguir o sequinte [tutorial](https://git-scm.com/download/win))

Agora no interpretador de comandos ou no bash do git, caso esteja em uma sistema windows, execute o seguinte comando

```commandline
git clone https://github.com/LucasAraujoUfu/SDTrab.git
```

Vá até a pasta onde o projeto foi clonado e execute os servidores

```commandline
python admin_server.py
```

```commandline
python order_server.py
```

Com ambos servidores rodando é possivel conectar os clients para isso execute os seguintes comandos

```commandline
python admin_client.py
```

```commandline
python order_client.py
```

OBS.: Os servidores trabalham idependente um do outro da mesma forma que os clientes, todavia vale ressaltar que o admin_client depende do admin_server da mesma forma que o order_client depende do order server.

OBS2.: Esse programa faz syscalls as quais só foram testadas em sistema Linux e talvez essas não funcionem corretamente em outros sistemas.

Video demonstrativo: [Link]
