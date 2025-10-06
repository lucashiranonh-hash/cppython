Sistema de Gestão de Produtos e Estoque - ERP
Sistema completo de gestão empresarial desenvolvido em Python com funcionalidades de cadastro de produtos, controle de estoque, vendas, descontos/promoções e relatórios gerenciais.

👥 Integrantes da Equipe

Felipe Stefani Honorato - RM: 563380

Pedro Leal Murad - RM: 565460

Lucas Yuji Nakayama Hirano - RM: 563420


📋 Funcionalidades
Entrega 1: Gerenciamento de Produtos

✅ Cadastro completo de produtos com QR Code

✅ Listagem de produtos cadastrados

✅ Gerenciamento de estoque (entrada, saída e ajustes)

✅ Consulta de produtos via QR Code

✅ Alertas de estoque baixo

Entrega 2: Vendas e Relatórios

3. Vendas

Registro de Vendas: Sistema completo para registrar vendas de produtos

Atualização Automática do Estoque: O estoque é reduzido automaticamente após cada venda

Emissão de Recibo: Geração automática de recibo/nota fiscal após cada venda

Descontos e Promoções: Aplicação de descontos percentuais nas vendas e promoções permanentes nos produtos

4. Relatórios

Relatório de Vendas: Detalhamento completo de vendas (data, produtos, quantidade, valores)

Relatório de Estoque: Visualização da quantidade atual e valor de todos os produtos

Histórico de Movimentações: Registro completo de todas as entradas e saídas de estoque


🚀 Instalação
1. Clone o Repositório
Via terminal:
bashgit clone <URL-DO-SEU-REPOSITORIO>
cd <NOME-DA-PASTA>
Ou via Visual Studio Code:

Abra o VS Code

Clique em "Explorer" no canto superior esquerdo

Clique em "Clone Repository"

Cole o link do repositório GitHub

Selecione a pasta de destino

Clique em "Open" quando aparecer a mensagem

2. Instale as Dependências

Abra o terminal no VS Code (Ctrl + J ou Ctrl + ') e execute:

bashpip install -r requirements.txt

Ou instale manualmente:

bashpip install qrcode

pip install opencv-python

pip install pyzbar

💻 Como Executar

Abra o terminal no VS Code (Ctrl + J)

Execute o programa:

bashpython main.py


O menu principal será exibido no console

Digite o número da opção desejada e pressione Enter


📁 Estrutura de Arquivos

├── main.py                 # Arquivo principal do sistema

├── produtos.json           # Banco de dados de produtos

├── vendas.json            # Registro de todas as vendas

├── movimentacoes.json     # Histórico de movimentações

├── requirements.txt       # Dependências do projeto

├── qrcodes/              # Pasta com QR Codes gerados

└── README.md             # Documentação do projeto

📊 Formato dos Arquivos JSON

produtos.json

json[
  {
    "nome_produto": "Shorts Adidas",
    "codigo_produto": "shorts",
    "categoria": "Vestuário",
    "quantidade_estoque": 50,
    "preco": 100.0,
    "descricao": "Shorts da Adidas preto e estiloso",
    "fornecedor": "deeply",
    "estoque_minimo": 5
  }
]


vendas.json
[
  {
    "id_venda": 1,
    "codigo_produto": "shorts",
    "nome_produto": "Shorts Adidas",
    "quantidade": 2,
    "valor_unitario": 100.0,
    "subtotal": 200.0,
    "desconto_percentual": 10.0,
    "valor_desconto": 20.0,
    "valor_total": 180.0,
    "data": "05/10/2025 14:30:00"
  }
]

movimentacoes.json

json[

[
  {
    "id": 1,
    "tipo": "saida",
    "codigo_produto": "shorts",
    "nome_produto": "Shorts Adidas",
    "quantidade": 2,
    "observacao": "Venda #1",
    "data": "05/10/2025 14:30:00"
  }
]


🎯 Funcionalidades Detalhadas

Registro de Vendas (Opção 6)


Exibe produtos disponíveis em estoque

Solicita código do produto e quantidade

Permite aplicar desconto percentual

Atualiza automaticamente o estoque

Gera recibo detalhado

Registra movimentação de saída

Promoções (Opções 7 e 8)


Aplicar Promoção: Define desconto permanente no preço do produto

Remover Promoção: Restaura o preço original do produto

Relatórios (Opções 9, 10, 11)

Relatório de Vendas:

Filtro por período (data inicial e final)

Totalizadores de vendas e descontos

Valor total vendido

Relatório de Estoque:

Lista completa com quantidades

Valor total em estoque

Indicação de produtos com estoque baixo

Produtos com promoção ativa

Histórico de Movimentações:

Filtros: todas, entradas, saídas ou por produto

Detalhamento completo de cada movimentação

Data e observações


📝 Exemplo de Uso

Realizar uma Venda

1. Selecione opção 6 (Registrar Venda)

2. Digite o código do produto (ex: shorts)

3. Informe a quantidade (ex: 2)

4. Aplique desconto se desejar (ex: 10)

5. O sistema emitirá o recibo automaticamente

6. O estoque será atualizado

Aplicar Promoção

1. Selecione opção 7 (Aplicar Promoção)

2. Digite o código do produto

3. Informe o desconto percentual (ex: 15)

4. O preço será atualizado permanentemente

⚠️ Alertas e Validações

❌ Não é possível vender quantidade maior que o estoque

❌ Código de produto deve ser único

⚠️ Alerta automático quando estoque atinge o mínimo

✅ Validação de valores numéricos

✅ Confirmação em operações críticas


🔧 Requisitos do Sistema

Python 3.7 ou superior

Bibliotecas: qrcode, opencv-python, pyzbar

Sistema operacional: Windows, Linux ou macOS


📖 Notas Adicionais

Os dados são persistidos em arquivos JSON

QR Codes são salvos automaticamente na pasta /qrcodes

Todas as movimentações são registradas para auditoria

O sistema valida todas as entradas do usuário

Recibos são exibidos no console após cada venda


🐛 Solução de Problemas

Erro ao instalar pyzbar:

Windows:

bashpip install pyzbar

# Pode ser necessário instalar o ZBar separadamente

Linux:

bashsudo apt-get install libzbar0

pip install pyzbar

macOS:

bashbrew install zbar

pip install pyzbar

Arquivo não encontrado:

Verifique se está executando o programa na pasta correta

Os arquivos JSON são criados automaticamente na primeira execução


📫 Suporte
Para dúvidas ou problemas, entre em contato com a equipe através dos RMs fornecidos.

