from twscrape import API, create_pool

api = API("account.db")

await create_pool(api)
await api.pool.add_account