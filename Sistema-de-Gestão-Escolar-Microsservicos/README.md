# Projeto Final: Microsserviços de Gestão Acadêmica

## Visão Geral

Este repositório contém o código-fonte para três microsserviços desenvolvidos em Python/Flask. O objetivo é demonstrar uma arquitetura de serviços distribuídos para gerenciamento de entidades, reservas e atividades acadêmicas.

### Características Principais

- Arquitetura MVC em cada serviço
- Bancos de dados SQLite isolados via SQLAlchemy
- Documentação de API através do Swagger UI (Flasgger)
- Comunicação síncrona entre serviços usando a biblioteca `requests`

> **Observação**: Os bancos de dados (SQLite) são iniciados vazios, sem dados de seed.

## Estrutura dos Serviços e Acesso

Os serviços podem ser acessados localmente nas seguintes portas, com Swagger UI disponível no caminho `/apidocs`:

| Serviço | Funcionalidade Principal | Endereço Local |
|---------|-------------------------|----------------|
| Gerenciamento | Cadastro de Professores e Turmas | http://localhost:5000 |
| Reservas | Criação e gestão de Reservas de Salas | http://localhost:5001 |
| Atividades | Definição e acompanhamento de Atividades | http://localhost:5002 |

## Instruções de Execução

### Pré-requisitos
- Docker
- Docker Compose

### Comandos Principais

1. **Iniciar o Projeto**:
   ```bash
   docker compose up --build
   ```

2. **Parar e Limpar**:
   ```bash
   docker compose down
   ```

### Persistência de Dados
Os arquivos SQLite são persistidos dentro das pastas dos respectivos serviços no host (montados via volumes no Docker Compose).

## Fluxo de Comunicação e Validação

Os serviços implementam validações cruzadas através de chamadas síncronas ao serviço de Gerenciamento:

- **Serviço de Reservas**: 
  - Valida a existência do `turma_id` via `GET /turmas/{id}`

- **Serviço de Atividades**:
  - Valida `turma_id` via `GET /turmas/{id}`
  - Valida `professor_id` via `GET /professores/{id}`

## Estrutura Interna de Cada Microsserviço

```
├── app.py           # Inicializador do Flask e Swagger
├── routes.py        # Endpoints REST e documentação Flasgger
├── controllers/     # Lógica de negócio (CRUD)
├── models/         # Classes ORM (SQLAlchemy)
├── database.py     # Conexão com banco de dados
├── requirements.txt # Dependências
└── Dockerfile      # Configuração de deploy
```

## Testes Rápidos (Exemplos cURL)

### 1. Criar Professor (Gerenciamento: 5000)
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"nome":"Prof A","idade":40,"materia":"Matematica"}' \
     http://localhost:5000/professores
```

### 2. Criar Turma (Gerenciamento: 5000)
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"descricao":"Turma 1","professor_id":1}' \
     http://localhost:5000/turmas
```

### 3. Criar Reserva (Reservas: 5001)
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"num_sala":"101","lab":false,"data":"2025-11-20","turma_id":1}' \
     http://localhost:5001/reservas
```

### 4. Criar Atividade (Atividades: 5002)
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"titulo":"Prova 1","descricao":"...", "peso_porcento":30, "data_entrega":"2025-12-01","turma_id":1,"professor_id":1}' \
     http://localhost:5002/atividades
```

## Script de exemplo para popular a API (PowerShell)

Criei um script PowerShell para popular os serviços com dados de exemplo (professor, turma, aluno, atividade, reserva, nota).

- Arquivo: `scripts\seed_sample.ps1`
- Uso (no PowerShell):
```
cd "C:\Users\kaiqu\Downloads\ap2\Sistema--Escolar-API-Microsservicos\Sistema-de-Gestão-Escolar-Microsservicos"
.\scripts\seed_sample.ps1
```

O script aguarda os serviços estarem prontos (`/status`) e em seguida cria os recursos na ordem correta.
