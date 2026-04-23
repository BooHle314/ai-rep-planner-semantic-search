"""
Simple background worker with error handling
"""
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting simple background worker...")
    
    try:
        # Try to import services
        sys.path.append('services')
        
        from data_loader import DataLoader
        logger.info("✅ DataLoader imported")
        
        from semantic_search import SemanticSearchService
        logger.info("✅ SemanticSearchService imported")
        
        # Initialize services
        data_loader = DataLoader()
        search_service = SemanticSearchService()
        
        # Load data
        logger.info("Loading data...")
        try:
            df = data_loader.load_customers()
            logger.info(f"✅ Loaded {len(df)} customers")
            
            # Prepare embeddings
            logger.info("Preparing embeddings...")
            success = search_service.prepare_embeddings(df)
            if success:
                logger.info("✅ Embeddings prepared successfully")
            else:
                logger.warning("⚠️ Embeddings preparation had issues")
                
        except Exception as e:
            logger.error(f"❌ Data processing error: {e}")
        
        # Keep running
        logger.info("✅ Worker ready and running")
        while True:
            time.sleep(60)
            logger.debug("Worker still running...")
            
    except KeyboardInterrupt:
        logger.info("Shutting down worker...")
    except Exception as e:
        logger.error(f"❌ Worker failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
