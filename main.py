import requests
import logging
from enum import Enum
from flask import Flask, jsonify, abort

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define a simple Enum for testing
class ChainDefillama(Enum):
    ETHEREUM = "Ethereum"
    SOLANA = "Solana"
    NEAR = "Near"
    BITCOIN = "Bitcoin"
    SUI = "Sui"
    APTOS = "Aptos"
    ARBITRUM = "Arbitrum"
    SEI = "Sei"
    BASE = "Base"
    BSC = "BSC"
    POLYGON = "Polygon"
    OPTIMISM = "Optimism"
    FANTOM = "Fantom"
    AVALANCHE = "Avalanche"
    CELO = "Celo"

    @classmethod
    def from_string(cls, value: str):
        for item in cls:
            # Case-insensitive matching
            if item.value.lower() == value.lower():
                return item
        return None 


class DefillamaService:
    def __init__(self):
        self.base_url = "https://api.llama.fi"
        self.stablecoins_url = "https://stablecoins.llama.fi"

    def _make_request(self, url):
        logger.info(f"Requesting URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Response Status Code: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            # Abort with an error code that Flask can handle
            abort(503, description=f"Upstream API error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            abort(500, description="Internal server error")


    def get_historical_chain_tvl(self, chain_value: str):
        url = f"{self.base_url}/v2/historicalChainTvl/{chain_value}"
        return self._make_request(url)

    def get_stable_coins_charts(self, chain_value: str):
        url = f"{self.stablecoins_url}/stablecoincharts/{chain_value}"
        return self._make_request(url)

    def get_overview_dexs(self, chain_value: str):
        url = f"{self.base_url}/overview/dexs/{chain_value}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyVolume"
        return self._make_request(url)

    def get_overview_fees(self, chain_value: str):
        url = f"{self.base_url}/overview/fees/{chain_value}?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false&dataType=dailyFees"
        return self._make_request(url)

# --- Flask App Setup ---
app = Flask(__name__)
defillama_service = DefillamaService()

@app.route('/')
def index():
    # Provide basic instructions or list available endpoints
    available_chains = [chain.value for chain in ChainDefillama]
    return jsonify({
        "message": "Defillama API Wrapper",
        "available_chains": available_chains,
        "endpoints": {
            "/tvl/<chain_name>": "Get historical TVL for a chain.",
            "/stablecoins/<chain_name>": "Get stablecoin charts for a chain.",
            "/dexs/<chain_name>": "Get DEX overview for a chain.",
            "/fees/<chain_name>": "Get fees overview for a chain."
        }
    })

@app.route('/tvl/<string:chain_name>')
def get_tvl(chain_name: str):
    logger.info(f"Received request for TVL for chain: {chain_name}")
    # chain = ChainDefillama.from_string(chain_name)
    # if not chain:
    #     abort(404, description=f"Chain '{chain_name}' not found or not supported.")
    # Use chain_name directly as Defillama API uses the string identifier
    data = defillama_service.get_historical_chain_tvl(chain_name)
    return jsonify(data)

@app.route('/stablecoins/<string:chain_name>')
def get_stablecoins(chain_name: str):
    logger.info(f"Received request for Stablecoins for chain: {chain_name}")
    # chain = ChainDefillama.from_string(chain_name)
    # if not chain:
    #     abort(404, description=f"Chain '{chain_name}' not found or not supported.")
    data = defillama_service.get_stable_coins_charts(chain_name)
    return jsonify(data)

@app.route('/dexs/<string:chain_name>')
def get_dexs(chain_name: str):
    logger.info(f"Received request for DEXs for chain: {chain_name}")
    # chain = ChainDefillama.from_string(chain_name)
    # if not chain:
    #     abort(404, description=f"Chain '{chain_name}' not found or not supported.")
    data = defillama_service.get_overview_dexs(chain_name)
    return jsonify(data)

@app.route('/fees/<string:chain_name>')
def get_fees(chain_name: str):
    logger.info(f"Received request for Fees for chain: {chain_name}")
    # chain = ChainDefillama.from_string(chain_name)
    # if not chain:
    #     abort(404, description=f"Chain '{chain_name}' not found or not supported.")
    data = defillama_service.get_overview_fees(chain_name)
    return jsonify(data)


if __name__ == "__main__":
    logger.info("Starting Flask server for Defillama API...")
    # Run in debug mode for development, host='0.0.0.0' to be accessible externally (like from Docker host)
    pass