# MollyBarber

**MollyBarber** é uma aplicação web desenvolvida com Django para gerenciamento de agendamentos e serviços de barbearia. Possui suporte a múltiplos barbeiros, cada um com suas próprias categorias, serviços e horários disponíveis, com interface moderna baseada em Bootstrap 5.

---

##  Funcionalidades

### Usuários

* Cadastro com tipos de usuário: **admin**, **barbeiro** e **cliente**.
* Apenas barbeiros têm acesso a funcionalidades administrativas (categorias, serviços, agendamentos).

### Autenticação

* Login, logout e "esqueci minha senha" via e-mail.
* Controle de acesso baseado em `user_type`.

### Serviços e Categorias

* Cada barbeiro possui suas **próprias categorias e serviços**.
* Formulários com campos filtrados automaticamente pelo barbeiro logado.

### Agendamentos

* Sistema de agendamento com:

  * Data/hora
  * Cliente (nome e celular)
  * Serviço (somente do barbeiro logado)
  * Status
* Visualização com **FullCalendar** (eventos dinâmicos por barbeiro).

### Horários Disponíveis

* Cada barbeiro define seus **disponíveis via JSONField**:

```json
{
  "daysOfWeek": [1, 2, 3],
  "startTime": "09:00",
  "endTime": "17:00"
}
```

### Interface Moderna

* Baseada em Bootstrap 5.
* Tela de login com logo centralizada.
* Todos os formulários abertos em **modais AJAX** (add, edit, delete).

---

##  Requisitos e Instalação

### requirements.txt

```txt
django>=4.2
djangorestframework
django-crispy-forms
django-widget-tweaks
gunicorn
psycopg2-binary
python-decouple
```

### Instalação local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🛁 Docker Compose (sem Nginx)

### docker-compose.yml (essencial)

```yaml
version: '3.9'
services:
  web:
    build: .
    container_name: mollybarber-web
    env_file:
      - .env
    volumes:
      - ./app:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:15
    container_name: mollybarber-db
    environment:
      POSTGRES_DB: mollybarber
      POSTGRES_USER: molly
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### .env (exemplo)

```env
DEBUG=0
SECRET_KEY=uma-chave-secreta
ALLOWED_HOSTS=*
DB_NAME=mollybarber
DB_USER=molly
DB_PASSWORD=secret
DB_HOST=db
```

---

##  Documentação Técnica

### Estrutura

* `UserProfile` extendendo `User` com campo `user_type`
* `Barber` com relação OneToOne com `User`
* `Category`, `Service`, `Appointment`, todos relacionados ao barbeiro logado

### Views com controle de acesso

* Decorador `@barber_required` criado para restringir rotas a barbeiros
* Uso de `request.user.barber` para consultas e filtros seguros

### FullCalendar integration

* `appointments_feed` filtra por intervalo (`start`, `end`) enviado pelo calendário
* Eventos renderizados com:

```json
{
  "id": 1,
  "title": "Corte - João",
  "start": "2025-05-27T10:00",
  "end": "2025-05-27T10:30",
  "url": "/agendamentos/1/detalhes/"
}
```

### Modais via jQuery (com JSON)

* Todas as views `add/edit/delete` usam AJAX para retornar `{ html: ... }`
* Formulários são enviados via AJAX e atualizam a interface sem reload

---

## Planos Futuros

* Upload de avatar por barbeiro
* Painel com estatísticas de agendamentos
* Notificação por e-mail/SMS (via Twilio ou SendGrid)

---

## 💌 Contato

Este projeto foi construído para demonstrar o uso do Django. Para suporte ou consultoria:

* https://blog.robertabrandao.com.br/about/
