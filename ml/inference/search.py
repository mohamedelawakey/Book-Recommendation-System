from backend.app.core.logging import get_logger
from ml.Enum.Enumerations import Enumerations
from ml.services.vector_service import VectorService
from ml.services.metadata_service import MetadataService
from ml.pipeline.v1.embed import Embedder
from typing import Any, List, Dict

logger = get_logger(__name__, system_type='ml')


class Search:
    @staticmethod
    def search(
        user_text: str,
        top_k: int = Enumerations.top_k
    ) -> List[Dict[str, Any]]:
        try:
            embed_result = Embedder.embedder(user_text)
            query_embedding = embed_result.get("name_embeddings")

            if not query_embedding:
                logger.warning("Search: empty embedding returned")
                return []

            vector_results = VectorService.search_similar_books(
                query_embedding=query_embedding,
                top_k=top_k
            )

            if not vector_results:
                logger.warning("Search: no vector results found")
                return []

            book_ids = [item["book_id"] for item in vector_results]

            metadata_results = MetadataService.get_books_metadata(book_ids)

            similarity_map = {
                item["book_id"]: item["similarity"]
                for item in vector_results
            }

            for book in metadata_results:
                book["similarity"] = similarity_map.get(book["book_id"], 0.0)

            logger.info(f"Search: returning {len(metadata_results)} books")
            return metadata_results

        except Exception as e:
            logger.error(f"Search error: {e}", exc_info=True)
            return []
