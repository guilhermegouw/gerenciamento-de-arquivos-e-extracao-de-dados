# API para Upload e Manipulação de arquivos de texto.

## Descrição
Esta API permite o upload e a manipulação de arquivos de texto, oferecendo endpoints para listar arquivos, 
recuperar informações específicas sobre usuários com maior ou menor tamanho de mensagem, 
listar usuários ordenados por nome e listar usuários dentro de um intervalo de mensagens.
A API é construída com Django e Django REST Framework.

## Endpoints
### Upload de Arquivos

- **Upload de arquivo**: `PUT /upload/` 
  - Response: `201 Created` (Arquivo não existia e foi criado)
  - Response: `204 No Content` (Já existia um arquivo com o mesmo nome e foi substituído)
  - Response: `400 Bad Request` (Nome de arquivo não permitido)

Exemplo de requisição usando curl:
```bash
curl -X PUT -F "file=@/path/to/the/file/example" http://127.0.0.1:8000/upload/
``` 

### Listagem de Arquivos

- **Listagem de arquivo**: `GET /files/` 
  - Response: `200 OK` (Devolve a lista de arquivos mesmo quando vazía.)
  - A resposta é composta por 4 campos: "count", "next", "previous", "results".
    - "count" é o número de arquivos.
    - "next" é o link para a próxima página.
    - "previous" é o link para a página anterior.
    - "results" é uma lista de arquivos.

Exemplo de requisição usando curl:
``` 
curl -X GET "http://127.0.0.1:8000/files/"
```

### Usuário com Maior Tamanho
- **Usuário com maior tamanho**: `GET /files/user_max_size/<file_name>/`
  - Response: 200 OK (Dados do arquivo retornados com sucesso)
  - Response: 404 Not Found (Arquivo não encontrado)
  - A resposta é composta por 4 campos: "username", "folder", "numberMessages", "size".
    - "username" é o nome do usuário.
    - "folder" é o nome da pasta.
    - "numberMessages" é o número de mensagens.
    - "size" é o tamanho do arquivo.

Exemplo de requisição usando curl:

```
curl -X GET "http://127.0.0.1:8000/files/user_max_size/input"
```

### Usuário com Menor Tamanho
- **Usuário com menor tamanho**: `GET /files/user_min_size/<file_name>/`
  - Response: 200 OK (Dados do arquivo retornados com sucesso)
  - Response: 404 Not Found (Arquivo não encontrado)
  - A resposta é composta por 4 campos: "username", "folder", "numberMessages", "size".
    - "username" é o nome do usuário.
    - "folder" é o nome da pasta.
    - "numberMessages" é o número de mensagens.
    - "size" é o tamanho do arquivo.

Exemplo de requisição usando curl:
```
curl -X GET "http://127.0.0.1:8000/files/user_min_size/input"
```

### Listagem de Usuários Ordenados por Nome
- **Listagem de usuários ordenados por nome**: `GET /files/users/<file_name>/`
  - Response: 200 OK (Lista de usuários retornada com sucesso)
  - A resposta é composta por 4 campos: "count", "next", "previous", "results".
    - "count" é o número de usuários.
    - "next" é o link para a próxima página.
    - "previous" é o link para a página anterior.
    - "results" é uma lista de usuários, cada um com "username", "folder", "numberMessages", "size".

Exemplo de requisição usando curl:
```
curl -X GET "http://127.0.0.1:8000/files/users/input"
```

### Listagem de Usuários Ordenados por Nome (Ordem Decrescente)
- **Listagem de usuários ordenados por nome (ordem decrescente)**: `GET /files/users_desc/<file_name>/`
  - Response: 200 OK (Lista de usuários retornada com sucesso)
  - A resposta é composta por 4 campos: "count", "next", "previous", "results".
    - "count" é o número de usuários.
    - "next" é o link para a próxima página.
    - "previous" é o link para a página anterior.
    - "results" é uma lista de usuários, cada um com "username", "folder", "numberMessages", "size".

Exemplo de requisição usando curl:
```
curl -X GET "http://127.0.0.1:8000/files/users_desc/input"
```

### Listagem de Usuários por Intervalo de Mensagens
- **Listagem de usuários por intervalo de mensagens**: `GET /files/users_range_messages/<file_name>/<int:min_msgs>/<int:max_msgs>/`
  - Response: 200 OK (Lista de usuários retornada com sucesso)
  - A resposta é composta por 4 campos: "count", "next", "previous", "results".
    - "count" é o número de usuários.
    - "next" é o link para a próxima página.
    - "previous" é o link para a página anterior.
    - "results" é uma lista de usuários, cada um com "username", "folder", "numberMessages", "size".

Exemplo de requisição usando curl:
```
curl -X GET "http://127.0.0.1:8000/files/users_range_messages/input/10/100"
```

## Instalação e Configuração

### Requisitos
- Docker
- Docker Compose

### Passos de Instalação

1. Clone o repositório:
```
git clone https://github.com/guilhermegouw/gerenciamento-de-arquivos-e-extracao-de-dados 
cd gerenciamento-de-arquivos-e-extracao-de-dados
```

2. Configure as variáveis de ambiente no arquivo .env:
```
cp env-sample .env
```
Substitua as variáveis de ambiente com os valores de sua escolha.

3. Construa as imagens Docker:
```
docker-compose build
```

4. Inicie os contêineres:
```
docker-compose up web
```
A aplicação estará disponível em `http://127.0.0.1:8000/`.

### Desenvolvimento e Testes
Para rodar o ambiente de desenvolvimento e executar testes:

```
docker-compose up web-dev
```

### Limpeza
Para parar e remover os contêineres e imagens:

```
docker-compose down --rmi all --volumes --remove-orphans
```
