-- Banco de dados para trabalho de faculdade (SQLite) - versão Sergipe
-- Alunos: dados totalmente fictícios.
-- Cursos/notas de corte: valores ilustrativos (aproximados), não oficiais.

DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS cursos_ies;

CREATE TABLE alunos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    nota_enem   REAL    NOT NULL CHECK (nota_enem BETWEEN 0 AND 1000),
    cidade      TEXT    NOT NULL,
    cpf         TEXT    NOT NULL UNIQUE,
    idade       INTEGER NOT NULL CHECK (idade >= 14),
    telefone    TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE
);

CREATE TABLE cursos_ies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    instituicao TEXT    NOT NULL,
    curso       TEXT    NOT NULL,
    nota_corte  REAL    NOT NULL CHECK (nota_corte BETWEEN 0 AND 1000),
    cidade      TEXT    NOT NULL
);

-- 10 alunos de Aracaju, 2 de São Cristóvão, 1 de Barra dos Coqueiros, 2 de Nossa Senhora do Socorro
INSERT INTO alunos (nome, nota_enem, cidade, cpf, idade, telefone, email) VALUES
('Larissa Santos Menezes',    812.30, 'Aracaju',                   '312.456.789-01', 18, '(79) 99123-4501', 'larissa.menezes@email.com'),
('Matheus Andrade Lima',      698.45, 'Aracaju',                   '423.567.890-12', 19, '(79) 99234-5602', 'matheus.lima@email.com'),
('Beatriz Oliveira Vieira',   745.90, 'Aracaju',                   '534.678.901-23', 18, '(79) 99345-6703', 'beatriz.vieira@email.com'),
('Thiago Barreto Souza',      621.15, 'Aracaju',                   '645.789.012-34', 20, '(79) 99456-7804', 'thiago.souza@email.com'),
('Juliana Prado Cardoso',     773.60, 'Aracaju',                   '756.890.123-45', 17, '(79) 99567-8905', 'juliana.cardoso@email.com'),
('Rafael Nascimento Dantas',  587.80, 'Aracaju',                   '867.901.234-56', 21, '(79) 99678-9006', 'rafael.dantas@email.com'),
('Amanda Fontes Rezende',     834.25, 'Aracaju',                   '978.012.345-67', 18, '(79) 99789-0107', 'amanda.rezende@email.com'),
('Gustavo Henrique Mota',     654.70, 'Aracaju',                   '089.123.456-78', 19, '(79) 99890-1208', 'gustavo.mota@email.com'),
('Patrícia Lemos Almeida',    709.35, 'Aracaju',                   '190.234.567-89', 22, '(79) 99901-2309', 'patricia.almeida@email.com'),
('Vinícius Cruz Batista',     563.40, 'Aracaju',                   '201.345.678-90', 20, '(79) 98012-3410', 'vinicius.batista@email.com'),
('Letícia Moura Santana',     726.10, 'São Cristóvão',             '312.567.890-11', 18, '(79) 98123-4511', 'leticia.santana@email.com'),
('Caio Eduardo Pinto',        641.55, 'São Cristóvão',             '423.678.901-22', 19, '(79) 98234-5612', 'caio.pinto@email.com'),
('Natália Siqueira Brito',    678.90, 'Barra dos Coqueiros',       '534.789.012-33', 18, '(79) 98345-6713', 'natalia.brito@email.com'),
('Diego Ferreira Costa',      599.20, 'Nossa Senhora do Socorro',  '645.890.123-44', 20, '(79) 98456-7814', 'diego.costa@email.com'),
('Sabrina Mendonça Lopes',    751.80, 'Nossa Senhora do Socorro',  '756.901.234-55', 19, '(79) 98567-8915', 'sabrina.lopes@email.com');

-- 10 instituições de Sergipe x 10 cursos cada (100 registros)
INSERT INTO cursos_ies (instituicao, curso, nota_corte, cidade) VALUES
-- Universidade Federal de Sergipe (UFS)
('Universidade Federal de Sergipe (UFS)', 'Medicina',                    782.40, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Odontologia',                 722.60, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Direito',                     701.20, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Psicologia',                  690.80, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Ciência da Computação',       672.30, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Engenharia Civil',            668.50, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Engenharia de Computação',    659.70, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Enfermagem',                  655.10, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Administração',               621.40, 'São Cristóvão'),
('Universidade Federal de Sergipe (UFS)', 'Pedagogia',                   575.90, 'São Cristóvão'),
-- Universidade Tiradentes (UNIT)
('Universidade Tiradentes (UNIT)', 'Medicina',                           735.00, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Odontologia',                        640.20, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Direito',                            612.50, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Psicologia',                         598.30, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Fisioterapia',                       585.70, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Arquitetura e Urbanismo',            570.60, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Enfermagem',                         560.40, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Engenharia Civil',                   545.80, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Administração',                      505.20, 'Aracaju'),
('Universidade Tiradentes (UNIT)', 'Ciências Contábeis',                 490.30, 'Aracaju'),
-- Instituto Federal de Sergipe (IFS)
('Instituto Federal de Sergipe (IFS)', 'Engenharia Civil',                       612.30, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Engenharia Elétrica',                    598.70, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Análise e Desenvolvimento de Sistemas',  590.40, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Engenharia Mecânica',                    585.20, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Engenharia de Controle e Automação',     580.00, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Sistemas de Informação',                 575.10, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Gestão da Tecnologia da Informação',     545.30, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Licenciatura em Matemática',             520.80, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Licenciatura em Química',                510.90, 'Aracaju'),
('Instituto Federal de Sergipe (IFS)', 'Licenciatura em Física',                 505.60, 'Aracaju'),
-- Faculdade de Administração e Negócios de Sergipe (FANESE)
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Direito',                   560.40, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Psicologia',                540.60, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Fisioterapia',              525.40, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Engenharia Civil',          520.30, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Enfermagem',                510.50, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Educação Física',           490.80, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Sistemas de Informação',    485.90, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Administração',             480.20, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Publicidade e Propaganda',  478.30, 'Aracaju'),
('Faculdade de Administração e Negócios de Sergipe (FANESE)', 'Ciências Contábeis',        470.10, 'Aracaju'),
-- Faculdade Pio Décimo
('Faculdade Pio Décimo', 'Medicina',        725.80, 'Aracaju'),
('Faculdade Pio Décimo', 'Odontologia',     630.40, 'Aracaju'),
('Faculdade Pio Décimo', 'Psicologia',      585.90, 'Aracaju'),
('Faculdade Pio Décimo', 'Direito',         575.60, 'Aracaju'),
('Faculdade Pio Décimo', 'Fisioterapia',    560.80, 'Aracaju'),
('Faculdade Pio Décimo', 'Enfermagem',      545.20, 'Aracaju'),
('Faculdade Pio Décimo', 'Biomedicina',     540.10, 'Aracaju'),
('Faculdade Pio Décimo', 'Farmácia',        535.70, 'Aracaju'),
('Faculdade Pio Décimo', 'Nutrição',        520.40, 'Aracaju'),
('Faculdade Pio Décimo', 'Administração',   480.50, 'Aracaju'),
-- Estácio Sergipe
('Estácio Sergipe', 'Direito',                  540.30, 'Aracaju'),
('Estácio Sergipe', 'Psicologia',               530.20, 'Aracaju'),
('Estácio Sergipe', 'Arquitetura e Urbanismo',  520.70, 'Aracaju'),
('Estácio Sergipe', 'Fisioterapia',             510.30, 'Aracaju'),
('Estácio Sergipe', 'Engenharia Civil',         500.60, 'Aracaju'),
('Estácio Sergipe', 'Enfermagem',               495.40, 'Aracaju'),
('Estácio Sergipe', 'Educação Física',          470.90, 'Aracaju'),
('Estácio Sergipe', 'Administração',            465.80, 'Aracaju'),
('Estácio Sergipe', 'Ciências Contábeis',       455.20, 'Aracaju'),
('Estácio Sergipe', 'Pedagogia',                450.10, 'Aracaju'),
-- Faculdade São Luís de França
('Faculdade São Luís de França', 'Direito',               555.90, 'Aracaju'),
('Faculdade São Luís de França', 'Psicologia',            545.30, 'Aracaju'),
('Faculdade São Luís de França', 'Fisioterapia',          520.60, 'Aracaju'),
('Faculdade São Luís de França', 'Farmácia',              515.90, 'Aracaju'),
('Faculdade São Luís de França', 'Engenharia Civil',      510.20, 'Aracaju'),
('Faculdade São Luís de França', 'Enfermagem',            505.80, 'Aracaju'),
('Faculdade São Luís de França', 'Nutrição',              500.40, 'Aracaju'),
('Faculdade São Luís de França', 'Educação Física',       475.30, 'Aracaju'),
('Faculdade São Luís de França', 'Administração',         470.40, 'Aracaju'),
('Faculdade São Luís de França', 'Ciências Contábeis',    460.70, 'Aracaju'),
-- Faculdade Atlântico
('Faculdade Atlântico', 'Direito',                                  535.40, 'Aracaju'),
('Faculdade Atlântico', 'Psicologia',                               525.70, 'Aracaju'),
('Faculdade Atlântico', 'Engenharia Civil',                         498.50, 'Aracaju'),
('Faculdade Atlântico', 'Enfermagem',                               490.20, 'Aracaju'),
('Faculdade Atlântico', 'Análise e Desenvolvimento de Sistemas',    470.60, 'Aracaju'),
('Faculdade Atlântico', 'Administração',                            455.60, 'Aracaju'),
('Faculdade Atlântico', 'Ciências Contábeis',                       450.30, 'Aracaju'),
('Faculdade Atlântico', 'Marketing',                                448.20, 'Aracaju'),
('Faculdade Atlântico', 'Pedagogia',                                445.80, 'Aracaju'),
('Faculdade Atlântico', 'Gestão de Recursos Humanos',               440.90, 'Aracaju'),
-- Uninassau Aracaju
('Uninassau Aracaju', 'Odontologia',        600.40, 'Aracaju'),
('Uninassau Aracaju', 'Direito',            545.10, 'Aracaju'),
('Uninassau Aracaju', 'Psicologia',         535.80, 'Aracaju'),
('Uninassau Aracaju', 'Fisioterapia',       515.50, 'Aracaju'),
('Uninassau Aracaju', 'Biomedicina',        510.80, 'Aracaju'),
('Uninassau Aracaju', 'Engenharia Civil',   505.40, 'Aracaju'),
('Uninassau Aracaju', 'Enfermagem',         500.90, 'Aracaju'),
('Uninassau Aracaju', 'Nutrição',           495.60, 'Aracaju'),
('Uninassau Aracaju', 'Administração',      462.30, 'Aracaju'),
('Uninassau Aracaju', 'Ciências Contábeis', 452.40, 'Aracaju'),
-- Faculdade Amadeus
('Faculdade Amadeus', 'Direito',                                    530.20, 'Aracaju'),
('Faculdade Amadeus', 'Psicologia',                                 520.40, 'Aracaju'),
('Faculdade Amadeus', 'Enfermagem',                                 488.60, 'Aracaju'),
('Faculdade Amadeus', 'Fisioterapia',                               495.30, 'Aracaju'),
('Faculdade Amadeus', 'Engenharia Civil',                           492.10, 'Aracaju'),
('Faculdade Amadeus', 'Análise e Desenvolvimento de Sistemas',      465.40, 'Aracaju'),
('Faculdade Amadeus', 'Administração',                              452.80, 'Aracaju'),
('Faculdade Amadeus', 'Ciências Contábeis',                         446.50, 'Aracaju'),
('Faculdade Amadeus', 'Pedagogia',                                  440.20, 'Aracaju'),
('Faculdade Amadeus', 'Educação Física',                            468.70, 'Aracaju');
