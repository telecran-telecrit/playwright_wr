import aiohttp
import asyncio
from loguru import logger

logger.add("smspool_logs.log", rotation="10 MB")

API_KEY = "e6fedlfRXzjUQHYjOiMGJXlINUwdoJug"
BASE_URL = "https://api.smspool.net"


async def purchase_number():
    data = {
        "country": "US",
        "service": "Walmart",
        "key": API_KEY
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("https://api.smspool.net/purchase/sms", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result["success"] == 1:
                        logger.info("Number retrieved successfully.")
                        logger.success(f"Number: {result['number']} | Order ID: {result['order_id']} | "
                                       f"Cost: {result['cost']}")
                        return result
                logger.error(f"Failed to retrieve number. Status code: {response.status}."
                             f" Answer: {await response.text()}")
        except Exception as e:
            logger.exception(f"Exception occurred while trying to get number: {e}")


async def receive_sms(order_id):
    data = {
        "key": API_KEY
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("https://api.smspool.net/request/history", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    for number in result:
                        if number["order_code"] == order_id:
                            logger.info(f"Found {order_id} - {number}")
                            return number
                        else:
                            logger.debug(f"{number['order_id']} != {order_id}")
                    logger.info("Number not found")
                    return
                else:
                    logger.error(f"Failed to receive SMS. Status code: {response.status}")
        except Exception as e:
            logger.exception(f"Exception occurred while trying to receive SMS: {e}")


# Example usage
async def main():
    a = {'success': 1, 'number': 16015954518, 'cc': '1', 'phonenumber': '6015954518', 'order_id': 'DSPQAYKT',
         'country': 'United States', 'service': 'Walmart', 'pool': 7, 'expires_in': 1200, 'expiration': 1712758090,
         'message': 'You have succesfully ordered a Walmart number from pool: Foxtrot for 0.24.', 'cost': '0.24',
         'cost_in_cents': 24}
    b = {'cost': '0.24', 'order_code': 'ZWATXJMC', 'phonenumber': '16152817121', 'code': '682835',
                'full_code': "[Walmart] 682835 is your Walmart verification code. It expires in 15 minutes. We'll never call or text to request this code.",
                'short_name': 'US', 'service': 'Walmart', 'status': 'completed', 'pool': 7,
                'timestamp': '2024-04-10 15:58:33', 'completed_on': '2024-04-10 16:00:57', 'expiry': 1712758713,
                'time_left': 1055}
    #
    # number = await purchase_number()
    # print(number)

    sms = await receive_sms(a["order_id"])
    print(sms)


if __name__ == "__main__":
    asyncio.run(main())
