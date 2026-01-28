from django.db import models

# Create your models here.
class Visitantes(models.Model): # Modelo para armazenar informações dos visitantes
    
    STATUS_VISITANTE = [ # Opções de status do visitante
        ("AGUARDANDO", "Aguardando autorização"),
        ("EM_VISITA", "Em visita"),
        ("FINALIZADO", "Visita finalizada"),
    ]
    
    status = models.CharField( # Campo para o status do visitante
        verbose_name="Status do visitante",
        max_length=10,
        choices=STATUS_VISITANTE,
        default="AGUARDANDO",
    )
    
    nome_completo = models.CharField(verbose_name="Nome completo", max_length=194)
    
    cpf = models.CharField(verbose_name="CPF", max_length=11, unique=True)

    data_nascimento = models.DateField(verbose_name="Data de nascimento", auto_now=False, auto_now_add=False)
    
    numero_casa = models.PositiveSmallIntegerField(verbose_name="Número da casa")
    
    placa_veiculo = models.CharField(verbose_name="Placa do veículo", max_length=7, blank=True, null=True)
    
    horario_chegada = models.DateTimeField(verbose_name="Horário de chegada na portaria", auto_now_add=True)
    
    horario_saida = models.DateTimeField(verbose_name="Horário de saída da portaria", auto_now=False, blank=True, null=True)
    
    horario_autorizacao= models.DateTimeField(verbose_name="Horário de autorização de entrada", auto_now=False, blank=True, null=True)
    
    morador_responsavel = models.CharField(verbose_name="Morador responsável pela autorização", max_length=194, blank=True)

    registrado_por = models.ForeignKey(
        "porteiros.Porteiro",
        verbose_name="Porteiro que registrou a entrada",
        on_delete=models.PROTECT,
    ) # Chave estrangeira para o modelo Porteiro
    
    def get_horario_saida(self): # Método para obter o horário de saída formatado
        if self.horario_saida:
            return self.horario_saida.strftime("%d/%m/%Y %H:%M:%S")
        return "Ainda não saiu"
    
    def get_horario_autorizacao(self): # Método para obter o horário de autorização formatado
        if self.horario_autorizacao:
            return self.horario_autorizacao.strftime("%d/%m/%Y %H:%M:%S")
        return "Ainda não autorizado"
    
    def get_morador_responsavel(self): # Método para obter o morador responsável ou mensagem padrão
        if self.morador_responsavel:
            return self.morador_responsavel
        return "Ainda não autorizado"
    
    def get_placa_veiculo(self): # Propriedade para obter a placa do veículo ou mensagem padrão
        if self.placa_veiculo:
            return self.placa_veiculo
        return "Veículo não informado"
    
    def get_cpf(self):
        if self.cpf:
            cpf = str(self.cpf)
            cpf_parte_um = cpf[0:3]
            cpf_parte_dois = cpf[3:6]
            cpf_parte_tres = cpf[6:9]
            cpf_parte_quatro = cpf[9:10]
            cpf_formatado = f"{cpf_parte_um}.{cpf_parte_dois}.{cpf_parte_tres}-{cpf_parte_quatro}"
            return cpf_formatado

    class Meta: # Metadados do modelo
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        db_table = "visitante"
        
    def __str__(self): # Representação em string do modelo
        return self.nome_completo