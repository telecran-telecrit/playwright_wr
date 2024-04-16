import aiohttp
import asyncio
import json


async def fetch():
    url = 'https://www.walmart.com/orchestra/home/graphql'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/json',
        'device_profile_ref_id': '5r1of9labirqxraz0kskktor5ep_vwim3un8',
        'dnt': '1',
        'downlink': '10',
        'dpr': '1',
        'origin': 'https://www.walmart.com',
        'referer': 'https://www.walmart.com/account/login?vid=oaoh&tid=0&returnUrl=%2F',
        'sec-ch-ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-cfa724441acb7b514d7811d3ddacd8ee-b291ec4fad083866-00',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'wm_mp': 'true',
        'wm_page_url': 'https://www.walmart.com/account/login?vid=oaoh&tid=0&returnUrl=%2F',
        'wm_qos.correlation_id': '1uGvZJVz8G8AtH2W2qalCsJmeanbQf0nQJYh',
        'x-apollo-operation-name': 'GetLoginOptions',
        'x-enable-server-timing': '1',
        'x-latency-trace': '1',
        'x-o-bu': 'WALMART-US',
        'x-o-ccm': 'server',
        'x-o-correlation-id': '1uGvZJVz8G8AtH2W2qalCsJmeanbQf0nQJYh',
        'x-o-gql-query': 'query GetLoginOptions',
        'x-o-mart': 'B2C',
        'x-o-platform': 'rweb',
        'x-o-platform-version': 'us-web-1.127.0-14ef2d4b4491be5938a5fa20df7d77ad9264e136-0321',
        'x-o-segment': 'oaoh'
    }
    data = {
        "query": "query GetLoginOptions($input:UserOptionsInput!){getLoginOptions(input:$input){loginOptions{...LoginOptionsFragment}errors{...LoginOptionsErrorFragment}}}"
                 "fragment LoginOptionsFragment on LoginOptions{loginId loginIdType emailId phoneNumber{number countryCode}canUsePassword canUsePhoneOTP canUseEmailOTP loginPhoneLastFour loginMaskedEmailId signInPreference loginPreference lastLoginPreference hasRemainingFactors isPhoneConnected otherAccountsWithPhone loginMaskedEmailId hasPasskeyOnProfile}"
                 "fragment LoginOptionsErrorFragment on IdentityLoginOptionsError{code message}",
        "variables": {"input": {"loginId": "takesm323@yahoo.com", "loginIdType": "EMAIL"}}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            response_json = await response.json()
            print(response_json)


loop = asyncio.get_event_loop()
loop.run_until_complete(fetch())
