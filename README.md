# gsuite-groups
Hack para manipular listas do Google Groups usando o Selenium

## Importante
Está quebrado: a Google mudou o formato do Groups. Contudo o login ainda funciona.

### Dependências:
  * python 3.7
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
Para inscrever membros na lista, usar a opção `subscribe`. Ele pedirá para digitar os endereços, um por linha, e esperará um `CTRL+D` para encerrar o arquivo.
```console
python3 listas.py subscribe sua-lista-de-email@ime.usp.br
```

Outra opção é fazer um pipe.
```console
cat sua-lista-antiga | python3 listas.py subscribe sua-lista-de-email@ime.usp.br
```

Para listar membros de uma lista, usar a opção `list`. Ele reaproveita cookies caso existirem. Para rodar o `list` e gerar um cookie, usar a opção `--login`.
```console
python3 listas.py list --login sua-lista-de-email@ime.usp.br
```

Caso já existir o cookie de uma execução anterior, basta suprimir a opção ``--login``.
```console
python3 listas.py list sua-lista-de-email@ime.usp.br
```
