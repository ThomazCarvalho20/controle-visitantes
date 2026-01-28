# Create your views here.
# Importa a função render, usada para renderizar (exibir) templates HTML
# e retornar uma resposta HTTP ao navegador
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Importa a classe HttpResponse, que representa uma resposta HTTP direta
# (não está sendo usada neste código, mas poderia ser usada para retornar texto simples)
#from django.http import HttpResponse
from visitantes.models import Visitantes

from django.utils import timezone

"""
Poderia ser usado assim:
def index(request):
    return HttpResponse("Olá, mundo! Esta é a página inicial.")
"""
# Define uma view chamada "index"
# Toda view Django recebe obrigatoriamente o objeto "request",
# que contém informações sobre a requisição feita pelo usuário

@login_required
def index(request):
    # Renderiza o arquivo "index.html" e retorna uma resposta HTTP
    # O Django procura esse arquivo dentro da pasta "templates"
    todos_visitantes = Visitantes.objects.order_by("-horario_chegada") #Busca todos os visitantes no banco de dados ordenados pela data de chegada (do mais recente para o mais antigo)
    
    visitantes_aguardando = todos_visitantes.filter(status='AGUARDANDO') #Filtra os visitantes que estão aguardando

    visitantes_em_visita = todos_visitantes.filter(status='EM_VISITA') #Filtra os visitantes que estão em visita
    
    visitantes_finalizados = todos_visitantes.filter(status='FINALIZADO') #Filtra os visitantes que finalizaram a visita
    
    hora_atual = timezone.now() #Pega a hora atual do sistema
    mes_atual = hora_atual.month #Pega o mês atual

    visitantes_mes = todos_visitantes.filter(horario_chegada__month=mes_atual) #Filtra os visitantes do mês atual

    context = { #Dicionário que passa variáveis para o template HTML
        "nome_pagina": "Início na dashboard", 
        "todos_visitantes": todos_visitantes, 
        "visitantes_aguardando": visitantes_aguardando.count(),
        "visitantes_em_visita": visitantes_em_visita.count(),
        "visitantes_finalizados": visitantes_finalizados.count(),
        "visitantes_mes": visitantes_mes.count(),
    }
    return render(request, "index.html", context)