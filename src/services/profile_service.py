from src.repositories.postgres_repository import PostgresRepository


class ProfileService:
    def __init__(self):
        self.postgres = PostgresRepository()

    def completar_perfil(self, payload):
        query = f"""
        UPDATE usuarios
        SET nome = '{payload.get('nome')}',
        telefone = '{payload.get('telefone')}',
        ie_primeiro_login = false
        WHERE login = '{payload.get('login')}';
        """

        try:
            self.postgres.execute_query(query, commit=True)
            return {
                "Status": "Perfil Completado"
            }
        except Exception as e:
            return {
                "Status": "Erro ao completar perfil",
                "Motivo": str(e)
            }
