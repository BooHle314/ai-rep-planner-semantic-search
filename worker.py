"""
Background Worker - Asynchronous processing with modular services
"""
import time
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Import modular services
from services.data_loader import DataLoader
from services.semantic_search import SemanticSearchService
from services.geocoding import HybridGeocoder
from services.route_optimizer import RouteOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackgroundWorker:
    """
    Modular background worker for async processing
    Demonstrates separation of concerns and async communication
    """
    
    def __init__(self, data_dir: str = "data", cache_dir: str = "cache"):
        self.data_dir = Path(data_dir)
        self.cache_dir = Path(cache_dir)
        
        # Initialize modular services
        self.data_loader = DataLoader(data_dir)
        self.search_service = SemanticSearchService(cache_dir=cache_dir)
        self.geocoder = HybridGeocoder(use_cache=True, cache_dir=cache_dir)
        self.route_optimizer = RouteOptimizer()
        
        self.is_ready = False
        self.metrics = {
            'start_time': datetime.now().isoformat(),
            'tasks_completed': 0,
            'last_error': None
        }
    
    def initialize(self) -> bool:
        """Initialize all services"""
        try:
            logger.info("🚀 Initializing background worker...")
            
            # 1. Load data
            logger.info("📂 Loading customer data...")
            customers_df = self.data_loader.load_customers()
            
            # 2. Prepare semantic search
            logger.info("🧠 Preparing semantic search...")
            self.search_service.prepare_embeddings(customers_df)
            
            # 3. Geocode addresses (optional - can run in background)
            logger.info("📍 Geocoding addresses...")
            geocoded_df = self.geocoder.geocode_dataframe(customers_df)
            
            # Save geocoded data
            output_path = self.data_dir / "customers_geocoded.xlsx"
            geocoded_df.to_excel(output_path, index=False)
            logger.info(f"💾 Saved geocoded data to: {output_path}")
            
            self.is_ready = True
            self.metrics['initialization_complete'] = datetime.now().isoformat()
            self.metrics['customers_loaded'] = len(customers_df)
            self.metrics['geocoded_count'] = len(geocoded_df)
            
            logger.info("✅ Background worker initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            self.metrics['last_error'] = str(e)
            return False
    
    def process_embeddings(self, force_rebuild: bool = False) -> bool:
        """Process embeddings in background"""
        try:
            logger.info("Processing embeddings...")
            customers_df = self.data_loader.load_customers()
            success = self.search_service.prepare_embeddings(customers_df, force_rebuild)
            
            if success:
                self.metrics['tasks_completed'] += 1
                logger.info("✅ Embeddings processed successfully")
            else:
                logger.warning("⚠️ Embeddings processing may have issues")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error processing embeddings: {e}")
            return False
    
    def geocode_addresses(self, batch_size: int = 100) -> Dict:
        """Geocode addresses in background batches"""
        try:
            logger.info(f"Geocoding addresses (batch size: {batch_size})...")
            
            customers_df = self.data_loader.load_customers()
            geocoded_df = self.geocoder.geocode_dataframe(customers_df)
            
            # Save results
            output_path = self.data_dir / "customers_geocoded.xlsx"
            geocoded_df.to_excel(output_path, index=False)
            
            metrics = self.geocoder.get_metrics()
            self.metrics['tasks_completed'] += 1
            self.metrics['geocoding_metrics'] = metrics
            
            logger.info(f"✅ Geocoded {len(geocoded_df)} addresses")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error geocoding: {e}")
            return {'error': str(e)}
    
    def optimize_sample_route(self) -> Dict:
        """Optimize a sample route for demonstration"""
        try:
            logger.info("Optimizing sample route...")
            
            # Load data
            customers_df = self.data_loader.load_customers()
            
            # Filter for a specific rep
            if 'rep_id' in customers_df.columns:
                sample_rep = customers_df['rep_id'].iloc[0]
                rep_customers = customers_df[customers_df['rep_id'] == sample_rep].head(10)
            else:
                rep_customers = customers_df.head(10)
            
            # Add dummy coordinates for demo
            import numpy as np
            rep_customers = rep_customers.copy()
            rep_customers['latitude'] = 40.7 + np.random.uniform(-0.1, 0.1, len(rep_customers))
            rep_customers['longitude'] = -74.0 + np.random.uniform(-0.1, 0.1, len(rep_customers))
            
            # Optimize route
            start_location = (40.7128, -74.0060)  # NYC
            end_location = (40.7580, -73.9855)    # Times Square
            
            route_result = self.route_optimizer.optimize_route(
                customers_df=rep_customers,
                start_location=start_location,
                end_location=end_location,
                start_time="09:00"
            )
            
            self.metrics['tasks_completed'] += 1
            
            logger.info("✅ Sample route optimized")
            return {
                'success': True,
                'customers_in_route': len(rep_customers),
                'route_available': route_result is not None
            }
            
        except Exception as e:
            logger.error(f"❌ Error optimizing route: {e}")
            return {'error': str(e)}
    
    def get_status(self) -> Dict:
        """Get worker status and metrics"""
        status = {
            'is_ready': self.is_ready,
            'metrics': self.metrics,
            'services': {
                'data_loader': 'initialized',
                'semantic_search': 'initialized' if self.search_service.customer_data is not None else 'pending',
                'geocoder': 'initialized',
                'route_optimizer': 'initialized'
            }
        }
        
        # Add search service metrics if available
        if self.search_service.customer_data is not None:
            status['search_metrics'] = self.search_service.get_metrics()
        
        # Add geocoder metrics if available
        status['geocoding_metrics'] = self.geocoder.get_metrics()
        
        return status

def main():
    """Main entry point for background worker"""
    logger.info("Starting background worker...")
    
    worker = BackgroundWorker()
    
    # Initialize services
    if not worker.initialize():
        logger.error("Failed to initialize worker")
        return
    
    # Run background tasks
    logger.info("Running background tasks...")
    
    # Task 1: Process embeddings (if not already done)
    worker.process_embeddings()
    
    # Task 2: Geocode addresses
    worker.geocode_addresses()
    
    # Task 3: Optimize sample route
    worker.optimize_sample_route()
    
    # Display status
    status = worker.get_status()
    logger.info(f"Worker status: {status}")
    
    logger.info("✅ Background worker ready")
    
    # Keep running to simulate background processing
    try:
        while True:
            time.sleep(60)  # Sleep for 1 minute
            logger.debug("Background worker still running...")
    except KeyboardInterrupt:
        logger.info("Shutting down background worker...")

if __name__ == "__main__":
    main()
