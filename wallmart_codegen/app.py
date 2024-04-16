import asyncio
import csv
import random

from faker import Faker
from playwright.async_api import async_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_async

from src.sms import purchase_number, receive_sms

# Lee,Elizabeth,leeelizabeth769@yahoo.com,gyzptdwexrtqikrq

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3"
)

VP = (
    {"width": 1920, "height": 1080},
    {"width": 1560, "height": 900}
)

fake = Faker()


def generate_fake_address():
    return {
        'street': fake.street_address(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip_code': fake.zipcode()
    }


async def run(config):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            proxy={
                "server": config['proxy_server'],
                "username": config['proxy_username'],
                "password": config['proxy_password']
            }
        )
        page = await browser.new_page(
            user_agent=random.choice(UA),
            viewport=random.choice(VP)
        )
        await stealth_async(page)
        try:
            await page.goto("https://www.walmart.com/",
                            timeout=35000,  # https://www.walmart.com/account/login?vid=oaoh
                            referer="https://www.google.com/search?q=walmart&sourceid=chrome&ie=UTF-8")
        except PlaywrightTimeoutError:
            print("Slow website")
            print("Ignoring wait")
        await asyncio.sleep(3)

        await page.get_by_text("Sign InAccount").click()
        await asyncio.sleep(3)
        try:
            await page.get_by_text("or create account").click(timeout=3000)
        except PlaywrightTimeoutError:
            print("Now 2nd sign in button, ignoring")

        await asyncio.sleep(5)

        email_input_by_name = page.locator('[name="Email Address"]')
        await email_input_by_name.click(timeout=15000)
        await email_input_by_name.press_sequentially(config["email"], delay=random.randint(200, 250))
        await email_input_by_name.fill(config["email"])
        await asyncio.sleep(2)

        await page.get_by_text("Continue").click()
        await asyncio.sleep(5)

        first_name_input_by_name = page.locator('[name="firstName"]')
        await first_name_input_by_name.press_sequentially(config["first_name"], delay=random.randint(140, 180))
        await asyncio.sleep(0.5)

        last_name_input_by_name = page.locator('[name="lastName"]')
        await last_name_input_by_name.press_sequentially(config["last_name"], delay=random.randint(140, 180))
        await asyncio.sleep(0.5)

        phone = await purchase_number()

        phone_number_input_by_name = page.locator('[name="phoneNumber"]')
        await phone_number_input_by_name.press_sequentially(phone["phonenumber"],
                                                            delay=random.randint(140, 180))
        await asyncio.sleep(1)

        new_password_input_by_name = page.locator('[name="newPassword"]')
        await new_password_input_by_name.press_sequentially(config["password"], delay=random.randint(140, 180))

        await asyncio.sleep(1)

        await page.get_by_text("Continue").last.click()
        await asyncio.sleep(5)

        code = "0"
        while code == "0":
            code = (await receive_sms(phone["order_id"]))["code"]
            await asyncio.sleep(3)
            # if code != "0":
            #     logger.success()

        for i, digit in enumerate(code):
            selector = f"#input-verificationCode"
            if i:
                selector += f"-{i}"
            await page.fill(selector, digit)

        await asyncio.sleep(3)
        await page.click('button[type="submit"][form="verify-phone-otp-form"]')

        await asyncio.sleep(15)

        try:
            await page.get_by_text("I agree to the terms (required)").click(timeout=60000)
        except PlaywrightTimeoutError:
            print("Subscription page not visible. Reloading")
            await page.reload()
            await page.get_by_text("I agree to the terms (required)").click(timeout=60000)

        await page.get_by_text("Continue & add payment method").click(timeout=60000)

        await asyncio.sleep(15)

        print("adding payment method")

        # Danger zone
        try:
            frame = page.frame_locator("#payments-wallet-chooser")
            await frame.get_by_text("Add a new payment method").click(timeout=45000)

            await asyncio.sleep(3)

            # CC
            await frame.locator("#cc-number").type(config["cc_number"], delay=random.randint(140, 180))
            await asyncio.sleep(random.randint(0, 2))

            # First name
            first_name_input_by_name = frame.locator('[name="firstName"]').last
            await first_name_input_by_name.type(config["first_name"], delay=random.randint(140, 180))
            await asyncio.sleep(random.randint(0, 2))

            # Last name
            last_name_input_by_name = frame.locator('[name="lastName"]').last
            await last_name_input_by_name.type(config["last_name"], delay=random.randint(140, 180))
            await asyncio.sleep(random.randint(0, 2))

            # Month
            # await frame.locator("#react-aria-8").select_option("04")
            await frame.locator('div[data-testid="selectMMContainer"] select').select_option(config["exp_month"])
            await asyncio.sleep(random.randint(0, 2))

            # Year
            # await frame.locator("#react-aria-8").select_option("04")
            await frame.locator('div[data-testid="selectYYContainer"] select').select_option(config["exp_year"])
            await asyncio.sleep(random.randint(0, 2))

            # CVV
            last_name_input_by_name = frame.locator('[name="cvv"]')
            await last_name_input_by_name.type(config["cvv"], delay=random.randint(140, 180))
            await asyncio.sleep(random.randint(0, 2))

            # Phone Number
            print("PHONE HUMBER")
            await asyncio.sleep(30)
            await frame.locator('input[data-automation-id="phone-number"]').type(phone["phonenumber"],
                                                                                 delay=random.randint(140, 180))
            await asyncio.sleep(random.randint(0, 2))

            # Street address
            await frame.locator('input[name="newBillingAddress.addressLineOne"]').type(config["street"])
            await asyncio.sleep(random.randint(0, 2))

            # City
            await frame.locator('input[autocomplete="address-level2"]').type(config["city"])
            await asyncio.sleep(random.randint(0, 2))

            # State
            await frame.locator('div[data-automation-id="state-drop-down"] select').select_option(config["state"])
            await asyncio.sleep(random.randint(0, 2))

            # Zip code
            await frame.locator('input[autocomplete="postal-code"]').type(config["zip_code"])
            await asyncio.sleep(random.randint(0, 2))

            # Continue
            try:
                await frame.locator("button[data-test-id='continueBtn']").click()
            except Exception as e:
                print(e)
            await asyncio.sleep(5)

            await page.locator("button[data-test-id='continueBtn']").click()
            await asyncio.sleep(5)

            await page.click('button[aria-label="Claim your free 30-day trial"]')

        except Exception as e:
            print(e)

        await asyncio.sleep(10)
        await browser.close()


# async def main(parallel_workers=5):
#     configs = [
#         {
#             'email': 'haley_baker43@yahoo.com',
#             'password': 'ypbgkcwFDSwsmeplw.32F',
#             'first_name': 'Elizabeth',
#             'last_name': 'Lee',
#             'cc_number': '5154620017051556',
#             'cvv': '757',
#             'exp_month': '07',
#             'exp_year': '2028',
#             'street': '925 S Chugach St',
#             'city': 'Palmer',
#             'zip_code': '99645',
#             'state': 'AK',
#             'proxy_server': 'pr.oxylabs.vip:7777',
#             'proxy_username': 'username1',
#             'proxy_password': 'password1',
#         },
#     ]
#
#     async with async_playwright() as playwright:
#         tasks = [run(playwright, config) for config in configs[:parallel_workers]]
#         await asyncio.gather(*tasks)


def update_file_lines(file_path, lines):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')


def read_and_update_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    remaining_data = data[1:]

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(remaining_data)

    return data[0] if data else None


def read_and_update_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return None
    remaining_lines = lines[1:]

    update_file_lines(file_path, [line.strip() for line in remaining_lines])

    return lines[0].strip().split('|')


# async def main():
#     accounts = read_and_update_csv("accounts.csv")
#     cards = read_and_update_txt('cards.txt')
#     proxies = read_and_update_txt('proxies.txt')
#
#     configs = []
#     for account, card, proxy in zip(accounts, cards, proxies):
#         config = {**account, 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3], **proxy}
#         configs.append(config)
#
#     tasks = [run(config) for config in configs]
#     await asyncio.gather(*tasks)


async def main():
    while True:
        account = read_and_update_csv('accounts.csv')
        card = read_and_update_txt('cards.txt')
        proxy = read_and_update_txt('proxies.txt')

        if not account or not card or not proxy:
            print("No more data available or file missing entries.")
            break
        address = generate_fake_address()
        config = {**account, 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3],
                  **proxy, **address}
        success = await run(config)
        if success:
            print("Process completed successfully.")
            break
        else:
            print("Retrying with next available data set...")
        await asyncio.sleep(1)


asyncio.run(main())