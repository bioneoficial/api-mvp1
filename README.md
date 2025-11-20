# API - Gestão de Comissões

Este é o backend do MVP de Gestão de Comissões. Ele provê uma API RESTful para cadastro de vendas e cálculo automático de comissões.

## Tecnologias
- Python 3
- Flask
- SQLAlchemy (SQLite)
- Flask-CORS
- Flasgger (Swagger UI)

## Instalação

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como Executar

Execute a aplicação:
```bash
python app.py
```

A API estará rodando em `http://localhost:5001`.

## Documentação da API (Swagger)

Após iniciar a aplicação, acesse a documentação interativa em:
- [http://localhost:5001/apidocs/](http://localhost:5001/apidocs/) (ou apenas abra a raiz e será redirecionado)
