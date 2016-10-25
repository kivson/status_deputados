import concurrent.futures
import json

import funcy

from camara.api_camara import todos_deputados, add_comissao_status, add_presenca, add_proposicoes


@funcy.print_durations()
def main():
    deputados = todos_deputados()

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        deputados = executor.map(add_comissao_status, deputados)
        deputados = executor.map(add_presenca, deputados)
        deputados = executor.map(add_proposicoes, deputados)

    with open('saida.json','w') as arq:
        json.dump(list(deputados), arq, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()