import concurrent.futures
import json

import funcy

from api_camara import todos_deputados, add_comissao_status, add_presenca


@funcy.print_durations()
def main():
    deputados = todos_deputados()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        deputados = executor.map(add_comissao_status, deputados)
        deputados = executor.map(add_presenca, deputados)

    with open('teste.json','w') as arq:
        json.dump(list(deputados), arq, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()