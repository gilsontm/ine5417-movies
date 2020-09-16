Implementação do trabalho de Engenharia de Software I (2020.1)

==================================================================================
### SETUP

# Instalar node e npm
O npm é um gerenciador de dependências para o NodeJS, que será usado para instalar bibliotecas e rodar o serviço frontend.
```
    sudo apt install nodejs
    sudo apt install npm
```

# Instalar sqlite3
É o gerenciador do banco sqlite.
```
    sudo apt install sqlite3
```


# Instalar dependências do Python
Obs: É recomendado usar um virtual environment nessa parte, mas não é obrigatório.

Na pasta root do projeto, execute:
```
    pip install -r requirements.txt
```

# Instalar dependências do frontend
Na pasta root do projeto:
```
    cd frontend
    npm install
```
==================================================================================

### EXECUTAR

# Frontend
Na pasta root do projeto, execute:
```
    cd frontend
    npm run serve
    [terminal ficará travado aqui]
```

O servidor frontend "servirá" as páginas web para o endereço http://localhost:8080

# Backend
Na pasta root do projeto, execute:
```
    cd backend
    python main.py
    [terminal ficará travado aqui]
```

O servidor backend ficará ouvindo a porta 8888, esperando por requisições do servidor frontend.
==================================================================================
