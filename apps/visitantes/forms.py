from django import forms
from visitantes.models import Visitantes

class VisitanteForm(forms.ModelForm): # Formulário para o modelo Visitante
    class Meta: # Metadados do formulário
        model = Visitantes # Modelo associado ao formulário
        fields = {"nome_completo", "cpf", "data_nascimento", "numero_casa", "placa_veiculo"
        } # Campos do modelo que serão incluídos no formulário
        error_messages = {
            "nome_completo": {
                "required": "O nome completo é obrigatório."
            },
            "cpf": {
                "required": "O CPF é obrigatório."
            },
            "data_nascimento": {
                "required": "A data de nascimento é obrigatória.",
                "invalid": "Insira uma data de nascimento válida e o seu formato é DD/MM/AAAA.",
            },
            "numero_casa": {
                "required": "O número da casa é obrigatório.",
            },
            "placa_veiculo": {
                "required": "A placa do veículo é obrigatória.",
                "max_length": "A placa do veículo não pode exceder 7 caracteres."
            }
        } # Mensagens de erro personalizadas para os campos do formulário
        
class AutorizacaoVisitanteForm(forms.ModelForm): # Formulário para autorizar visitantes
    
    morador_responsavel = forms.CharField( # Campo para o morador responsável
        required=True
    )
    
    class Meta: # Metadados do formulário
        model = Visitantes # Modelo associado ao formulário
        fields = {"morador_responsavel"} # Campo do modelo que será incluído no formulário
        error_messages = { # Mensagem de erro personalizada
            "morador_responsavel": {
                "required": "O nome do morador responsável é obrigatório para autorizar a entrada do visitante."
            }
        } # Mensagem de erro personalizada para o campo do formulário