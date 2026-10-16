# Testando
Para testar siga estes passos:

### Abra o terminal, crie um venv na pasta raiz do projeto:
```
python -m venv .venv
```
### Ative o venv:

No Windows: `.venv/Scripts/activate`.

No Linux: `source .venv/bin/activate`.

É possível também configurar o python no vscode para usar o venv automaticamente como interpretador. Veja as configurações do python no VSCODE.

### Instale o luupy2d no venv em modo editável:
```
pip install -e .
```
(**não esqueça do ponto! '.' no final do comando**)

### Pronto!
Crie uma pasta para o jogo, dentro dela teste o comando `luupy2d`!