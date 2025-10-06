import os
import json
import qrcode
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime

# --- Constantes e Configuração ---
DB_FILE = "produtos.json"
VENDAS_FILE = "vendas.json"
MOVIMENTACOES_FILE = "movimentacoes.json"
QR_FOLDER = "qrcodes"

# --- Funções Auxiliares de Arquivos ---
def carregar_produtos():
    """Carrega os produtos do arquivo JSON."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_produtos(produtos):
    """Salva a lista de produtos no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, indent=2, ensure_ascii=False)
    
def carregar_vendas():
    """Carrega as vendas do arquivo JSON."""
    if not os.path.exists(VENDAS_FILE):
        return []
    try:
        with open(VENDAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_vendas(vendas):
    """Salva a lista de vendas no arquivo JSON."""
    with open(VENDAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(vendas, f, indent=2, ensure_ascii=False)

def carregar_movimentacoes():
    """Carrega as movimentações do arquivo JSON."""
    if not os.path.exists(MOVIMENTACOES_FILE):
        return []
    try:
        with open(MOVIMENTACOES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_movimentacoes(movimentacoes):
    """Salva a lista de movimentações no arquivo JSON."""
    with open(MOVIMENTACOES_FILE, 'w', encoding='utf-8') as f:
        json.dump(movimentacoes, f, indent=2, ensure_ascii=False)

def garantir_pasta_existente(nome_pasta):
    """Garante que uma pasta exista, criando-a se necessário."""
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

def registrar_movimentacao(tipo, codigo_produto, nome_produto, quantidade, observacao):
    """Registra uma movimentação de estoque."""
    movimentacoes = carregar_movimentacoes()
    movimentacao = {
        "id": len(movimentacoes) + 1,
        "tipo": tipo,  # 'entrada' ou 'saida'
        "codigo_produto": codigo_produto,
        "nome_produto": nome_produto,
        "quantidade": quantidade,
        "observacao": observacao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    movimentacoes.append(movimentacao)
    salvar_movimentacoes(movimentacoes)

# --- Funcionalidades do ERP (Entrega 1) ---
def cadastrar_produto():
    """Realiza o cadastro completo de um novo produto e gera seu QR Code."""
    print("\n--- 1. Cadastro de Novo Produto ---")
    produtos = carregar_produtos()
    
    codigo_produto = input("Digite o Código do Produto (único): ")
    if any(p['codigo_produto'] == codigo_produto for p in produtos):
        print("\n[ERRO] Já existe um produto com este código.")
        return

    try:
        produto = {
            "nome_produto": input("Nome do Produto: "),
            "codigo_produto": codigo_produto,
            "categoria": input("Categoria: "),
            "quantidade_estoque": int(input("Quantidade em Estoque: ")),
            "preco": float(input("Preço (ex: 199.99): ")),
            "descricao": input("Descrição: "),
            "fornecedor": input("Fornecedor: "),
            "estoque_minimo": int(input("Nível mínimo para alerta de estoque: "))
        }
        produtos.append(produto)
        salvar_produtos(produtos)
        print(f"\n[SUCESSO] Produto '{produto['nome_produto']}' cadastrado!")
        
        # Registrar movimentação inicial
        registrar_movimentacao('entrada', codigo_produto, produto['nome_produto'], 
                              produto['quantidade_estoque'], 'Cadastro inicial')
        
        # Gera o QR Code
        dados_qr = (
            f"Nome: {produto['nome_produto']}\n"
            f"Código: {produto['codigo_produto']}\n"
            f"Categoria: {produto['categoria']}\n"
            f"Quantidade em Estoque: {produto['quantidade_estoque']}\n"
            f"Preço: R$ {produto['preco']:.2f}\n"
            f"Descrição: {produto['descricao']}\n"
            f"Fornecedor: {produto['fornecedor']}\n"
            f"Estoque Mínimo: {produto['estoque_minimo']}"
        )
        gerar_qr_code(dados_qr, produto['codigo_produto'])

    except ValueError:
        print("\n[ERRO] Quantidade, preço e estoque mínimo devem ser números.")

def listar_produtos():
    """Exibe todos os produtos cadastrados."""
    produtos = carregar_produtos()
    if not produtos:
        print("\n[INFO] Nenhum produto cadastrado.")
        return

    print("\n--- Lista de Produtos Cadastrados ---")
    for p in produtos:
        print("-" * 30)
        for chave, valor in p.items():
            if chave == 'preco':
                print(f"Preço: R$ {valor:.2f}")
            else:
                print(f"{chave.replace('_', ' ').capitalize()}: {valor}")
        verificar_estoque_baixo(p, silencioso=False)
    print("-" * 30)

def gerenciar_estoque():
    """Submenu para adicionar, remover ou atualizar o estoque."""
    codigo = input("Digite o código do produto para gerenciar o estoque: ")
    produtos = carregar_produtos()
    produto_encontrado = None
    indice = -1
    
    for i, p in enumerate(produtos):
        if p['codigo_produto'] == codigo:
            produto_encontrado = p
            indice = i
            break
            
    if not produto_encontrado:
        print("\n[ERRO] Produto não encontrado.")
        return

    print(f"\nGerenciando estoque de: {produto_encontrado['nome_produto']} (Atual: {produto_encontrado['quantidade_estoque']})")
    print("a - Adicionar ao Estoque")
    print("r - Remover do Estoque")
    print("u - Atualizar Estoque (manual)")
    
    opcao = input("Escolha uma opção: ").lower()
    
    try:
        quantidade_anterior = produto_encontrado['quantidade_estoque']
        
        if opcao == 'a':
            quantidade = int(input("Quantidade a adicionar: "))
            produto_encontrado['quantidade_estoque'] += quantidade
            registrar_movimentacao('entrada', codigo, produto_encontrado['nome_produto'], 
                                  quantidade, 'Entrada manual')
        elif opcao == 'r':
            quantidade = int(input("Quantidade a remover: "))
            if quantidade > produto_encontrado['quantidade_estoque']:
                print("\n[ERRO] Não é possível remover mais do que a quantidade existente.")
                return
            produto_encontrado['quantidade_estoque'] -= quantidade
            registrar_movimentacao('saida', codigo, produto_encontrado['nome_produto'], 
                                  quantidade, 'Saída manual')
        elif opcao == 'u':
            quantidade = int(input("Digite a nova quantidade total do estoque: "))
            diferenca = quantidade - quantidade_anterior
            produto_encontrado['quantidade_estoque'] = quantidade
            tipo = 'entrada' if diferenca > 0 else 'saida'
            registrar_movimentacao(tipo, codigo, produto_encontrado['nome_produto'], 
                                  abs(diferenca), 'Ajuste manual de estoque')
        else:
            print("\n[ERRO] Opção inválida.")
            return

        produtos[indice] = produto_encontrado
        salvar_produtos(produtos)
        print("\n[SUCESSO] Estoque atualizado.")
        verificar_estoque_baixo(produto_encontrado)

    except ValueError:
        print("\n[ERRO] Por favor, digite um número válido.")

def verificar_estoque_baixo(produto, silencioso=True):
    """Verifica se o estoque está baixo e notifica."""
    if produto['quantidade_estoque'] <= produto['estoque_minimo']:
        mensagem = f"  -> ALERTA: Estoque baixo! (Atual: {produto['quantidade_estoque']}, Mínimo: {produto['estoque_minimo']})"
        if not silencioso:
            print(mensagem)
        return True, mensagem
    return False, ""

def relatorio_estoque_baixo():
    """Exibe um relatório de todos os produtos com estoque baixo."""
    print("\n--- Relatório de Estoque Baixo ---")
    produtos = carregar_produtos()
    encontrou_item = False
    for p in produtos:
        baixo, mensagem = verificar_estoque_baixo(p)
        if baixo:
            print(f"Produto: {p['nome_produto']} (Código: {p['codigo_produto']})")
            print(mensagem)
            print("-" * 20)
            encontrou_item = True
    
    if not encontrou_item:
        print("[INFO] Nenhum produto com estoque baixo no momento.")

# --- Funcionalidades de QR Code ---
def gerar_qr_code(dados_texto, codigo_produto):
    """Gera um QR Code com os dados formatados do produto."""
    garantir_pasta_existente(QR_FOLDER)
    
    caminho_arquivo = os.path.join(QR_FOLDER, f"{codigo_produto.replace(' ', '_')}.png")
    
    img = qrcode.make(dados_texto)
    img.save(caminho_arquivo)
    print(f"[INFO] QR Code gerado e salvo em '{caminho_arquivo}'")

def ler_e_consultar_qr():
    """Lê um QR code de um arquivo e exibe os dados do produto."""
    print("\n--- Consultar Produto por QR Code ---")
    caminho_arquivo = input("Digite o caminho do arquivo do QR Code: ").strip()

    if not os.path.exists(caminho_arquivo):
        print("\n[ERRO] Arquivo não encontrado.")
        return

    try:
        imagem = cv2.imread(caminho_arquivo)
        dados_decodificados = decode(imagem)

        if not dados_decodificados:
            print("\n[ERRO] Nenhum QR Code encontrado na imagem.")
            return

        dados_lidos = dados_decodificados[0].data.decode('utf-8')
        print("\n--- Detalhes do Produto (QR Code) ---")
        print(dados_lidos)

    except Exception as e:
        print(f"\n[ERRO] Falha ao processar: {e}")

# ======================================================================
# === ENTREGA 2: VENDAS, DESCONTOS E RELATÓRIOS ===
# ======================================================================

# --- 3. VENDAS ---
def registrar_venda():
    """Registra uma nova venda de produto."""
    print("\n--- Registrar Nova Venda ---")
    produtos = carregar_produtos()
    
    if not produtos:
        print("\n[ERRO] Nenhum produto cadastrado.")
        return
    
    # Exibir produtos disponíveis
    print("\nProdutos disponíveis:")
    for p in produtos:
        if p['quantidade_estoque'] > 0:
            print(f"  - Código: {p['codigo_produto']} | {p['nome_produto']} | "
                  f"Preço: R$ {p['preco']:.2f} | Estoque: {p['quantidade_estoque']}")
    
    codigo = input("\nDigite o código do produto: ")
    produto_encontrado = None
    indice = -1
    
    for i, p in enumerate(produtos):
        if p['codigo_produto'] == codigo:
            produto_encontrado = p
            indice = i
            break
    
    if not produto_encontrado:
        print("\n[ERRO] Produto não encontrado.")
        return
    
    if produto_encontrado['quantidade_estoque'] == 0:
        print("\n[ERRO] Produto sem estoque disponível.")
        return
    
    try:
        quantidade = int(input("Quantidade a vender: "))
        
        if quantidade <= 0:
            print("\n[ERRO] Quantidade deve ser maior que zero.")
            return
        
        if quantidade > produto_encontrado['quantidade_estoque']:
            print(f"\n[ERRO] Estoque insuficiente! Disponível: {produto_encontrado['quantidade_estoque']}")
            return
        
        # Calcular valores
        valor_unitario = produto_encontrado['preco']
        subtotal = valor_unitario * quantidade
        
        # Aplicar desconto
        desconto_percentual = float(input("Desconto (%) [0 para nenhum]: ") or 0)
        valor_desconto = subtotal * (desconto_percentual / 100)
        valor_total = subtotal - valor_desconto
        
        # Criar venda
        vendas = carregar_vendas()
        venda = {
            "id_venda": len(vendas) + 1,
            "codigo_produto": codigo,
            "nome_produto": produto_encontrado['nome_produto'],
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "subtotal": subtotal,
            "desconto_percentual": desconto_percentual,
            "valor_desconto": valor_desconto,
            "valor_total": valor_total,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        vendas.append(venda)
        salvar_vendas(vendas)
        
        # ATUALIZAÇÃO AUTOMÁTICA DO ESTOQUE
        produto_encontrado['quantidade_estoque'] -= quantidade
        produtos[indice] = produto_encontrado
        salvar_produtos(produtos)
        
        # Registrar movimentação
        registrar_movimentacao('saida', codigo, produto_encontrado['nome_produto'], 
                              quantidade, f"Venda #{venda['id_venda']}")
        
        print("\n[SUCESSO] Venda registrada com sucesso!")
        print(f"Novo estoque de '{produto_encontrado['nome_produto']}': {produto_encontrado['quantidade_estoque']}")
        
        # EMISSÃO DE RECIBO
        emitir_recibo(venda)
        
        verificar_estoque_baixo(produto_encontrado)
        
    except ValueError:
        print("\n[ERRO] Valores inválidos.")

def emitir_recibo(venda):
    """Emite o recibo/nota fiscal da venda."""
    print("\n" + "="*50)
    print("           RECIBO DE VENDA")
    print("="*50)
    print(f"Venda #: {venda['id_venda']}")
    print(f"Data: {venda['data']}")
    print("-"*50)
    print(f"Produto: {venda['nome_produto']}")
    print(f"Código: {venda['codigo_produto']}")
    print(f"Quantidade: {venda['quantidade']} unidade(s)")
    print(f"Valor Unitário: R$ {venda['valor_unitario']:.2f}")
    print(f"Subtotal: R$ {venda['subtotal']:.2f}")
    
    if venda['desconto_percentual'] > 0:
        print(f"Desconto ({venda['desconto_percentual']}%): -R$ {venda['valor_desconto']:.2f}")
    
    print("-"*50)
    print(f"VALOR TOTAL: R$ {venda['valor_total']:.2f}")
    print("="*50)
    print("      Obrigado pela preferência!")
    print("="*50 + "\n")

def aplicar_promocao():
    """Aplica desconto promocional a um produto específico."""
    print("\n--- Aplicar Promoção a Produto ---")
    produtos = carregar_produtos()
    
    if not produtos:
        print("\n[ERRO] Nenhum produto cadastrado.")
        return
    
    print("\nProdutos disponíveis:")
    for p in produtos:
        print(f"  - Código: {p['codigo_produto']} | {p['nome_produto']} | "
              f"Preço: R$ {p['preco']:.2f}")
    
    codigo = input("\nDigite o código do produto: ")
    produto_encontrado = None
    indice = -1
    
    for i, p in enumerate(produtos):
        if p['codigo_produto'] == codigo:
            produto_encontrado = p
            indice = i
            break
    
    if not produto_encontrado:
        print("\n[ERRO] Produto não encontrado.")
        return
    
    try:
        print(f"\nProduto: {produto_encontrado['nome_produto']}")
        print(f"Preço atual: R$ {produto_encontrado['preco']:.2f}")
        
        desconto = float(input("Digite o desconto promocional (%): "))
        
        if desconto < 0 or desconto > 100:
            print("\n[ERRO] Desconto deve estar entre 0 e 100%.")
            return
        
        # Salvar preço original se ainda não tiver
        if 'preco_original' not in produto_encontrado:
            produto_encontrado['preco_original'] = produto_encontrado['preco']
        
        novo_preco = produto_encontrado['preco_original'] * (1 - desconto/100)
        produto_encontrado['preco'] = novo_preco
        produto_encontrado['promocao_ativa'] = desconto
        
        produtos[indice] = produto_encontrado
        salvar_produtos(produtos)
        
        print(f"\n[SUCESSO] Promoção aplicada!")
        print(f"Preço original: R$ {produto_encontrado['preco_original']:.2f}")
        print(f"Novo preço: R$ {novo_preco:.2f} ({desconto}% OFF)")
        
    except ValueError:
        print("\n[ERRO] Valor inválido.")

def remover_promocao():
    """Remove promoção de um produto."""
    print("\n--- Remover Promoção ---")
    produtos = carregar_produtos()
    
    produtos_com_promocao = [p for p in produtos if 'promocao_ativa' in p]
    
    if not produtos_com_promocao:
        print("\n[INFO] Nenhum produto com promoção ativa.")
        return
    
    print("\nProdutos com promoção:")
    for p in produtos_com_promocao:
        print(f"  - Código: {p['codigo_produto']} | {p['nome_produto']} | "
              f"Desconto: {p['promocao_ativa']}% | Preço: R$ {p['preco']:.2f}")
    
    codigo = input("\nDigite o código do produto: ")
    
    for i, p in enumerate(produtos):
        if p['codigo_produto'] == codigo and 'promocao_ativa' in p:
            preco_original = p.get('preco_original', p['preco'])
            p['preco'] = preco_original
            del p['promocao_ativa']
            if 'preco_original' in p:
                del p['preco_original']
            
            produtos[i] = p
            salvar_produtos(produtos)
            
            print(f"\n[SUCESSO] Promoção removida! Preço voltou para R$ {preco_original:.2f}")
            return
    
    print("\n[ERRO] Produto não encontrado ou sem promoção ativa.")

# --- 4. RELATÓRIOS ---
def relatorio_vendas():
    """Exibe relatório detalhado de vendas."""
    print("\n--- Relatório de Vendas ---")
    vendas = carregar_vendas()
    
    if not vendas:
        print("\n[INFO] Nenhuma venda registrada.")
        return
    
    # Opção de filtro por data
    print("\nFiltrar por período?")
    print("1 - Todas as vendas")
    print("2 - Filtrar por data")
    opcao = input("Escolha: ")
    
    vendas_filtradas = vendas
    
    if opcao == '2':
        data_inicial = input("Data inicial (DD/MM/YYYY): ")
        data_final = input("Data final (DD/MM/YYYY): ")
        # Simplificação: comparação de strings (funciona para formato DD/MM/YYYY)
        vendas_filtradas = [v for v in vendas 
                           if data_inicial <= v['data'].split()[0] <= data_final]
    
    if not vendas_filtradas:
        print("\n[INFO] Nenhuma venda no período selecionado.")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<6} {'Data':<18} {'Produto':<25} {'Qtd':<6} {'Total':>10}")
    print("="*80)
    
    total_geral = 0
    total_descontos = 0
    
    for v in vendas_filtradas:
        print(f"{v['id_venda']:<6} {v['data']:<18} {v['nome_produto']:<25} "
              f"{v['quantidade']:<6} R$ {v['valor_total']:>8.2f}")
        total_geral += v['valor_total']
        total_descontos += v['valor_desconto']
    
    print("="*80)
    print(f"Total de vendas: {len(vendas_filtradas)}")
    print(f"Total em descontos: R$ {total_descontos:.2f}")
    print(f"TOTAL GERAL: R$ {total_geral:.2f}")
    print("="*80 + "\n")

def relatorio_estoque():
    """Exibe relatório completo do estoque atual."""
    print("\n--- Relatório de Estoque ---")
    produtos = carregar_produtos()
    
    if not produtos:
        print("\n[INFO] Nenhum produto cadastrado.")
        return
    
    print("\n" + "="*90)
    print(f"{'Código':<12} {'Produto':<25} {'Categoria':<15} {'Qtd':<8} {'Preço':>10}")
    print("="*90)
    
    valor_total_estoque = 0
    
    for p in produtos:
        valor_produto = p['preco'] * p['quantidade_estoque']
        valor_total_estoque += valor_produto
        
        promocao_info = f" ({p['promocao_ativa']}% OFF)" if 'promocao_ativa' in p else ""
        
        print(f"{p['codigo_produto']:<12} {p['nome_produto']:<25} "
              f"{p['categoria']:<15} {p['quantidade_estoque']:<8} "
              f"R$ {p['preco']:>8.2f}{promocao_info}")
        
        if p['quantidade_estoque'] <= p['estoque_minimo']:
            print(f"  ⚠ ALERTA: Estoque baixo (mínimo: {p['estoque_minimo']})")
    
    print("="*90)
    print(f"Total de produtos: {len(produtos)}")
    print(f"Valor total em estoque: R$ {valor_total_estoque:.2f}")
    print("="*90 + "\n")

def historico_movimentacoes():
    """Exibe o histórico de todas as movimentações de estoque."""
    print("\n--- Histórico de Movimentações ---")
    movimentacoes = carregar_movimentacoes()
    
    if not movimentacoes:
        print("\n[INFO] Nenhuma movimentação registrada.")
        return
    
    # Opção de filtro
    print("\nFiltrar movimentações:")
    print("1 - Todas")
    print("2 - Apenas entradas")
    print("3 - Apenas saídas")
    print("4 - Por produto")
    opcao = input("Escolha: ")
    
    movimentacoes_filtradas = movimentacoes
    
    if opcao == '2':
        movimentacoes_filtradas = [m for m in movimentacoes if m['tipo'] == 'entrada']
    elif opcao == '3':
        movimentacoes_filtradas = [m for m in movimentacoes if m['tipo'] == 'saida']
    elif opcao == '4':
        codigo = input("Digite o código do produto: ")
        movimentacoes_filtradas = [m for m in movimentacoes if m['codigo_produto'] == codigo]
    
    if not movimentacoes_filtradas:
        print("\n[INFO] Nenhuma movimentação encontrada.")
        return
    
    print("\n" + "="*100)
    print(f"{'ID':<5} {'Data':<18} {'Tipo':<10} {'Produto':<25} {'Qtd':<8} {'Observação'}")
    print("="*100)
    
    for m in movimentacoes_filtradas:
        tipo_display = "ENTRADA" if m['tipo'] == 'entrada' else "SAÍDA"
        print(f"{m['id']:<5} {m['data']:<18} {tipo_display:<10} "
              f"{m['nome_produto']:<25} {m['quantidade']:<8} {m['observacao']}")
    
    print("="*100)
    print(f"Total de movimentações: {len(movimentacoes_filtradas)}")
    print("="*100 + "\n")

# --- Menu Principal ---
def menu():
    """Exibe o menu principal e gerencia as ações do usuário."""
    garantir_pasta_existente(QR_FOLDER)
    
    while True:
        print("\n" + "="*50)
        print("   SISTEMA DE GESTÃO ERP - ENTREGA 2")
        print("="*50)
        print("\n=== GERENCIAMENTO DE PRODUTOS ===")
        print("1. Cadastrar Produto")
        print("2. Listar Todos os Produtos")
        print("3. Gerenciar Estoque")
        print("4. Consultar Produto por QR Code")
        print("5. Relatório de Estoque Baixo")
        
        print("\n=== VENDAS ===")
        print("6. Registrar Venda")
        print("7. Aplicar Promoção/Desconto")
        print("8. Remover Promoção")
        
        print("\n=== RELATÓRIOS ===")
        print("9. Relatório de Vendas")
        print("10. Relatório de Estoque")
        print("11. Histórico de Movimentações")
        
        print("\n12. Sair")
        print("="*50)
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastrar_produto()
        elif escolha == '2':
            listar_produtos()
        elif escolha == '3':
            gerenciar_estoque()
        elif escolha == '4':
            ler_e_consultar_qr()
        elif escolha == '5':
            relatorio_estoque_baixo()
        elif escolha == '6':
            registrar_venda()
        elif escolha == '7':
            aplicar_promocao()
        elif escolha == '8':
            remover_promocao()
        elif escolha == '9':
            relatorio_vendas()
        elif escolha == '10':
            relatorio_estoque()
        elif escolha == '11':
            historico_movimentacoes()
        elif escolha == '12':
            print("\n[INFO] Saindo do sistema...")
            break
        else:
            print("\n[ERRO] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
