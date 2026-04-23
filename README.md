# 🏦 Sistema Bancário Orientado a Objetos

Este projeto implementa um sistema bancário completo em Python seguindo os princípios de Programação Orientada a Objetos (POO), com operações de depósito, saque, extrato, gerenciamento de clientes e contas correntes.

## 🎯 Diagrama de Classes

```uml
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Historico    │       │     Conta       │       │   ContaCorrente │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ - transacoes    │       │ - saldo         │       │ - limite        │
├─────────────────┤       │ - numero        │       │ - limite_saques │
│ + adicionar_    │       │ - agencia       │       └─────────────────┤
│   transacao()   │       │ - cliente       │               ▲         │
└─────────────────┘       │ - historico     │               │         │
           ▲              ├─────────────────┤       ┌───────┴───────┐ │
           │              │ + sacar()       │       │  ContaCorrente│ │
           │              │ + depositar()   │       └───────────────┘ │
           │              │ + mostrar_      │                 △       │
           │              │   extrato()     │                 │       │
┌─────────────────┐       └─────────────────┘         Herança        │
│   Transacao     │                 △                               │
├─────────────────┤                 │                               │
│ + valor         │         Composição                             │
│ + registrar()   │                 │                               │
└─────────────────┘                 │                               │
           △                        │                               │
           │                        │                               │
┌─────────────────────┐    ┌─────────────────┐        ┌─────────────────┐
│      Deposito       │    │    Cliente       │        │  PessoaFisica   │
├─────────────────────┤    ├─────────────────┤        ├─────────────────┤
│ - valor            │    │ - endereco       │        │ - cpf           │
├─────────────────────┤    │ - contas         │        │ - nome          │
│ + registrar()      │    ├─────────────────┤        │ - data_nascimento│
└─────────────────────┘    │ + realizar_     │        └─────────────────┘
           △               │   transacao()   │                 △
           │               │ + adicionar_    │                 │
┌─────────────────────┐    │   conta()       │        Herança  │
│       Saque         │    └─────────────────┘                 │
├─────────────────────┤                 △                      │
│ - valor            │                 │                      │
├─────────────────────┤         Associação                    │
│ + registrar()      │                 │                      │
└─────────────────────┘        ┌─────────────────┐            │
                                │     Banco       │            │
                                ├─────────────────┤            │
                                │ - clientes      │────────────┘
                                │ - contas        │
                                ├─────────────────┤
                                │ + adicionar_    │
                                │   cliente()     │
                                │ + adicionar_    │
                                │   conta()       │
                                │ + buscar_       │
                                │   cliente()     │
                                │ + buscar_       │
                                │   conta()       │
                                └─────────────────┘
```

## ✨ Funcionalidades Implementadas

### 🏛️ Arquitetura POO Completa
- **Classes abstratas** e **interfaces** bem definidas
- **Herança** para especialização de classes
- **Composição** para relacionamento entre objetos
- **Encapsulamento** com propriedades e métodos privados

### 💰 Operações Bancárias
- **✅ Depósito**: Valores positivos com registro no histórico
- **✅ Saque**: Limite de 3 saques diários (até R$ 500,00 cada)
- **✅ Extrato**: Histórico completo com timestamps e saldo

### 👥 Gestão de Clientes
- **Cadastro de clientes** com validação de CPF único
- **Pessoa Física**: Nome, CPF, data nascimento e endereço
- **Associação** automática entre clientes e contas

### 🏦 Gestão de Contas
- **Conta Corrente**: Número sequencial e agência fixa "0001"
- **Limites configuráveis**: Valor por saque e quantidade diária
- **Histórico de transações**: Registro completo com data/hora

## 🛠️ Tecnologias e Padrões

- **Python 3.x** com POO avançada
- **ABC (Abstract Base Classes)**: Para interfaces
- **Decoradores @property**: Para encapsulamento
- **Expressões regulares**: Validação de dados
- **Módulo datetime**: Registro temporal preciso
- **Design Patterns**: Factory Method, Strategy

## 🚀 Como Executar

1. **Clone o repositório**:
```bash
git clone https://github.com/renoalencar/dio-logbook.git
```

2. **Navegue até o diretório**:
```bash
cd dio-logbook/desafios/python/00-fundamentos/sistema-bancario-py-v03
```

3. **Execute o sistema**:
```bash
python sistema-bancario-py-v03.py
```

## 📋 Menu de Operações

```
=============== SISTEMA BANCÁRIO ================
[d]  Depositar     [s]  Sacar         [e]  Extrato
[nc] Nova Conta    [lc] Listar Contas [nu] Novo Cliente
[q]  Sair
=================================================
```

## 💻 Exemplos de Uso

### Cadastro de Cliente:
```
=== CADASTRO DE CLIENTE ===
Informe o CPF (apenas números): 12345678900
Informe o nome completo: Maria Silva
Informe a data de nascimento (dd/mm/aaaa): 15/05/1985
Informe o endereço: Rua das Flores, 123 - Centro - São Paulo/SP

✅ Cliente Maria Silva cadastrado com sucesso!
```

### Operação de Depósito:
```
Informe o número da conta: 1
Informe o valor do depósito: R$ 1000.00
✅ Depósito de R$ 1000.00 realizado com sucesso!
```

### Extrato Bancário:
```
================== EXTRATO ==================
[15/05/2023 14:30:25] Deposito   R$  1000.00
[15/05/2023 15:45:12] Saque      R$   200.00
-------------------------------------------
Saldo: R$ 800.00
===========================================
```

## 🏗️ Estrutura de Classes

### Classe `Conta` (Base)
```python
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
```

### Classe `ContaCorrente` (Especializada)
```python
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
```

### Interface `Transacao`
```python
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
```

### Classe `Banco` (Gerenciador Central)
```python
class Banco:
    def __init__(self):
        self._clientes = []
        self._contas = []
```

## 🔧 Principais Métodos

### Operações Bancárias
```python
def sacar(self, valor):  # Na classe Conta
def depositar(self, valor):  # Na classe Conta
def mostrar_extrato(self):  # Exibe histórico completo
```

### Gestão de Transações
```python
def realizar_transacao(self, conta, transacao):  # No Cliente
def registrar(self, conta):  # Nas classes Saque/Deposito
```

### Buscas e Validações
```python
def buscar_cliente(self, cpf):  # No Banco
def buscar_conta(self, numero):  # No Banco
```

## ⚙️ Regras de Negócio

- ❌ **CPF duplicado**: Impede cadastro de clientes com mesmo CPF
- ❌ **Saldo insuficiente**: Bloqueia saques acima do saldo
- ❌ **Limite de saque**: R$ 500,00 por operação
- ❌ **Quantidade de saques**: Máximo 3 por dia
- ❌ **Valores inválidos**: Rejeita valores negativos ou zero
- ✅ **Números de conta**: Sequenciais e únicos
- ✅ **Agência**: Fixa "0001" para todas as contas

## 👨‍💻 Autor

Desenvolvido como parte do desafio de programação da Digital Innovation One.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](/LICENSE) para mais detalhes.

---

**💡 Observação**: Este sistema foi desenvolvido como terceira versão (v3). A primeira e segunda versão podem ser acessada em [sistema-bancario-py-v01.py](/desafios/python/00-fundamentos/sistema-bancario-py-v01/) e [sistema-bancario-py-v02.py](/desafios/python/00-fundamentos/sistema-bancario-py-v02/).