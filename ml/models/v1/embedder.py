from sentence_transformers import SentenceTransformer
from backend.app.core.logging import get_logger

logger = get_logger(__name__, system_type='ml')


class Model():
    _model = None

    @staticmethod
    def model():
        if Model._model is None:
            try:
                Model._model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info('loading successfully')
            except Exception as e:
                logger.error(f'error: {e}')

        return Model._model
