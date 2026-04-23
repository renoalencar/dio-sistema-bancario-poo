import re
from abc import ABC, abstractmethod
from datetime import datetime

# ==================== CLASSES DO DOMÍNIO ====================

class Cliente:
    """
    Classe base para clientes do banco. Gerencia as contas associadas.
    """
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        """Inicia o processo de registro de uma transação em uma conta."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista do cliente."""
        self._contas.append(conta)


class PessoaFisica(Cliente):
    """
    Representa um cliente do tipo Pessoa Física, com nome, data de nascimento e CPF.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


class Conta:
    """
    Classe base para contas bancárias. Controla saldo, histórico e operações básicas.
    """
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de fábrica para criar uma nova instância de conta."""
        return cls(numero, cliente)

    def sacar(self, valor):
        """Método interno para efetivar a retirada de valor do saldo."""
        if valor <= 0:
            print("❌ Operação falhou! O valor informado é inválido.")
            return False
        
        if valor > self._saldo:
            print("❌ Operação falhou! Saldo insuficiente.")
            return False

        self._saldo -= valor
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        """Método interno para efetivar a adição de valor ao saldo."""
        if valor > 0:
            self._saldo += valor
            print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True
        
        print("❌ Operação falhou! O valor informado é inválido.")
        return False

    def mostrar_extrato(self):
        """Exibe o histórico de transações e o saldo final da conta."""
        print("\n================== EXTRATO ==================")
        transacoes = self.historico.transacoes

        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for item in transacoes:
                transacao = item["transacao"]
                tipo_transacao = transacao.__class__.__name__
                log = f"[{item['timestamp']}] {tipo_transacao:<9} R$ {transacao.valor:8.2f}"
                print(log)

        print("-------------------------------------------")
        print(f"Saldo: R$ {self.saldo:.2f}")
        print("===========================================\n")
    
    def realizar_deposito(self, valor):
        """Método de alto nível para orquestrar uma operação de depósito."""
        deposito = Deposito(valor)
        self.cliente.realizar_transacao(self, deposito)

    def realizar_saque(self, valor):
        """Método de alto nível para orquestrar uma operação de saque."""
        saque = Saque(valor)
        self.cliente.realizar_transacao(self, saque)


class ContaCorrente(Conta):
    """
    Especialização da Conta para o tipo Corrente, com limites de saque.
    """
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para incluir validações de limite e número de saques."""
        hoje = datetime.now().date()
        saques_de_hoje = []

        # Itera sobre os itens do histórico
        for item in self.historico.transacoes:
            transacao = item["transacao"]
            timestamp_str = item["timestamp"]
            
            # Converte a string do timestamp para um objeto date
            data_transacao = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S').date()

            # Adiciona à lista apenas se for um Saque e se a data for de hoje
            if isinstance(transacao, Saque) and data_transacao == hoje:
                saques_de_hoje.append(transacao)
        
        saques_realizados = len(saques_de_hoje)

        if valor > self._limite:
            print(f"❌ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
            return False
        
        if saques_realizados >= self._limite_saques:
            print(f"❌ Operação falhou! Você atingiu o limite de {self._limite_saques} saques diários.")
            return False

        return super().sacar(valor)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"


class Historico:
    """Armazena a lista de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            "transacao": transacao
        })


class Transacao(ABC):
    """Interface para as transações, garantindo que todas tenham valor e método de registro."""
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """Representa a transação de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Tenta efetivar o saque na conta e, se bem-sucedido, o adiciona ao histórico."""
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Representa a transação de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Tenta efetivar o depósito na conta e, se bem-sucedido, o adiciona ao histórico."""
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Banco:
    """
    Centraliza o gerenciamento de clientes e contas, atuando como o estado principal do sistema.
    """
    def __init__(self):
        self._clientes = []
        self._contas = []

    @property
    def clientes(self):
        return self._clientes

    @property
    def contas(self):
        return self._contas

    def adicionar_cliente(self, cliente):
        self._clientes.append(cliente)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def buscar_cliente(self, cpf):
        """Busca um cliente na lista a partir do CPF."""
        clientes_filtrados = [cliente for cliente in self._clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def buscar_conta(self, numero):
        """Busca uma conta na lista a partir do número."""
        contas_filtradas = [conta for conta in self._contas if conta.numero == numero]
        return contas_filtradas[0] if contas_filtradas else None


# ==================== FUNÇÕES DE INTERFACE (MENU) ====================

def menu_criar_cliente(banco):
    """Função para a interface de criação de cliente."""
    print("\n=== CADASTRO DE CLIENTE ===")
    cpf = input("Informe o CPF (apenas números): ").strip()
    
    if not re.match(r"^\d{11}$", cpf):
        print("❌ CPF inválido! Por favor, digite 11 números.")
        return
    if banco.buscar_cliente(cpf):
        print("❌ Já existe um cliente com este CPF!")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    endereco_str = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco_str)
    banco.adicionar_cliente(novo_cliente)
    print(f"\n✅ Cliente {nome} cadastrado com sucesso!")


def menu_criar_conta(banco):
    """Função para a interface de criação de conta."""
    print("\n=== ABERTURA DE CONTA CORRENTE ===")
    if not banco.clientes:
        print("❌ Nenhum cliente cadastrado! Cadastre um cliente primeiro.")
        return

    cpf = input("Informe o CPF do titular: ").strip()
    cliente = banco.buscar_cliente(cpf)

    if not cliente:
        print("❌ Cliente não encontrado!")
        return

    numero_conta = len(banco.contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    banco.adicionar_conta(conta)
    cliente.adicionar_conta(conta)
    print(f"✅ Conta {conta.numero} criada com sucesso para {cliente.nome}!")


def menu_listar_contas(banco):
    """Função para a interface de listagem de contas."""
    if not banco.contas:
        print("Nenhuma conta cadastrada.\n")
        return
    
    print("\n=== CONTAS CADASTRADAS ===")
    for conta in banco.contas:
        print(f"Agência: {conta.agencia} | Conta: {conta.numero} | "
              f"Titular: {conta.cliente.nome} | Saldo: R$ {conta.saldo:.2f}")
    print()


def exibir_menu_principal():
    """Exibe o menu de opções e retorna a escolha do usuário."""
    return input("""
=============== SISTEMA BANCÁRIO ================
[d]  Depositar     [s]  Sacar         [e]  Extrato
[nc] Nova Conta    [lc] Listar Contas [nu] Novo Cliente
[q]  Sair
=================================================
Escolha uma opção: """).lower().strip()


# ==================== SISTEMA PRINCIPAL ====================

def main():
    """Função principal que inicia o sistema e gerencia o loop de menu."""
    banco = Banco()
    print("🏛️  Bem-vindo ao DIO Bank!")
    
    while True:
        opcao = exibir_menu_principal()

        if opcao in ["d", "s", "e"]:
            if not banco.contas:
                print("❌ Nenhuma conta cadastrada para realizar a operação.")
                continue
            
            try:
                num_conta = int(input("Informe o número da conta: "))
                conta = banco.buscar_conta(num_conta)
                
                if not conta:
                    print("❌ Conta não encontrada.")
                    continue

                if opcao == "d":
                    valor = float(input("Informe o valor do depósito: R$ "))
                    conta.realizar_deposito(valor)
                
                elif opcao == "s":
                    valor = float(input("Informe o valor do saque: R$ "))
                    conta.realizar_saque(valor)
                
                elif opcao == "e":
                    conta.mostrar_extrato()

            except ValueError:
                print("❌ Valor inválido! Por favor, digite um número.")

        elif opcao == "nu":
            menu_criar_cliente(banco)
        elif opcao == "nc":
            menu_criar_conta(banco)
        elif opcao == "lc":
            menu_listar_contas(banco)
        elif opcao == "q":
            print("👋 Obrigado por usar nosso sistema! Até logo!")
            break
        else:
            print("❌ Operação inválida! Escolha uma opção válida do menu.\n")

# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    main()