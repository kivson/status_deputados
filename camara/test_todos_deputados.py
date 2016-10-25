from unittest import TestCase

from camara.api_camara import todos_deputados, add_comissao_status, add_presenca, add_proposicoes


class TestApiCamara(TestCase):
    def test_todos_deputados(self):
        deputados = todos_deputados()
        for dep in deputados:
            self.assertIn('ideCadastro', dep, 'Deputados possuem ideCadastro')

    def test_add_comissao_status(self):
        deputado = add_comissao_status(dict(ideCadastro=141480))
        self.assertEqual(deputado.get('comissoes_stats'), {'Titular': 8, 'Suplente': 2})

    def test_add_presenca(self):
        deputado = add_presenca(dict(matricula=371))
        self.fail()

    def test_add_proposicoes(self):
        deputado = add_proposicoes(dict(ideCadastro=141480,nomeParlamentar="LÁZARO BOTELHO"))
        print(deputado)
        self.fail()