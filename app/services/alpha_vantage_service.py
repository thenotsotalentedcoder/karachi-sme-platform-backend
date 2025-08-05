"""Alpha Vantage service for real-time market data and sector performance."""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache

from app.config import settings

logger = logging.getLogger(__name__)


class AlphaVantageService:
    """Service for fetching market data from Alpha Vantage API."""
    
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.base_url = settings.ALPHA_VANTAGE_BASE_URL
        self.rate_limit = settings.ALPHA_VANTAGE_RATE_LIMIT
        self._last_request_time = 0
    
    async def _make_request(self, function: str, **params) -> Dict[str, Any]:
        """Make rate-limited request to Alpha Vantage API."""
        
        # Rate limiting - max 5 requests per minute
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < 12:  # 12 seconds between requests for 5/minute
            await asyncio.sleep(12 - time_since_last)
        
        params.update({
            "function": function,
            "apikey": self.api_key
        })
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                self._last_request_time = asyncio.get_event_loop().time()
                data = response.json()
                
                # Check for API error messages
                if "Error Message" in data:
                    raise Exception(f"Alpha Vantage error: {data['Error Message']}")
                
                if "Note" in data:
                    raise Exception(f"Alpha Vantage rate limit: {data['Note']}")
                
                return data
                
        except httpx.TimeoutException:
            logger.error("Alpha Vantage API timeout")
            raise Exception("Alpha Vantage API request timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"Alpha Vantage API HTTP error: {e.response.status_code}")
            raise Exception(f"Alpha Vantage API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Alpha Vantage API error: {str(e)}")
            raise
    
    async def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview and major indices."""
        
        logger.info("Fetching market overview from Alpha Vantage")
        
        try:
            # Get major market indices
            indices_tasks = [
                self._get_index_data("SPY"),   # S&P 500
                self._get_index_data("QQQ"),   # NASDAQ
                self._get_index_data("DIA"),   # Dow Jones
                self._get_index_data("IWM"),   # Russell 2000 (small cap)
                self._get_index_data("VTI"),   # Total Stock Market
            ]
            
            indices_results = await asyncio.gather(*indices_tasks, return_exceptions=True)
            
            # Process results
            market_data = {
                "sp500": None,
                "nasdaq": None,
                "dow_jones": None,
                "russell_2000": None,
                "total_market": None,
                "market_sentiment": "neutral",
                "volatility_index": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            index_names = ["sp500", "nasdaq", "dow_jones", "russell_2000", "total_market"]
            
            for i, result in enumerate(indices_results):
                if not isinstance(result, Exception) and result:
                    market_data[index_names[i]] = result
            
            # Calculate market sentiment
            market_data["market_sentiment"] = self._calculate_market_sentiment(market_data)
            market_data["market_health_score"] = self._calculate_market_health_score(market_data)
            
            return market_data
            
        except Exception as e:
            logger.error(f"Failed to get market overview: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_index_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific index/ETF."""
        
        try:
            data = await self._make_request("GLOBAL_QUOTE", symbol=symbol)
            
            global_quote = data.get("Global Quote", {})
            if not global_quote:
                return None
            
            return {
                "symbol": global_quote.get("01. symbol"),
                "price": float(global_quote.get("05. price", 0)),
                "change": float(global_quote.get("09. change", 0)),
                "change_percent": global_quote.get("10. change percent", "0%").replace("%", ""),
                "volume": int(global_quote.get("06. volume", 0)),
                "previous_close": float(global_quote.get("08. previous close", 0)),
                "last_updated": global_quote.get("07. latest trading day")
            }
            
        except Exception as e:
            logger.warning(f"Failed to get data for {symbol}: {str(e)}")
            return None
    
    async def get_sector_performance(self, sector: str) -> Dict[str, Any]:
        """Get sector-specific performance data."""
        
        logger.info(f"Fetching sector performance for {sector}")
        
        try:
            # Get sector performance overview
            sector_data = await self._make_request("SECTOR")
            
            # Get sector-specific ETFs
            sector_etfs = self._get_sector_etf_mapping()
            sector_etf = sector_etfs.get(sector.lower())
            
            sector_etf_data = None
            if sector_etf:
                sector_etf_data = await self._get_index_data(sector_etf)
            
            # Process sector performance data
            if "Rank A: Real-Time Performance" in sector_data:
                realtime_performance = sector_data["Rank A: Real-Time Performance"]
                
                sector_performance = {
                    "sector": sector,
                    "etf_data": sector_etf_data,
                    "sector_rankings": self._process_sector_rankings(realtime_performance),
                    "relative_performance": self._calculate_sector_relative_performance(
                        realtime_performance, sector
                    ),
                    "timestamp": datetime.now().isoformat()
                }
                
                return sector_performance
            
            return {"error": "No sector data available", "timestamp": datetime.now().isoformat()}
            
        except Exception as e:
            logger.error(f"Failed to get sector performance for {sector}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _get_sector_etf_mapping(self) -> Dict[str, str]:
        """Map business sectors to relevant ETFs."""
        return {
            "electronics": "XLK",        # Technology Select Sector SPDR
            "technology": "XLK",
            "food": "XLP",               # Consumer Staples Select Sector SPDR
            "retail": "XLY",             # Consumer Discretionary Select Sector SPDR
            "auto": "XLI",               # Industrial Select Sector SPDR
            "automotive": "XLI",
            "manufacturing": "XLI",
            "healthcare": "XLV",         # Health Care Select Sector SPDR
            "finance": "XLF",            # Financial Select Sector SPDR
            "energy": "XLE",             # Energy Select Sector SPDR
            "utilities": "XLU",          # Utilities Select Sector SPDR
            "real_estate": "XLRE",       # Real Estate Select Sector SPDR
            "materials": "XLB",          # Materials Select Sector SPDR
            "communication": "XLC"       # Communication Services Select Sector SPDR
        }
    
    def _process_sector_rankings(self, sector_data: Dict[str, str]) -> Dict[str, float]:
        """Process sector ranking data."""
        processed_rankings = {}
        
        for sector_name, performance_str in sector_data.items():
            try:
                # Extract percentage from string like "+1.23%"
                performance_str = performance_str.replace("%", "").replace("+", "")
                performance = float(performance_str)
                processed_rankings[sector_name.lower().replace(" ", "_")] = performance
            except (ValueError, AttributeError):
                continue
        
        return processed_rankings
    
    def _calculate_sector_relative_performance(self, sector_data: Dict[str, str], target_sector: str) -> Dict[str, Any]:
        """Calculate how target sector performs relative to others."""
        
        sector_mapping = {
            "electronics": "Information Technology",
            "technology": "Information Technology", 
            "food": "Consumer Staples",
            "retail": "Consumer Discretionary",
            "auto": "Industrials",
            "automotive": "Industrials",
            "manufacturing": "Industrials"
        }
        
        mapped_sector = sector_mapping.get(target_sector.lower(), "Information Technology")
        
        processed_rankings = self._process_sector_rankings(sector_data)
        
        if mapped_sector.lower().replace(" ", "_") in processed_rankings:
            sector_performance = processed_rankings[mapped_sector.lower().replace(" ", "_")]
            
            # Calculate percentile rank
            all_performances = list(processed_rankings.values())
            all_performances.sort()
            
            rank = all_performances.index(sector_performance) + 1
            percentile = (rank / len(all_performances)) * 100
            
            return {
                "sector_performance": sector_performance,
                "percentile_rank": percentile,
                "relative_strength": "strong" if percentile > 70 else "weak" if percentile < 30 else "average",
                "outperforming_sectors": sum(1 for p in all_performances if p < sector_performance),
                "total_sectors": len(all_performances)
                    }
       
        return {"error": "Sector data not found"}
   
    def _calculate_market_sentiment(self, market_data: Dict[str, Any]) -> str:
        """Calculate overall market sentiment based on indices performance."""
        
        try:
            positive_count = 0
            negative_count = 0
            total_count = 0
            
            indices = ["sp500", "nasdaq", "dow_jones", "russell_2000", "total_market"]
            
            for index_name in indices:
                index_data = market_data.get(index_name)
                if index_data and isinstance(index_data, dict):
                    change_percent_str = index_data.get("change_percent", "0")
                    try:
                        change_percent = float(change_percent_str.replace("%", ""))
                        total_count += 1
                        
                        if change_percent > 0.5:
                            positive_count += 1
                        elif change_percent < -0.5:
                            negative_count += 1
                    except (ValueError, AttributeError):
                        continue
                       
            if total_count == 0:
                return "neutral"
            
            positive_ratio = positive_count / total_count
            negative_ratio = negative_count / total_count
            
            if positive_ratio >= 0.6:
                return "bullish"
            elif negative_ratio >= 0.6:
                return "bearish"
            elif positive_ratio > negative_ratio:
                return "cautiously_optimistic"
            elif negative_ratio > positive_ratio:
                return "cautiously_pessimistic"
            else:
                return "neutral"
                
        except Exception:
            return "neutral"
    
    def _calculate_market_health_score(self, market_data: Dict[str, Any]) -> float:
        """Calculate market health score (0-100)."""
        
        try:
            score = 50  # Baseline
            weight_per_index = 10
            
            indices = ["sp500", "nasdaq", "dow_jones", "russell_2000", "total_market"]
            
            for index_name in indices:
                index_data = market_data.get(index_name)
                if index_data and isinstance(index_data, dict):
                    try:
                        change_percent_str = index_data.get("change_percent", "0")
                        change_percent = float(change_percent_str.replace("%", ""))
                        
                        # Add points for positive performance, subtract for negative
                        score += min(weight_per_index, max(-weight_per_index, change_percent * 2))
                        
                    except (ValueError, AttributeError):
                        continue
                       
            return max(0, min(100, score))
            
        except Exception:
            return 50
    
    async def get_economic_indicators(self) -> Dict[str, Any]:
        """Get key economic indicators from Alpha Vantage."""
        
        logger.info("Fetching economic indicators from Alpha Vantage")
        
        try:
            # Get key economic indicators
            indicators_tasks = [
                self._get_economic_indicator("REAL_GDP"),
                self._get_economic_indicator("UNEMPLOYMENT"),
                self._get_economic_indicator("INFLATION"),
                self._get_economic_indicator("RETAIL_SALES"),
                self._get_economic_indicator("CONSUMER_SENTIMENT")
            ]
            
            results = await asyncio.gather(*indicators_tasks, return_exceptions=True)
            
            indicators = {
                "gdp": None,
                "unemployment": None,
                "inflation": None,
                "retail_sales": None,
                "consumer_sentiment": None,
                "timestamp": datetime.now().isoformat()
            }
            
            indicator_names = ["gdp", "unemployment", "inflation", "retail_sales", "consumer_sentiment"]
            
            for i, result in enumerate(results):
                if not isinstance(result, Exception) and result:
                    indicators[indicator_names[i]] = result
            
            return indicators
            
        except Exception as e:
            logger.error(f"Failed to get economic indicators: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_economic_indicator(self, indicator: str) -> Optional[Dict[str, Any]]:
        """Get specific economic indicator data."""
        
        try:
            data = await self._make_request(indicator, interval="annual")
            
            if "data" in data and len(data["data"]) > 0:
                latest_data = data["data"][0]
                return {
                    "indicator": indicator,
                    "value": latest_data.get("value"),
                    "date": latest_data.get("date"),
                    "unit": data.get("unit")
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get {indicator}: {str(e)}")
            return None
    
    async def get_currency_data(self) -> Dict[str, Any]:
        """Get USD currency exchange rates."""
        
        logger.info("Fetching currency data")
        
        try:
            # Get major currency pairs
            currency_tasks = [
                self._get_fx_rate("EUR", "USD"),
                self._get_fx_rate("GBP", "USD"),
                self._get_fx_rate("JPY", "USD"),
                self._get_fx_rate("CAD", "USD"),
                self._get_fx_rate("AUD", "USD")
            ]
            
            results = await asyncio.gather(*currency_tasks, return_exceptions=True)
            
            currency_data = {
                "eur_usd": None,
                "gbp_usd": None,
                "jpy_usd": None,
                "cad_usd": None,
                "aud_usd": None,
                "usd_strength_index": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            currency_names = ["eur_usd", "gbp_usd", "jpy_usd", "cad_usd", "aud_usd"]
            
            for i, result in enumerate(results):
                if not isinstance(result, Exception) and result:
                    currency_data[currency_names[i]] = result
            
            # Calculate USD strength index
            currency_data["usd_strength_index"] = self._calculate_usd_strength(currency_data)
            
            return currency_data
            
        except Exception as e:
            logger.error(f"Failed to get currency data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_fx_rate(self, from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        """Get foreign exchange rate between two currencies."""
        
        try:
            data = await self._make_request(
                "FX_DAILY",
                from_symbol=from_currency,
                to_symbol=to_currency
            )
            
            time_series_key = f"Time Series FX (Daily)"
            if time_series_key in data:
                time_series = data[time_series_key]
                latest_date = max(time_series.keys())
                latest_data = time_series[latest_date]
                
                return {
                    "pair": f"{from_currency}/{to_currency}",
                    "rate": float(latest_data.get("4. close", 0)),
                    "change": float(latest_data.get("4. close", 0)) - float(latest_data.get("1. open", 0)),
                    "high": float(latest_data.get("2. high", 0)),
                    "low": float(latest_data.get("3. low", 0)),
                    "date": latest_date
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get {from_currency}/{to_currency} rate: {str(e)}")
            return None
    
    def _calculate_usd_strength(self, currency_data: Dict[str, Any]) -> float:
        """Calculate USD strength index based on major currency pairs."""
        
        try:
            # This is a simplified USD strength calculation
            # In reality, you'd use the DXY index or weighted basket
            
            strength_score = 100  # Baseline
            pairs_data = []
            
            for pair_name in ["eur_usd", "gbp_usd", "aud_usd", "cad_usd"]:
                pair_data = currency_data.get(pair_name)
                if pair_data and isinstance(pair_data, dict):
                    try:
                        rate = pair_data.get("rate", 1.0)
                        change = pair_data.get("change", 0)
                        
                        # Negative change in these pairs means USD strengthening
                        pairs_data.append(-change)
                    except (ValueError, TypeError):
                        continue
                       
            if pairs_data:
                avg_change = sum(pairs_data) / len(pairs_data)
                strength_score += avg_change * 1000  # Scale the change
            
            return max(0, min(200, strength_score))
            
        except Exception:
            return 100
    
    async def get_commodity_data(self) -> Dict[str, Any]:
        """Get commodity prices relevant to businesses."""
        
        logger.info("Fetching commodity data")
        
        try:
            # Get key commodity data
            commodity_tasks = [
                self._get_commodity_price("WTI"),   # Oil
                self._get_commodity_price("BRENT"), # Brent Oil
                self._get_commodity_price("NATURAL_GAS"),
                self._get_commodity_price("COPPER"),
                self._get_commodity_price("ALUMINUM")
            ]
            
            results = await asyncio.gather(*commodity_tasks, return_exceptions=True)
            
            commodity_data = {
                "oil_wti": None,
                "oil_brent": None,
                "natural_gas": None,
                "copper": None,
                "aluminum": None,
                "energy_cost_index": 0,
                "materials_cost_index": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            commodity_names = ["oil_wti", "oil_brent", "natural_gas", "copper", "aluminum"]
            
            for i, result in enumerate(results):
                if not isinstance(result, Exception) and result:
                    commodity_data[commodity_names[i]] = result
            
            # Calculate cost indices
            commodity_data["energy_cost_index"] = self._calculate_energy_cost_index(commodity_data)
            commodity_data["materials_cost_index"] = self._calculate_materials_cost_index(commodity_data)
            
            return commodity_data
            
        except Exception as e:
            logger.error(f"Failed to get commodity data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_commodity_price(self, commodity: str) -> Optional[Dict[str, Any]]:
        """Get price data for specific commodity."""
        
        try:
            data = await self._make_request(commodity, interval="daily")
            
            if "data" in data and len(data["data"]) > 0:
                latest_data = data["data"][0]
                previous_data = data["data"][1] if len(data["data"]) > 1 else latest_data
                
                current_price = float(latest_data.get("value", 0))
                previous_price = float(previous_data.get("value", current_price))
                
                return {
                    "commodity": commodity,
                    "price": current_price,
                    "change": current_price - previous_price,
                    "change_percent": ((current_price - previous_price) / previous_price * 100) if previous_price > 0 else 0,
                    "date": latest_data.get("date"),
                    "unit": data.get("unit")
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get {commodity} price: {str(e)}")
            return None
    
    def _calculate_energy_cost_index(self, commodity_data: Dict[str, Any]) -> float:
        """Calculate energy cost index for businesses."""
        
        try:
            index = 100  # Baseline
            
            # Weight different energy sources
            oil_data = commodity_data.get("oil_wti")
            gas_data = commodity_data.get("natural_gas")
            
            if oil_data and isinstance(oil_data, dict):
                oil_change = oil_data.get("change_percent", 0)
                index += oil_change * 0.6  # 60% weight for oil
            
            if gas_data and isinstance(gas_data, dict):
                gas_change = gas_data.get("change_percent", 0)
                index += gas_change * 0.4  # 40% weight for natural gas
            
            return max(0, index)
            
        except Exception:
            return 100
    
    def _calculate_materials_cost_index(self, commodity_data: Dict[str, Any]) -> float:
        """Calculate materials cost index for businesses."""
        
        try:
            index = 100  # Baseline
            
            copper_data = commodity_data.get("copper")
            aluminum_data = commodity_data.get("aluminum")
            
            if copper_data and isinstance(copper_data, dict):
                copper_change = copper_data.get("change_percent", 0)
                index += copper_change * 0.5  # 50% weight for copper
            
            if aluminum_data and isinstance(aluminum_data, dict):
                aluminum_change = aluminum_data.get("change_percent", 0)
                index += aluminum_change * 0.5  # 50% weight for aluminum
            
            return max(0, index)
            
        except Exception:
            return 100
    
    @lru_cache(maxsize=16)
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote for a symbol."""
        
        try:
            data = await self._make_request("GLOBAL_QUOTE", symbol=symbol)
            
            global_quote = data.get("Global Quote", {})
            if not global_quote:
                return {"error": f"No data available for {symbol}"}
            
            return {
                "symbol": global_quote.get("01. symbol"),
                "price": float(global_quote.get("05. price", 0)),
                "change": float(global_quote.get("09. change", 0)),
                "change_percent": global_quote.get("10. change percent", "0%"),
                "volume": int(global_quote.get("06. volume", 0)),
                "previous_close": float(global_quote.get("08. previous close", 0)),
                "open": float(global_quote.get("02. open", 0)),
                "high": float(global_quote.get("03. high", 0)),
                "low": float(global_quote.get("04. low", 0)),
                "last_updated": global_quote.get("07. latest trading day"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get quote for {symbol}: {str(e)}")
            return {"error": str(e)}
    
    async def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview data."""
        
        try:
            data = await self._make_request("OVERVIEW", symbol=symbol)
            
            if "Symbol" in data:
                return {
                    "symbol": data.get("Symbol"),
                    "name": data.get("Name"),
                    "sector": data.get("Sector"),
                    "industry": data.get("Industry"),
                    "market_cap": data.get("MarketCapitalization"),
                    "pe_ratio": data.get("PERatio"),
                    "dividend_yield": data.get("DividendYield"),
                    "revenue_ttm": data.get("RevenueTTM"),
                    "profit_margin": data.get("ProfitMargin"),
                    "beta": data.get("Beta"),
                    "52_week_high": data.get("52WeekHigh"),
                    "52_week_low": data.get("52WeekLow"),
                    "description": data.get("Description"),
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": f"No overview data available for {symbol}"}
            
        except Exception as e:
            logger.error(f"Failed to get overview for {symbol}: {str(e)}")
            return {"error": str(e)}