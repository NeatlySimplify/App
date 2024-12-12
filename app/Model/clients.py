from datetime import date
from enum import Enum
from pydantic import EmailStr, BaseModel
from types import List


# Enums
class ClientsType(str, Enum):
    PF: str = "Pessoa Física"
    PJ: str = "Pessoa Jurídica"


class RelationshipTag(str, Enum):
    CASADO: str = "Casado(a)"
    SOLTEIRO: str = "Solteiro(a)"
    VIUVO: str = "Viúvo(a)"
    UNIAO: str = "Em União Estável"
    DIVORCIADO: str = "Divorciado(a)"


# Complement to be dumped as json on db
class Endereco(BaseModel):
    rua: str
    numero: str
    complemento: str = ''
    bairro: str
    cep: str
    cidade: str
    estado: str


class Telefone(BaseModel):
    tipo: dict
    numero: str
    contato: str
    details: str
# end


class Client(BaseModel):
    email: EmailStr
    name: str
    sex: str
    relationship: RelationshipTag
    details: str = ''
    category: ClientsType
    birth: date
    city: str
    estate: str
    phone: List[Telefone]
    address: List[Endereco]


class PessoaFisica(BaseModel):
    user: str
    cpf: str
    rg: str
    pis: str
    ctps: str
    serie: str
    nancionalidade: str
    profissao: str
    nome_mae: str


class PessoaJuridica(BaseModel):
    user: str
    cnpj: str
    responsavel: str
    tipo_empresa: str
    atividade_principal: str
    inscricao_municipal: str
    inscricao_estadual: str








