# Projeto

## Rodar postgres com docker

```bash
docker run -d --name postgres-barber -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=12345678 -e PGDATA=/var/lib/postgresql/data/pgdata -v ./data:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_DB=mollybarber postgres
```
