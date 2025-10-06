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
