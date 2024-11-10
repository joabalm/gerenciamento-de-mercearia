from models import *
from dao import *
from datetime import datetime

class ControllerCategoria:

    def cadastrarCategoria(self, nova_categoria):
        existe = False
        list_categorias = DaoCategoria.ler()
        for i in list_categorias:
            if i.categoria == nova_categoria:
                existe = True

        if not existe:
            DaoCategoria.salvar(nova_categoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('Essa categoria já existe!')

    def removerCategoria(self, categoriaRemover):
        lista_categoria = DaoCategoria.ler()
        cat = list(filter(lambda lista_categoria: lista_categoria.categoria.upper() == categoriaRemover.upper(), lista_categoria ))

        if len(cat) <= 0:
            print(f'A categoria: {categoriaRemover}, não existe!')
        else:
            for i in range(len(lista_categoria)):
                if lista_categoria[i].categoria.upper() == categoriaRemover.upper():
                    del lista_categoria[i]
                    break
            print(f'Categoria {categoriaRemover} foi removida com sucesso!')

            with open('categoria.txt', 'w') as arq:
                for i in lista_categoria:
                    print(i)
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

        estoque = DaoEstoque.ler()

        estoque = list(
            map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade) if (
                        x.produto.categoria == categoriaRemover) else (x), estoque))

        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(
                    i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines("\n")

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        lista_categoria = DaoCategoria.ler()

        cat = list(filter(lambda lista_categoria: lista_categoria.categoria == categoriaAlterar, lista_categoria))

        if len(cat) > 0:
            cat1 = list(filter(lambda lista_categoria: lista_categoria.categoria == categoriaAlterada, lista_categoria))
            if len(cat1) == 0:
                lista_categoria = list(map( lambda lista_categoria: Categoria(categoriaAlterada)
                                            if(lista_categoria.categoria == categoriaAlterar)
                                            else(lista_categoria), lista_categoria)
                                           )
                estoque = DaoEstoque.ler()

                estoque = list(
                    map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaAlterada), x.quantidade) if (
                            x.produto.categoria == categoriaAlterar) else (x), estoque))
                print('A categoria alterada com sucesso')
            else:
                print('A categoria para qual deseja alterar ja existe')
        else:
            print('A categoria que deseja alterar ja existe')

        with open('categoria.txt', 'w') as arq:
            for i in lista_categoria:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        lista_categorias = DaoCategoria.ler()
        if len(lista_categorias) == 0:
            print('Categoria vazia!')
            return 0
        for i in lista_categorias:
            print(f'Categoria: {i.categoria}')

class ControllerEstoque:

    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        lista_produtos = DaoEstoque.ler()
        lista_categorias = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoria, lista_categorias))
        nome_existe = list(filter(lambda x: x.produto.nome == nome, lista_produtos))


        if len(cat) > 0:
            if len(nome_existe) == 0:
                produto = Produtos(str(nome), str(preco), str(categoria))
                DaoEstoque.salva(produto, quantidade)
                print('Produto cadastrado com sucesso')
            else:
                print('Produto já está cadastrado')
        else:
            print('Categoria inexistente')

    def removerProduto(self, nome):
        lista_produtos = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, lista_produtos))
        if len(est) > 0:
            for i in range(len(lista_produtos)):
                if lista_produtos[i].produto.nome == nome:
                    del lista_produtos[i]
                    break
            print('Produto removido com sucesso!')
        else:
            print('O produto não existe!')

        with open('estoque.txt', 'w') as arq:
            for i in lista_produtos:
                arq.writelines(i.produto.nome + '|' + i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                arq.writelines('\n')


    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        lista_estoque = DaoEstoque.ler()
        cat = DaoCategoria.ler()

        catfilter = list(filter(lambda x: x.categoria == novaCategoria, cat))

        if len(catfilter) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, lista_estoque))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, lista_estoque))
                if len(est) == 0:
                    lista_estoque = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), lista_estoque))
                    print('Produto alterado com sucesso')
                else:
                    print('produto ja cadastrado')
            else:
                print('Produto não existe')

            with open('estoque.txt', 'w') as arq:
                for i in lista_estoque:
                    arq.writelines(
                        i.produto.nome + '|' + i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                    arq.writelines('\n')


        else:
            print('a categoria não existe')

    def mostrarEstoque(self):
        lista_estoque = DaoEstoque.ler()
        if len(lista_estoque) > 0:
            for i in lista_estoque:
                print(
                        f'Produto em estoque - Produto: {i.produto.nome},'
                        f' Preço: R${i.produto.preco},'
                        f' Categoria: {i.produto.categoria},'
                        f' Quantidade: {i.quantidade}'

                      )

class ControllerVenda:

    def cadastrarVenda(self, nome, preco, categoria, vendedor, comprador, quantidadeVendida):
        est = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in est:
            if existe == False:
                if i.produto.nome >= nome:
                    existe = True
                    if int(i.quantidade) >= int(quantidadeVendida):
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valor_compra = int(quantidadeVendida) * int(i.produto.preco)

                        DaoVendas.salvar(vendido)
            temp.append(Estoque(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade))

            arq = open('estoque.txt', 'w')
            arq.write('')

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i.produto.nome + '|' +i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                arq.writelines('\n')

        if existe == False:
            print('O produto não existe')
            return 1
        elif not quantidade:
            print('O produto não tem quantidade')
            return 1
        else:
            print('Venda realizada com sucesso', valor_compra)
            return 3, valor_compra

    def relatorioProdutos(self):
        vendas = DaoVendas.ler()
        produtos = []

        for i in vendas:
            nome = i.itensVendidos.nome
            quantidade = i.quandidadeVendida
            tamanho =list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produtos':nome, 'quantidade': int(x['quantidade']) + int(quantidade)} if(x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': quantidade})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esseds são os produtos mais vendidos')
        a = 1
        for i in ordenado:
            print(f'============Produto [{a}]')
            print(f'Produto: {i['produto']}\n'
                  f'Quantidade: {i['quantidade']}\n')
            a += 1

    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVendas.ler()
        dataInicio1 = datetime.strptime(dataInicio,'%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino,'%d/%m/%Y')

        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y') >= dataInicio1
                                        and datetime.strptime(x.data, '%d/%m/%Y') <= dataTermino1, vendas))


        cont = 1
        total = 0

        for i in vendasSelecionadas:
            print(f'===========Venda [{cont}] ============')
            print(f'Nome: {i.itensVendidos.nome}\n')
            print(f'Categoria: {i.itensVendidos.categoria}\n')
            print(f'Data: {i.data}\n')
            print(f'Quantidade: {i.quandidadeVendida}\n')
            print(f'Cliente: {i.cliente}\n')
            print(f'Vendedor: {i.vendedor}\n')

            total += int(i.itensVendidos.preco) * int(i.quandidadeVendida)
        print(f'total vendido: {total}')

class ControllerFornecedor:
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        listaCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listaTelefone = list(filter(lambda x: x.cnpj == cnpj, x))
        if len(listaCnpj) > 0:
            print("O cnpj já existe")
        elif len(listaTelefone) > 0:
            print('O telefone já existe')
        else:
            if len(cnpj)  == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
            else:
                print("Digite um cnpj ou telefone válido")

    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novoCategoria):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            est = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len(est) == 0:
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novoCategoria) if(x.nome == nomeAlterar) else(x),x))
            else:
                print('Cnpj já existe')
        else:
            print('O fornecedor que deseja alterar nao existe')

        with open('fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('fornecedor alterado com sucesso')

    def removerFornecedor(self, nome):
        x = DaoFornecedor.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del  x[i]
                    break
        else:
            print('O fornecedor que deseja remover não existe')
            return None

        with open('fornecedores.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                arq.writelines('\n')
            print('Fornecedor removido com sucesso')

    def mostrarFornecedores(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) == 0:
            print("Lista de fornecedores vazia")

        for i in fornecedores:
            print("=========Fornecedores==========")
            print(f"Categoria fornecida: {i.categoria}\n"
                  f"Nome: {i.nome}\n"
                  f"Telefone: {i.telefone}\n"
                  f"Cnpj: {i.cnpj}")

class ControllerCliente:
    def cadastrarCliente(self, nome, telefone, cpf, email, endereco):
        x = DaoPessoa.ler()

        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        if len(listaCpf) > 0:
            print('CPF já existente')
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <=11:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente Cadastrado com sucesso')
            else:
                print('digite um cpf ou telefone válido')

    def alterarCliente(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if (
                        x.nome == nomeAlterar) else (x), x))
        else:
            print('O cliente que deseja alterar nao existe')

        with open('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('cliente alterado com sucesso')

    def removerCliente(self, nome):
        x = DaoPessoa.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del  x[i]
                    break
        else:
            print('O cliente que deseja remover não existe')
            return None

        with open('clientes.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Cliente removido com sucesso')

    def mostrarClientes(self):
        clientes = DaoPessoa.ler()

        if len(clientes) == 0:
            print("Lista de clientes vazia")

        for i in clientes:
            print("=========Cliente=========")
            print(f"Nome: {i.nome}\n"
                  f"Telefone: {i.telefone}\n"
                  f"Endereço: {i.endereco}\n"
                  f"Email: {i.email}\n"
                  f"CPF: {i.cpf}")

class ControllerFuncionario:
    def cadastrarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        x = DaoFuncionario.ler()

        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))
        if len(listaCpf) > 0:
            print('CPF já existente')
        elif len(listaClt) > 0:
            print('Já existe um funcionario com essa clt')
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <=11:
                DaoFuncionario.salvar(Funcionario(clt, nome, telefone, cpf, email, endereco))
                print('Funcionario Cadastrado com sucesso')
            else:
                print('digite um cpf ou telefone válido')

    def alterarFuncionario(self, nomeAlterar, novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            x = list(map(lambda x: Funcionario(novoClt,novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if (
                    x.nome == nomeAlterar) else (x), x))
        else:
            print('O funcionario que deseja alterar nao existe')

        with open('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.clt + "|" + i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email
                               + "|" + i.endereco)
                arq.writelines('\n')
            print('funcionario alterado com sucesso')

    def removerFuncionario(self, nome):
        x = DaoFuncionario.ler()

        est = list(filter(lambda x: x.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].nome == nome:
                    del  x[i]
                    break
        else:
            print('O funcionario que deseja remover não existe')
            return None

        with open('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
            print('Funcionarios removido com sucesso')

    def mostrarFuncionarios(self):
        funcionario = DaoFuncionario.ler()

        if len(funcionario) == 0:
            print("Lista de funcionarios vazia")

        for i in funcionario:
            print("========Funcionario==========")
            print(f"Nome: {i.nome}\n"
                  f"Telefone: {i.telefone}\n"
                  f"Email: {i.email}\n"
                  f"Endereço: {i.endereco}\n"
                  f"CPF: {i.cpf}\n"
                  f"CLT: {i.clt}\n")



