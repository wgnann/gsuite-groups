# gsuite-groups
Hack para manipular coisas do Google Groups usando o Selenium

## Importante
A parte de lista está quebrada: a Google mudou o formato do Groups. Contudo o login ainda funciona.

Agora temos Google Drive. 

### Dependências:
  * python 3.x
  * Instalação das dependências de python listadas em requirements.txt;
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

### Como rodar
```console
python3 drive.py 0AI4iTmGhBORVUk9PVA -l
```

Caso já existir o cookie de uma execução anterior, basta suprimir a opção ``--login``.
```console
python3 drive.py 0AI4iTmGhBORVUk9PVA
```
