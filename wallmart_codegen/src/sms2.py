import aiohttp
import asyncio
from threading import Thread
from loguru import logger

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

logger.add("daisysms_logs.log", rotation="10 MB")

API_KEY = "jShVuORHOaqtPPsrY5IdODZCBn3nko"
BASE_URL = "https://daisysms.com"
SERVICE_SHORT = "wr" # Walmart
MAX_PRICE = 0.50

#https://daisysms.com/docs/api

async def purchase_number ():
    data = {
        "action": "getNumber",
        "api_key": API_KEY,
        "country": "US",
        "service": SERVICE_SHORT,
        "max_price": str(MAX_PRICE),
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_URL + f"/stubs/handler_api.php?{urlencode(data, doseq=False)}") as response:
                if (response.status == 200 or response.status == 400 or response.status == 401 or response.status == 402 or response.status == 403):
                    result = await response.text()
                    resultData = result.split(':')
                    statusMode = resultData[0]
                    if (statusMode == 'MAX_PRICE_EXCEEDED'):
                        logger.info("Please, change variable MAX_PRICE.")
                    elif (statusMode == 'ACCESS_NUMBER' and len(resultData) >= 3 and response.status == 200):
                        res = dict()
                        res['order_id'] = resultData[1]
                        res['cost'] = MAX_PRICE # TODO: What is actual price
                        res['number'] = str(resultData[2])
                        if (res['number'][0] == '+'):
                            res['number'] = res['number'][1:]
                        if (res['number'][0] == '1' or res['number'][0] == '7'):
                            res['phonenumber'] = res['number'][1:]
                        else:
                            res['phonenumber'] = res['number']
                        logger.info("Number retrieved successfully.")
                        logger.success(f"Number: {res['number']} | Order ID: {res['order_id']} | "
                                       f"Cost: {res['cost']}")
                        return res
                logger.error(f"Failed to retrieve number. Status code: {response.status}."
                             f" Answer: {await response.text()}")
        except Exception as e:
            logger.exception(f"Exception occurred while trying to get number: {e}")
        return None


async def receive_sms (order_id):
    data = {
        "action": "getStatus",
        "api_key": API_KEY,
        "id": str(order_id),
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_URL + f"/stubs/handler_api.php?{urlencode(data, doseq=False)}") as response:
                if (response.status == 200 or response.status == 400 or response.status == 401 or response.status == 402 or response.status == 403):
                    result = await response.text()
                    resultData = result.split(':')
                    statusMode = resultData[0]
                    res = dict()
                    res['statusMode'] = statusMode
                    res['order_id'] = str(order_id)
                    res['code'] = ''
                    if (statusMode == 'NO_ACTIVATION'):
                        return res
                    elif (statusMode == 'STATUS_WAIT_CODE'):
                        logger.info('Please, be patient')
                        return res
                    elif (len(resultData) >= 2 and (response.status == 200 or statusMode == 'STATUS_OK')):
                        number = resultData[1]
                        res['code'] = number
                        if (number is not None and len(number.strip()) > 0):
                            logger.info(f"Found {order_id} - {number}")
                            return res
                    else:
                        logger.error(f"Smth went wrong: {await response.text()}")
                    return res
                else:
                    logger.error(f"Failed to receive SMS. Status code: {response.status}")
        except Exception as e:
            logger.exception(f"Exception occurred while trying to receive SMS: {e}")
        res = dict()
        res['statusMode'] = 'FAILED'
        res['order_id'] = str(order_id)
        res['code'] = ''
        return res

def async_to_sync (awaitable):
    class MyThread (Thread):
        def run (self):
            self.res = None
            loop = asyncio.new_event_loop() #loop = asyncio.get_event_loop()
            self.res = loop.run_until_complete(self._run())
            loop.close()
            #self.res = asyncio.run(self._run())
        async def _run (self):
            self.res = await awaitable
            return self.res
    t = MyThread()
    t.start()
    try:
        t.join()
    except KeyboardInterrupt:
        pass
    return t.res

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
