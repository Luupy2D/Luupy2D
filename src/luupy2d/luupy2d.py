import argparse
from pathlib import Path
import sys
import shutil

def new_game():
    print("Executando rotina de criação diretórios")
    target= Path.cwd()

    try:
        #gerar as pastas
        (target / "assets" / "graphics").mkdir(parents=True,exist_ok=True)
        (target / "assets" / "sounds").mkdir(parents=True,exist_ok=True)
        (target / "stages").mkdir(parents=True,exist_ok=True)

        #copiar o main.py padrão
        src_folder = Path(__file__).resolve().parent
        main_script = src_folder / "demos" / "default" / "main.py"

        #print(f"o path do script: {main_script}")

        if main_script.exists():
            shutil.copy(main_script, target / "main.py")
        else:
            raise FileNotFoundError("main.py not found.")

    except Exception as e:
        print(f"Erro ao criar o projeto: {e}")

def play_game():
    print("Executar jogo!!")
    target = Path.cwd()
    try:
        main_script = target / "main.py"
        if main_script.exists():
            sys.path.insert(0, target)
            code = main_script.read_text(encoding="utf-8")

            exec(code, {"__name__": "__main__", "__file__": str(main_script)})
        else:
            raise FileNotFoundError("main.py not found.")
        
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")

def load_demo(demoname):
    target = Path.cwd()
    try:
        src_folder = Path(__file__).resolve().parent
        demo = src_folder / "demos" / demoname
        if demo.exists():
            #print(f"a pasta existe! {demo}")
            (target / "assets" / "graphics").mkdir(parents=True,exist_ok=True)
            (target / "assets" / "sounds").mkdir(parents=True,exist_ok=True)
            (target / "stages").mkdir(parents=True,exist_ok=True)

            shutil.copytree(demo, target, dirs_exist_ok=True)

        else:
            raise FileNotFoundError(f"folder {demoname} does not exists.")

    except Exception as e:
        print(f"Erro ao carregar demo: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Framework pedagógico para criação de jogos!"
    )

    #tratando dos comandos com subparsers
    subparsers = parser.add_subparsers(dest="command", help="comandos disponíveis")
    parser_new = subparsers.add_parser(
        "new", help="cria todas as pastas necessárias para iniciar a construção de um novo jogo.")

    parser_play = subparsers.add_parser(
        "play", help="executa o jogo a partir do arquivo main.py.")

    parser_load = subparsers.add_parser(
        "load", help="carrega um exemplo ou demonstração.")
    parser_load.add_argument("demo",type=str, help="nome da demo a ser carregada.")

    args = parser.parse_args()
    if args.command == "new":
        new_game()
    elif args.command == "play":
        play_game() 
    elif args.command == "load":
        load_demo(args.demo)
    else:
        #print("Bem vindo! Use o programa com essas opções:")
        print(parser.format_help())


if __name__ == "__main__":
    main()
