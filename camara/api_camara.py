import xml.etree.ElementTree as ET

import funcy
import requests

LEGISLATURA_ATUAL = '55'
INICIO_LEGISLATURA = '1/2/2015'
FIM_LEGISLATURA = '30/12/2018'

URL_TODOS_DEPUTADOS = 'http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDeputados'
URL_DETALHE_DEPUTADO = 'http://www.camara.leg.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado'
URL_PRESENCAS = 'http://www.camara.leg.br/SitCamaraWS/sessoesreunioes.asmx/ListarPresencasParlamentar'
URL_PROPOSICOES = 'http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes'


# TODO: Add funcy cache e excepion handler
@funcy.print_durations()
def todos_deputados():
    req = requests.get(URL_TODOS_DEPUTADOS)
    xml_deputados = ET.fromstring(req.text)
    for dep_elem in xml_deputados:
        yield {d.tag: d.text for d in dep_elem}


@funcy.print_durations
def add_comissao_status(deputado):
    req = requests.get(URL_DETALHE_DEPUTADO,
                       params={'ideCadastro': deputado.get('ideCadastro'), 'numLegislatura': LEGISLATURA_ATUAL})
    xml_detalhes = ET.fromstring(req.text)

    comissoes_por_tipo_membro = funcy.group_by(lambda c: c.find('condicaoMembro').text,
                                               funcy.first(xml_detalhes.iter('comissoes')))
    deputado['comissoes_stats'] = funcy.walk_values(len, comissoes_por_tipo_membro)

    return deputado


@funcy.print_durations
def add_presenca(deputado):
    req = requests.get(URL_PRESENCAS,
                       params={'dataIni': INICIO_LEGISLATURA, 'dataFim': FIM_LEGISLATURA,
                               'numMatriculaParlamentar': deputado['matricula']})
    xml_presenca = ET.fromstring(req.text)

    dias = funcy.first(xml_presenca.iter('diasDeSessoes2'))

    sessoes = funcy.cat(d.find('sessoes').findall('sessao') for d in dias)
    sessoes_por_status = funcy.group_by(lambda s: s.find('frequencia').text, sessoes)
    deputado['presencas_stats'] = funcy.walk_values(len, sessoes_por_status)

    return deputado


@funcy.print_durations
def add_proposicoes(deputado):
    req = requests.get(URL_PROPOSICOES,
                       params={
                           "sigla": "", "numero": "", "ano": "",
                           "datApresentacaoIni": INICIO_LEGISLATURA,
                           "datApresentacaoFim": "",
                           "parteNomeAutor": deputado.get('nomeParlamentar').replace("'", " "),
                           "idTipoAutor": "", "siglaPartidoAutor": "", "siglaUFAutor": "", "generoAutor": "",
                           "codEstado": "", "codOrgaoEstado": "", "emTramitacao": ""
                       })
    xml_proposicoes = ET.fromstring(req.text)
    proposicoes = xml_proposicoes.findall('proposicao')
    proposicoes = filter(lambda p: p.find('autor1').find('idecadastro').text == str(deputado['ideCadastro']),
                         proposicoes)
    prop_por_tipo = funcy.group_by(lambda p: p.find('tipoProposicao').find('sigla').text, proposicoes)
    deputado['proposicoes_stats'] = funcy.walk_values(len, prop_por_tipo)

    return deputado
