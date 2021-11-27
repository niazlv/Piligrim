from environs import Env

env = Env()
env.read_env()

token = env.str("TOKEN")
hostc = env.str("PG_HOST")
userc = env.str("PG_USER")
passc = env.str("PG_PASS")