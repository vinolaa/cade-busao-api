from src.repositories.postgres_repository import PostgresRepository


class AuthService:
    def __init__(self):
        self.postgres = PostgresRepository()

    def login(self, login, senha):
        query = f"""
        SELECT
            login,
            email,
            nome,
            tipo_usuario,
            ie_primeiro_login
        FROM usuarios
        WHERE login = '{login}'
        """.format(login=login)
        cursor = self.postgres.execute_query(query)
        usuario = cursor.fetchone()

        if usuario:
            pw_query = f"""
            SELECT
                crypt('{senha}', senha) = senha
            AS password_match
            FROM usuarios
            WHERE login = '{login}';
            """.format(senha=senha, login=login)
            cursor = self.postgres.execute_query(pw_query)
            match = cursor.fetchone()[0]
            if match:
                return {
                    "Status": "Acesso Liberado",
                    "Usuário": usuario
                }
            else:
                return {
                    "Status": "Acesso Negado",
                    "Motivo": "Senha incorreta"
                }
        else:
            return {
                "Status": "Acesso Negado",
                "Motivo": "Usuário não encontrado"
            }

    def register(self, login, senha, c_senha, email):
        if senha != c_senha:
            return {
                "Status": "Erro ao cadastrar usuário",
                "Motivo": "As senhas não coincidem"
            }

        query = f"""
        INSERT INTO usuarios (login, senha, email, tipo_usuario, dt_cadastro)
        VALUES ('{login}', crypt('{senha}', gen_salt('bf')), '{email}', 'U', 
        NOW() at time zone 'America/Sao_Paulo');
        """

        try:
            self.postgres.execute_query(query, commit=True)
            return {
                "Status": "Usuário cadastrado com sucesso"
            }
        except Exception as e:
            return {
                "Status": "Erro ao cadastrar usuário",
                "Motivo": str(e)
            }
