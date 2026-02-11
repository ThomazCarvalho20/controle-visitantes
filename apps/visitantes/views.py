from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseNotAllowed
from visitantes.forms import VisitanteForm, AutorizacaoVisitanteForm
from visitantes.models import Visitantes

from django.utils import timezone

# Create your views here.
@login_required
def registrar_visitante(request): # View para registrar um novo visitante
    
    form = VisitanteForm()
    
    if request.method == "POST": # Verifica se o formulário foi submetido
        form = VisitanteForm(request.POST) # Popula o formulário com os dados submetidos
        if form.is_valid(): # Verifica se os dados são válidos
            visitante = form.save(commit=False) # Cria uma instância do modelo sem salvar no banco de dados ainda
            # Aqui você pode adicionar lógica adicional antes de salvar, se necessário
            visitante.registrado_por = request.user.porteiro  # Assume que o usuário logado é um porteiro
            visitante.save() # Salva a instância no banco de dados
            
            messages.success(
                request, "Visitante registrado com sucesso!"
            )

            return redirect("index") # Redireciona para a página inicial após o registro bem-sucedido

    context = {
        "nome_pagina": "Registrar visitante",
        "form": form
    } # Contexto para o template
    
    return render(request, 'registrar_visitante.html', context) # Renderiza o template com o contexto

@login_required
def informacoes_visitante(request, id): # View para exibir informações detalhadas de um visitante
    
    visitante = get_object_or_404(Visitantes, id=id) # Obtém o visitante pelo ID ou retorna 404 se não encontrado
    
    form = AutorizacaoVisitanteForm() # Inicializa o formulário de autorização do visitante
    
    if request.method == "POST": # Verifica se o formulário foi submetido
        form = AutorizacaoVisitanteForm(request.POST, instance=visitante) # Popula o formulário com os dados submetidos
        
        if form.is_valid(): # Verifica se os dados são válidos
            visitante = form.save(commit=False) # Salva as alterações no banco de dados
            visitante.status = "EM_VISITA" # Atualiza o status do visitante para "EM_VISITA"
            visitante.horario_autorizacao = timezone.now() # Define o horário de autorização como o horário atual
            visitante.save() # Salva a instância no banco de dados
            
            messages.success(
                request, "Visitante autorizado com sucesso!"
            )
            
            return redirect("index") # Redireciona para a página inicial após a autorização bem-sucedida
        
    
    context = {
        "nome_pagina": "Informações do visitante",
        "visitante": visitante,
        "form": form
    } # Contexto para o template
    
    return render(request, 'informacoes_visitante.html', context) # Renderiza o template com o contexto

@login_required
def finalizar_visita(request, id): # View para finalizar a visita de um visitante
    
    if request.method == "POST": # Verifica se o formulário foi submetido
        visitante = get_object_or_404(Visitantes, id=id) # Obtém o visitante pelo ID ou retorna 404 se não encontrado
        visitante.status = "FINALIZADO" # Atualiza o status do visitante para "FINALIZADO"
        visitante.horario_saida = timezone.now() # Define o horário de saída como o horário atual
        visitante.save() # Salva a instância no banco de dados
        
        messages.success(
            request, "Visita finalizada com sucesso!"
        )
    
        return redirect("index") # Redireciona para a página inicial após finalizar a visita
    else:
        return HttpResponseNotAllowed(["POST"], "Método não permitido!") # Retorna 405 se o método não for POST