# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Contato(models.Model):
    idcontato = models.AutoField(db_column='IDContato', primary_key=True)  # Field name made lowercase.
    idpessoa = models.PositiveIntegerField(db_column='IDPessoa')  # Field name made lowercase.
    contato = models.CharField(db_column='Contato', max_length=15)  # Field name made lowercase.
    telefone1 = models.CharField(db_column='Telefone1', max_length=14)  # Field name made lowercase.
    telefone2 = models.CharField(db_column='Telefone2', max_length=14)  # Field name made lowercase.
    celular1 = models.CharField(db_column='Celular1', max_length=14)  # Field name made lowercase.
    celular2 = models.CharField(db_column='Celular2', max_length=14)  # Field name made lowercase.
    radio = models.CharField(db_column='Radio', max_length=10)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=40)  # Field name made lowercase.
    nascimento = models.DateField(db_column='Nascimento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contato'
        unique_together = (('idcontato', 'idpessoa'),)


class Formapgto(models.Model):
    idformapgto = models.AutoField(db_column='IDFormaPgto', primary_key=True)  # Field name made lowercase.
    fatura = models.PositiveIntegerField(db_column='Fatura')  # Field name made lowercase.
    diapago = models.DateField(db_column='DiaPago')  # Field name made lowercase.
    dinheiro = models.DecimalField(db_column='Dinheiro', max_digits=10, decimal_places=2)  # Field name made lowercase.
    debito = models.DecimalField(db_column='Debito', max_digits=10, decimal_places=2)  # Field name made lowercase.
    credito = models.DecimalField(db_column='Credito', max_digits=10, decimal_places=2)  # Field name made lowercase.
    parcelas = models.PositiveIntegerField(db_column='Parcelas')  # Field name made lowercase.
    deposito = models.DecimalField(db_column='Deposito', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'formapgto'


class Foto(models.Model):
    foto = models.TextField(db_column='Foto')  # Field name made lowercase.
    idcontato = models.PositiveIntegerField(db_column='IDContato')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'foto'


class Pagar(models.Model):
    idpagar = models.PositiveIntegerField(db_column='IDPagar', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=50)  # Field name made lowercase.
    categoria = models.CharField(db_column='Categoria', max_length=30)  # Field name made lowercase.
    diaservico = models.DateField(db_column='DiaServico')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=10, decimal_places=2)  # Field name made lowercase.
    vencimento = models.DateField(db_column='Vencimento')  # Field name made lowercase.
    valorpago = models.DecimalField(db_column='ValorPago', max_digits=10, decimal_places=2)  # Field name made lowercase.
    diapago = models.DateField(db_column='DiaPago')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=15)  # Field name made lowercase.
    idpessoa = models.PositiveIntegerField(db_column='IDPessoa')  # Field name made lowercase.
    obs = models.TextField(db_column='Obs', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pagar'


class Pessoa(models.Model):
    idpessoa = models.AutoField(db_column='IDPessoa', primary_key=True)  # Field name made lowercase.
    apelido = models.CharField(db_column='Apelido', max_length=25)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=60)  # Field name made lowercase.
    endereco = models.CharField(db_column='Endereco', max_length=60)  # Field name made lowercase.
    bairro = models.CharField(db_column='Bairro', max_length=25)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=25)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=2)  # Field name made lowercase.
    cep = models.CharField(db_column='CEP', max_length=9)  # Field name made lowercase.
    site = models.CharField(db_column='Site', max_length=30)  # Field name made lowercase.
    cnpj = models.CharField(db_column='CNPJ', max_length=18)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=14)  # Field name made lowercase.
    ie = models.CharField(db_column='IE', max_length=15)  # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=12)  # Field name made lowercase.
    ativo = models.CharField(db_column='Ativo', max_length=1)  # Field name made lowercase.
    funcao = models.CharField(db_column='Funcao', max_length=15)  # Field name made lowercase.
    obs = models.TextField(db_column='OBS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pessoa'


class Produto(models.Model):
    idproduto = models.AutoField(db_column='IDProduto', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=35)  # Field name made lowercase.
    obs = models.TextField(db_column='Obs', blank=True, null=True)  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=10, decimal_places=2)  # Field name made lowercase.
    categoria = models.CharField(db_column='Categoria', max_length=35)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'produto'


class Receber(models.Model):
    idfatura = models.PositiveIntegerField(db_column='IDFatura', primary_key=True)  # Field name made lowercase.
    diafatura = models.DateField(db_column='DiaFatura')  # Field name made lowercase.
    valorfatura = models.DecimalField(db_column='ValorFatura', max_digits=12, decimal_places=2)  # Field name made lowercase.
    vencimento = models.DateField(db_column='Vencimento')  # Field name made lowercase.
    valorpago = models.DecimalField(db_column='ValorPago', max_digits=12, decimal_places=2)  # Field name made lowercase.
    diapago = models.DateField(db_column='DiaPago')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=9)  # Field name made lowercase.
    tipofatura = models.CharField(db_column='TipoFatura', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receber'


class Servico(models.Model):
    idservico = models.PositiveIntegerField(db_column='IDServico', primary_key=True)  # Field name made lowercase.
    idcadastro = models.PositiveIntegerField(db_column='IDCadastro')  # Field name made lowercase.
    diaservico = models.DateField(db_column='DiaServico')  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=2)  # Field name made lowercase.
    idfatura = models.PositiveIntegerField(db_column='IDFatura')  # Field name made lowercase.
    obs = models.TextField(db_column='Obs', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=8)  # Field name made lowercase.
    obra = models.CharField(db_column='Obra', max_length=25)  # Field name made lowercase.
    diaentrega = models.DateField(db_column='DiaEntrega')  # Field name made lowercase.
    solicitante = models.CharField(db_column='Solicitante', max_length=25)  # Field name made lowercase.
    seleciona = models.CharField(db_column='Seleciona', max_length=1)  # Field name made lowercase.
    checkin = models.PositiveIntegerField(db_column='Checkin')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'servico'


class Servicoitem(models.Model):
    idservicoitem = models.AutoField(db_column='IDServicoItem', primary_key=True)  # Field name made lowercase.
    idservico = models.PositiveIntegerField(db_column='IDServico')  # Field name made lowercase.
    idproduto = models.PositiveIntegerField(db_column='IDProduto')  # Field name made lowercase.
    originais = models.PositiveIntegerField(db_column='Originais')  # Field name made lowercase.
    copias = models.PositiveIntegerField(db_column='Copias')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=10, decimal_places=2)  # Field name made lowercase.
    tamanho = models.DecimalField(db_column='Tamanho', max_digits=6, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'servicoitem'
        unique_together = (('idservicoitem', 'idservico'),)


class Tabela(models.Model):
    idtabela = models.AutoField(db_column='IDTabela', primary_key=True)  # Field name made lowercase.
    idcadastro = models.PositiveIntegerField(db_column='IDCadastro')  # Field name made lowercase.
    idproduto = models.PositiveIntegerField(db_column='IDProduto')  # Field name made lowercase.
    valor = models.DecimalField(db_column='Valor', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tabela'
