# Registro de validação técnica

Validação executada em 25 de setembro de 2026.

## Ambiente utilizado

- Python 3.12.14
- FastAPI 0.141.1
- Pydantic 2.13.5
- Uvicorn 0.54.0
- Pytest 9.1.1
- httpx2 2.13.1

## Verificações concluídas

- 41 testes automatizados aprovados;
- compilação de todos os módulos Python concluída;
- análise estática e formatação aprovadas pelo Ruff;
- esquema OpenAPI gerado corretamente;
- rotas das três estratégias responderam com os tipos de conteúdo esperados;
- CSV experimental gerado com 9 combinações entre estratégia e cenário;
- arquivo `docker-compose.yml` validado sintaticamente.

O ambiente de validação não possui o executável Docker. Por isso, a construção
da imagem e a execução dos serviços do Compose devem ser confirmadas em uma
máquina com Docker Desktop ou Docker Engine. A mesma suíte de testes pode ser
executada pelo serviço `tests` definido no Compose.

