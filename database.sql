
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    tipo VARCHAR(20) CHECK (tipo IN ('cliente', 'barbeiro', 'admin')) NOT NULL
);


CREATE TABLE disponiveis (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    horarios_disponiveis TEXT,
    CONSTRAINT fk_barbeiro_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);


CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco NUMERIC(10,2) NOT NULL,
    disponivel_id INTEGER NOT NULL,
    categoria_id INTEGER,
    CONSTRAINT fk_servico_barbeiro FOREIGN KEY (disponivel_id) REFERENCES disponiveis(id) ON DELETE CASCADE,
    CONSTRAINT fk_servico_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);


CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    disponivel_id INTEGER NOT NULL,
    servico_id INTEGER NOT NULL,
    data_horario TIMESTAMP NOT NULL,
    status VARCHAR(20) CHECK (status IN ('confirmado', 'cancelado', 'concluido')) DEFAULT 'confirmado',
    CONSTRAINT fk_agendamento_cliente FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_agendamento_barbeiro FOREIGN KEY (disponivel_id) REFERENCES disponiveis(id) ON DELETE CASCADE,
    CONSTRAINT fk_agendamento_servico FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE
);




INSERT INTO usuarios (nome, email, senha, telefone, tipo) VALUES
  ('João Silva', 'joao.silva@example.com', 'senha123', '31987654321', 'cliente'),
  ('Maria Oliveira', 'maria.oliveira@example.com', 'senha456', '31987654322', 'cliente'),
  ('Carlos Souza', 'carlos.souza@example.com', 'senha789', '31987654323', 'barbeiro'),
  ('Ana Costa', 'ana.costa@example.com', 'senha101', '31987654324', 'barbeiro'),
  ('Lucas Pereira', 'lucas.pereira@example.com', 'senha112', '31987654325', 'admin'),
  ('Pedro Lima', 'pedro.lima@example.com', 'senha321', '31987654326', 'cliente'),
  ('Fernanda Rocha', 'fernanda.rocha@example.com', 'senha654', '31987654327', 'cliente');



INSERT INTO disponiveis (usuario_id, horarios_disponiveis) VALUES
  (3, 'Segunda a Sexta: 09:00-18:00'),
  (4, 'Segunda a Sexta: 10:00-19:00'),
  (3, 'Sábado: 08:00-12:00');


INSERT INTO categorias (nome) VALUES
  ('Corte de cabelo'),
  ('Barba'),
  ('Design de sobrancelha'),
  ('Tratamento capilar');



INSERT INTO servicos (nome, preco, disponivel_id, categoria_id) VALUES
  ('Corte masculino', 50.00, 1, 1),
  ('Corte feminino', 60.00, 1, 1),
  ('Barba completa', 40.00, 2, 2),
  ('Design de sobrancelha', 30.00, 2, 3),
  ('Hidratação capilar', 70.00, 3, 4),
  ('Corte infantil', 35.00, 1, 1);



INSERT INTO agendamentos (cliente_id, disponivel_id, servico_id, data_horario, status) VALUES
  (1, 1, 1, '2025-05-06 10:00:00', 'confirmado'),
  (2, 2, 3, '2025-05-07 14:00:00', 'confirmado'),
  (1, 1, 2, '2025-05-08 11:00:00', 'cancelado'),
  (6, 3, 5, '2025-05-09 09:30:00', 'confirmado'),
  (7, 1, 6, '2025-05-10 15:00:00', 'concluido');

