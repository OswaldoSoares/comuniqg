# `CadastraPessoa`

Arquivo: `clientes/forms.py`

Formulário do modal de cliente ou fornecedor. Grava na tabela `pessoa` no mesmo formato do app Delphi, que usa o mesmo banco.

## Fluxo de Execução

1. `tipo` (jurídica ou física) é limpo primeiro (`field_order`).
2. Cada `clean_<campo>` normaliza o valor no formato do Delphi: maiúsculas, máscaras e máscara zerada quando vazio.
3. Os documentos do outro tipo são gravados como máscara zerada.
4. `save` grava `Ativo = 'S'` só no cadastro novo.

## Parâmetros

- `data` (`QueryDict`): POST do modal.
- `instance` (`Pessoa` ou `None`): Pessoa em alteração.

## Retorno

- Form do Django; `save()` retorna a `Pessoa` gravada.

## Dependências

- `Pessoa` (`databaseold`, `managed=False`).
- [`preenchido`](preenchido.md), [`tipo_da_pessoa`](tipo_da_pessoa.md), [`so_digitos`](so_digitos.md), [`cnpj_valido`](cnpj_valido.md), [`cpf_valido`](cpf_valido.md), [`formata_cnpj`](formata_cnpj.md), [`formata_cpf`](formata_cpf.md).

## Métodos

| Método | O que faz |
|---|---|
| `__init__` | Deixa opcionais os campos de `CAMPOS_OPCIONAIS`, põe `form-control` e `autocomplete="off"`, mostra máscaras zeradas como vazio. Cadastro novo: cidade `SÃO PAULO`, UF `SP` e tipo jurídica; alteração: tipo por `tipo_da_pessoa`. |
| `_texto(nome, maiusculas=True)` | Junta espaços, recusa caracteres fora do latin1 (o banco é latin1) e põe em maiúsculas (ou minúsculas, no site). |
| `_fora_do_tipo(campo)` | Verdadeiro para documento do outro tipo (ex.: CPF numa jurídica). Depende de `tipo` ser limpo antes (`field_order`). |
| `_documento_repetido(campo, valor)` | Verdadeiro se outra pessoa já tiver o documento. |
| `clean_apelido` | Maiúsculas, sem repetir (sem diferenciar maiúsculas). |
| `clean_nome`, `clean_endereco`, `clean_bairro`, `clean_cidade` | `_texto`. |
| `clean_cnpj`, `clean_cpf` | Fora do tipo ou vazio: máscara zerada. Confere os dígitos, formata e recusa repetido. |
| `clean_ie` | Fora do tipo ou vazio: máscara zerada. Com 12 dígitos, formata `000.000.000.000`; texto (ex.: `ISENTO`) fica como digitado. |
| `clean_rg` | Fora do tipo ou vazio: máscara zerada; senão, como digitado. |
| `clean_cep` | Vazio: máscara zerada; exige 8 dígitos e formata `00000-000`. |
| `clean_site` | `_texto` em minúsculas. |
| `clean_obs` | Vazio grava `NULL` (como o Delphi); senão, maiúsculas. |
| `save` | Cadastro novo grava `Ativo = 'S'`; a alteração não mexe em `Ativo`. |

## Código da Função

```{py3 linenums="1"}
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
```

## Exemplo de Uso

```{py3 linenums="1"}
form = CadastraPessoa({"tipo": "J", "funcao": "CLIENTE",
                       "apelido": "acme", "nome": "acme ltda"})
if form.is_valid():
    pessoa = form.save()  # APELIDO "ACME"
```
