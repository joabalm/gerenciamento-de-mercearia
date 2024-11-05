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
                print(f'Produto em estoque:{i.produto.nome, i.produto.preco, i.produto.categoria, i.quantidade }')

x = ControllerEstoque()

x.alterarProduto('bife','file', '20', 'carnes', 20)



