# from dotenv import load_dotenv
# from openai import OpenAI
# 
# from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
# import os
# 
# 
# class LeagueAccountGPT:
# 
#     def __init__(self):
#         self.client = OpenAI()
#         load_dotenv()
#         self.TOKEN_GPT = os.getenv("OPENAI_API_KEY")
# 
# 
#     def get_tips(self, account_instance: AccountLoL):
#         self.client.api_key = self.TOKEN_GPT
#         response = self.client.completions.create(
#             model="gpt-3.5-turbo-instruct",
#             max_tokens=200,
#             prompt="You are a League of Legends coach and are responsible for analyzing this account and giving tips to improve it and its performance, list just two tips"
#                    f"{account_instance.nick}"
#                    f"{account_instance.pdl} League Points"
#                    f"{account_instance.tier} Tier,"
#                    f"{account_instance.league} League"
#                    f"{account_instance.winrate} Winrate")
#         return response.choices[0].text
