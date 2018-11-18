from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from core.forms import DecisorForm, NomeProjetoForm, AlternativaForm, CriterioForm, AvaliacaoForm, AvaliacaoTempForm
from core.models import Projeto, Decisor, Alternativa, Criterio

# aux functions
def _inclui_decisor_no_projeto(projeto, decisor):
    projeto.decisores.add(decisor)
    return


def index(request):
    """ 
    1 - cadastrar somente nome do projeto e redirecionar para cadastrar decisores - OK
    2 - cadastrar decisores - OK
    3 - atualizar cadastro do projeto com decisores - OK
    4 - cadastra Alternativas - OK
    5 - cadastra Criterios - OK
    6 - cadastra Peso
    7 - avalia Critérios
    8 - coloca resultado final da avaliação no projeto
    """
    template_name = 'index.html'
    projetos = Projeto.objects.all()

    if request.method == "POST":
        nome_projeto_form = NomeProjetoForm(request.POST)
        if nome_projeto_form.is_valid():
            projeto_novo = nome_projeto_form.save()

        return redirect('cadastradecisores', projeto_id=projeto_novo.id)

    else:
        nome_projeto_form = NomeProjetoForm()

    return render(request, template_name, {
                'nome_projeto_form': nome_projeto_form,
                'projetos': projetos})


def projeto(request, projeto_id):
    template_name = 'projeto.html'
    projeto = Projeto.objects.get(id=projeto_id)
    decisores = Decisor.objects.filter(projeto=projeto_id)
    alternativas = Alternativa.objects.filter(projeto=projeto_id)
    criterios = Criterio.objects.filter(projeto=projeto_id)


    return render(request, template_name, {
                'projeto': projeto,
                'decisores': decisores,
                'alternativas': alternativas,
                'criterios': criterios})


def cadastradecisores(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_decisores.html'
    projeto_nome = projeto.nome
    decisores = Decisor.objects.filter(projeto=projeto_id)

    if request.method == 'POST':
        decisor_form = DecisorForm(request.POST)
        if decisor_form.is_valid():
            decisor_novo = decisor_form.save()
            _inclui_decisor_no_projeto(projeto, decisor_novo)
            decisor_novo.projeto = projeto
            decisor_novo.save()

    else:
        decisor_form = DecisorForm()

    return render(request, template_name, {
                'decisor_form': decisor_form, 
                'decisores': decisores, 
                'projeto_nome': projeto_nome,
                'projeto_id': projeto_id})


def cadastraalternativas(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_alternativas.html'
    projeto_nome = projeto.nome
    alternativas = Alternativa.objects.filter(projeto=projeto_id)

    if request.method == 'POST':
        alternativa_form = AlternativaForm(request.POST)
        if alternativa_form.is_valid():
            alternativa_nova = alternativa_form.save()
            alternativa_nova.projeto = projeto
            alternativa_nova.save()

    else:
        alternativa_form = AlternativaForm()

    return render(request, template_name, {
                'alternativa_form': alternativa_form,
                'alternativas': alternativas,
                'projeto_nome': projeto_nome,
                'projeto_id': projeto_id})


def cadastracriterios(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_criterios.html'
    projeto_nome = projeto.nome
    criterios = Criterio.objects.filter(projeto=projeto_id)

    if request.method == 'POST':
        criterio_form = CriterioForm(request.POST)
        if criterio_form.is_valid():
            criterio_novo = criterio_form.save()
            criterio_novo.projeto = projeto
            criterio_novo.save()
    
    else:
        criterio_form = CriterioForm()

    return render(request, template_name, {
                'criterio_form': criterio_form,
                'criterios': criterios,
                'projeto_nome': projeto_nome,
                'projeto_id': projeto_id,
    })


def avaliarcriterios(request, projeto_id):
    # mudar nome para avaliarcriterios
    '''
    - avaliar criterios (cada decisor)
    - avaliar alternativas (cada decisor) ==> outra view
    - normalizar para gerar lista de pesos
    - calcular peso final
    - normalizar alternativas
    - somar alternativa por criterio
    - 
    
    ''' 
    # template_name = 'avaliacao.html'
    template_name = 'avaliacao_temp.html'
    # projeto_id = '1'
    projeto_id = projeto_id
    # decisores = list(Decisor.objects.filter(projeto=projeto_id).values_list('id', 'nome'))
    decisores = list(Decisor.objects.filter(projeto=projeto_id, avaliou_criterios=False).values_list('id', 'nome'))
    criterios_id = Criterio.objects.filter(projeto=projeto_id).values_list('id', flat=True)

    if not decisores:
        return redirect('https://www.google.com/search?q=avaliar_alternativas')

    combinacoes_criterios = _gerar_combinacoes_criterios(criterios_id)

    # virar uma funcao?
    criterios_combinados = []
    for i in combinacoes_criterios:
        nome_criterio1 = Criterio.objects.get(id=i[0]).nome
        nome_criterio2 = Criterio.objects.get(id=i[1]).nome

        criterios_combinados.append(
            (nome_criterio1, nome_criterio2, i[0], i[1])
        )

    if request.method == 'POST':
        print(request.POST)
        # atualizo o decisor com True (avaliou)
        decisor_id = request.POST['decisor_id']
        decisor = Decisor.objects.get(id=decisor_id)
        decisor.avaliou_criterios = True
        decisor.save()

        return redirect('avaliarcriterios', projeto_id)

    return render(request, template_name, {
                'decisores': decisores,
                'criterios_combinados': criterios_combinados,
                })

        # grava no banco 
        # tabela avaliação_criterios
        # projeto = projeto_id
        # decisor = decisor.id
        # criterios = criterios
        # valor = 3
        # print(f'd{decisor1.id}{criterios}')
    

# def avaliar_criterios(request, projeto_id, decisor):



#### gerar combinacoes #####
from itertools import product

def _gerar_combinacoes_criterios(criterios):
    criterios_keys = criterios
    
    # criterios_keys = criterios.keys()
    # criterios_keys = ['c1', 'c2', 'c3', 'c4']

    # permsList = []
    genComb = product(criterios_keys, repeat=2)

    combinacoes = []
    for subset in genComb:
        l = list(subset)
        l.reverse()
        subset_reversed = tuple(l)

        if not subset[0] == subset[1]:
            if subset not in combinacoes  and subset_reversed not in combinacoes:
                combinacoes.append(subset)

    return combinacoes
#### gerar combinacoes
