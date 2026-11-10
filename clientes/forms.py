import re

from django import forms

from databaseold.models import Pessoa

# Valores que o app Delphi grava quando o campo não se aplica.
# Ao gravar, campo vazio vira a máscara zerada; ao editar, a máscara
# zerada aparece como campo vazio.
MASCARA_ZERADA = {
    "cnpj": "00.000.000/0000-00",
    "cpf": "000.000.000-00",
    "ie": "000.000.000.000",
    "rg": "00.000.000-0",
    "cep": "00000-000",
}

FUNCOES = [("CLIENTE", "CLIENTE"), ("FORNECEDOR", "FORNECEDOR")]

# A tabela pessoa não tem coluna de tipo: ele vem dos documentos
# preenchidos e só decide quais campos o formulário mostra e grava.
JURIDICA = "J"
FISICA = "F"
TIPOS = [(JURIDICA, "JURÍDICA"), (FISICA, "FÍSICA")]
DOCUMENTOS = {JURIDICA: ["cnpj", "ie"], FISICA: ["cpf", "rg"]}

UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO",
]

CAMPOS_OPCIONAIS = [
    "cnpj", "ie", "cpf", "rg", "endereco", "bairro", "cidade", "estado",
    "cep", "site", "obs",
]


def preenchido(valor):
    """Valor gravado pelo usuário; a máscara zerada do Delphi vira ''."""
    valor = (valor or "").strip()
    return valor if valor.strip(" .-/()0") else ""


def tipo_da_pessoa(pessoa):
    """Jurídica ou física pelos documentos; sem nenhum, pela função
    (clientes costumam ser empresas e fornecedores, pessoas)."""
    if any(preenchido(getattr(pessoa, c)) for c in DOCUMENTOS[JURIDICA]):
        return JURIDICA
    if any(preenchido(getattr(pessoa, c)) for c in DOCUMENTOS[FISICA]):
        return FISICA
    return FISICA if pessoa.funcao == "FORNECEDOR" else JURIDICA


def so_digitos(valor):
    return re.sub(r"\D", "", valor or "")


def _digito_verificador(numeros, pesos):
    resto = sum(n * p for n, p in zip(numeros, pesos)) % 11
    return 0 if resto < 2 else 11 - resto


def cnpj_valido(digitos):
    if len(digitos) != 14 or len(set(digitos)) == 1:
        return False
    numeros = [int(d) for d in digitos]
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    primeiro = _digito_verificador(numeros[:12], pesos)
    segundo = _digito_verificador(numeros[:13], [6, *pesos])
    return numeros[12] == primeiro and numeros[13] == segundo


def cpf_valido(digitos):
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    numeros = [int(d) for d in digitos]
    primeiro = _digito_verificador(numeros[:9], range(10, 1, -1))
    segundo = _digito_verificador(numeros[:10], range(11, 1, -1))
    return numeros[9] == primeiro and numeros[10] == segundo


def formata_cnpj(d):
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"


def formata_cpf(d):
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


class CadastraPessoa(forms.ModelForm):
    """Cliente ou fornecedor na tabela pessoa, no formato do app Delphi."""

    tipo = forms.ChoiceField(label="PESSOA", choices=TIPOS)
    funcao = forms.ChoiceField(label="FUNÇÃO", choices=FUNCOES)
    estado = forms.ChoiceField(
        label="UF", choices=[("", "")] + [(uf, uf) for uf in UFS],
        required=False,
    )

    field_order = ["tipo"]  # noqa: RUF012 (limpo antes dos documentos)

    class Meta:
        model = Pessoa
        fields = [  # noqa: RUF012 (Meta do Django)
            "funcao", "apelido", "nome", "cnpj", "ie", "cpf", "rg",
            "endereco", "bairro", "cidade", "estado", "cep", "site", "obs",
        ]
        labels = {  # noqa: RUF012 (Meta do Django)
            "apelido": "APELIDO",
            "nome": "NOME",
            "cnpj": "CNPJ",
            "ie": "INSCRIÇÃO ESTADUAL",
            "cpf": "CPF",
            "rg": "RG",
            "endereco": "ENDEREÇO",
            "bairro": "BAIRRO",
            "cidade": "CIDADE",
            "cep": "CEP",
            "site": "SITE",
            "obs": "OBSERVAÇÃO",
        }
        widgets = {  # noqa: RUF012 (Meta do Django)
            "cnpj": forms.TextInput(
                attrs={"data-mascara": "00.000.000/0000-00",
                       "inputmode": "numeric"}
            ),
            "cpf": forms.TextInput(
                attrs={"data-mascara": "000.000.000-00",
                       "inputmode": "numeric"}
            ),
            "cep": forms.TextInput(
                attrs={"data-mascara": "00000-000", "inputmode": "numeric"}
            ),
            "site": forms.TextInput(attrs={"inputmode": "url"}),
            "obs": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nome in CAMPOS_OPCIONAIS:
            self.fields[nome].required = False
        for nome, campo in self.fields.items():
            campo.widget.attrs.setdefault("class", "form-control")
            campo.widget.attrs.setdefault("autocomplete", "off")
            if nome in MASCARA_ZERADA and self.initial.get(nome) == (
                MASCARA_ZERADA[nome]
            ):
                self.initial[nome] = ""
        if self.instance.pk is None:
            self.initial.setdefault("cidade", "SÃO PAULO")
            self.initial.setdefault("estado", "SP")
            self.initial.setdefault("tipo", JURIDICA)
        else:
            self.initial.setdefault("tipo", tipo_da_pessoa(self.instance))

    # --- regras gerais -----------------------------------------------------

    def _texto(self, nome, maiusculas=True):
        """Remove espaços extras, confere o latin1 do banco e põe em
        maiúsculas."""
        valor = " ".join((self.cleaned_data.get(nome) or "").split())
        invalidos = sorted({c for c in valor if ord(c) > 255})
        if invalidos:
            raise forms.ValidationError(
                "Caractere não permitido: " + " ".join(invalidos)
            )
        return valor.upper() if maiusculas else valor.lower()

    def _fora_do_tipo(self, campo):
        """Documento do outro tipo: não aparece na tela e é gravado
        como a máscara zerada."""
        tipo = self.cleaned_data.get("tipo")
        return bool(tipo) and campo not in DOCUMENTOS[tipo]

    def _documento_repetido(self, campo, valor):
        return (
            Pessoa.objects.filter(**{campo: valor})
            .exclude(pk=self.instance.pk)
            .exists()
        )

    # --- campos --------------------------------------------------------------

    def clean_apelido(self):
        apelido = self._texto("apelido")
        repetido = Pessoa.objects.filter(apelido__iexact=apelido).exclude(
            pk=self.instance.pk
        )
        if repetido.exists():
            raise forms.ValidationError(
                "Já existe um cadastro com este apelido."
            )
        return apelido

    def clean_nome(self):
        return self._texto("nome")

    def clean_cnpj(self):
        if self._fora_do_tipo("cnpj"):
            return MASCARA_ZERADA["cnpj"]
        digitos = so_digitos(self.cleaned_data.get("cnpj"))
        if not digitos:
            return MASCARA_ZERADA["cnpj"]
        if not cnpj_valido(digitos):
            raise forms.ValidationError("CNPJ inválido.")
        cnpj = formata_cnpj(digitos)
        if self._documento_repetido("cnpj", cnpj):
            raise forms.ValidationError("Já existe um cadastro com este CNPJ.")
        return cnpj

    def clean_cpf(self):
        if self._fora_do_tipo("cpf"):
            return MASCARA_ZERADA["cpf"]
        digitos = so_digitos(self.cleaned_data.get("cpf"))
        if not digitos:
            return MASCARA_ZERADA["cpf"]
        if not cpf_valido(digitos):
            raise forms.ValidationError("CPF inválido.")
        cpf = formata_cpf(digitos)
        if self._documento_repetido("cpf", cpf):
            raise forms.ValidationError("Já existe um cadastro com este CPF.")
        return cpf

    def clean_ie(self):
        if self._fora_do_tipo("ie"):
            return MASCARA_ZERADA["ie"]
        ie = self._texto("ie")
        digitos = so_digitos(ie)
        if not ie or (digitos == ie and set(digitos) == {"0"}):
            return MASCARA_ZERADA["ie"]
        if digitos == ie and len(digitos) == 12:
            return f"{ie[:3]}.{ie[3:6]}.{ie[6:9]}.{ie[9:]}"
        return ie

    def clean_rg(self):
        if self._fora_do_tipo("rg"):
            return MASCARA_ZERADA["rg"]
        rg = self._texto("rg")
        return rg or MASCARA_ZERADA["rg"]

    def clean_cep(self):
        digitos = so_digitos(self.cleaned_data.get("cep"))
        if not digitos:
            return MASCARA_ZERADA["cep"]
        if len(digitos) != 8:
            raise forms.ValidationError("CEP deve ter 8 dígitos.")
        return f"{digitos[:5]}-{digitos[5:]}"

    def clean_endereco(self):
        return self._texto("endereco")

    def clean_bairro(self):
        return self._texto("bairro")

    def clean_cidade(self):
        return self._texto("cidade")

    def clean_site(self):
        return self._texto("site", maiusculas=False)

    def clean_obs(self):
        # O Delphi grava NULL quando não há observação
        obs = (self.cleaned_data.get("obs") or "").strip()
        invalidos = sorted({c for c in obs if ord(c) > 255})
        if invalidos:
            raise forms.ValidationError(
                "Caractere não permitido: " + " ".join(invalidos)
            )
        return obs.upper() or None

    def save(self, commit=True):
        pessoa = super().save(commit=False)
        if pessoa.pk is None:
            pessoa.ativo = "S"
        if commit:
            pessoa.save()
        return pessoa
