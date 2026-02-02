from backend.app.core.logging import get_logger
from backend.app.db.postgres import PostgresDBConnection

logger = get_logger(__name__, system_type='backend')


class PGVectorDBConnection:
    @staticmethod
    def get_pgvector_connection():
        try:
            logger.info('connection successfully')
            return PostgresDBConnection.get_pg_connection()
        except Exception as e:
            logger.error(f'connection error: {e}')
            raise
