# gsuite-tools
Hack para manipular coisas da Google usando o Selenium

## Importante
A parte de lista está quebrada: a Google mudou o formato do Groups. Contudo o login ainda funciona.

Agora temos Google Drive. 

### Dependências:
  * python 3.x
  * Instalação das dependências de python listadas em requirements.txt (pode ser via sistema);
  * firefox (sistema);
  * xvfb (sistema).
  * geckodriver (não tem pacote no debian)

Baixar o [geckodriver](https://github.com/mozilla/geckodriver/releases/latest) e descompactar
em um diretório. Colocar no PATH, exemplo:

    export PATH=$PATH:/home/usuario/geckodriver

### Instalação:
  * clonar o repositório;
  * instalar as dependências;
  * gerar um arquivo `.env` tal qual o exemplo.

### Como achar a chave?
Para achar a chave:
  * abra um drive compartilhado com o developer mode ativado;
  * filtre por `v2internal`;
  * mande mostrar os cabeçalhos. Estará na URL como variável GET.

### Como rodar
```console
python3 drive.py 0AI4iTmGhBORVUk9PVA -l
```

Caso já existir o cookie de uma execução anterior, basta suprimir a opção ``--login``.
```console
python3 drive.py 0AI4iTmGhBORVUk9PVA
```

### Como rodar com Docker
```console
# assumiremos que foi clonado para /tmp/gsuite-tools
#             que COOKIE=cookie

docker build -t gsuite-tools .
touch cookie
docker run --rm --env-file .env -v /tmp/gsuite-tools/cookie:/root/gsuite-tools/cookie -it gsuite-tools python3 drive.py 0AI4iTmGhBORVUk9PVA -l
```
