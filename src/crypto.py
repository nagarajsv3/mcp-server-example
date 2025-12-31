import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Cryto")


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

@mcp.tool()
def get_cryptocurrency_price(crypto: str) -> str:
    """Fetch the USD price for a cryptocurrency using the CoinGecko simple price API.

     Parameters
     ----------
     crypto : str
         Cryptocurrency identifier accepted by CoinGecko (for example, "bitcoin",
         "ethereum"). The value will be stripped and lowercased before querying.

     Returns
     -------
     str
         A human-readable message:
         - On success: "The price of {crypto} is ${price} USD."
         - If the crypto identifier is invalid or not found: informative message.
         - If a network or response error occurs: error message describing the failure.

     Raises
     ------
     None
         Network and JSON parsing errors are handled internally and returned as strings.

     Notes
     -----
     - Endpoint: https://api.coingecko.com/api/v3/simple/price
     - Query params: ids=<crypto>&vs_currencies=usd
     - Request timeout: 10 seconds

     Examples
     --------
     >>> get_cryptocurrency_price("bitcoin")
     "The price of bitcoin is $12345.67 USD."
     """
    if not crypto or not isinstance(crypto, str):
        return "Invalid cryptocurrency identifier."

    crypto_id = crypto.lower().strip()
    params = {"ids": crypto_id, "vs_currencies": "usd"}

    try:
        resp = requests.get(COINGECKO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        price = data.get(crypto_id, {}).get("usd")
        if price is None:
            return f"Price for {crypto} not found."
        return f"The price of {crypto} is ${price} USD."
    except requests.exceptions.RequestException as e:
        return f"Network error while fetching price for {crypto}: {e}"
    except ValueError:
        return f"Invalid response when fetching price for {crypto}."
    except Exception as e:
        return f"Error fetching price for {crypto}: {e}"

if __name__ == "__main__":
    print('starting to run')
    mcp.run()