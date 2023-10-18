
#used to store tokens
class UserSecretConfig():
    reset_password_token_secret = 'reset_password_token_secret'
    verification_token_secret = 'verification_token_secret'
    jwt_secret = 'jwt_secret'   

user_secrets: UserSecretConfig = UserSecretConfig()

def configure_secrets(
        jwt_secret: str, 
        reset_password_token_secret: str, 
        verification_token_secret: str
    ):

    user_secrets.jwt_secret = jwt_secret
    user_secrets.reset_password_token_secret = reset_password_token_secret
    user_secrets.verification_token_secret = verification_token_secret

async def user_secret_generator() -> UserSecretConfig:
    yield user_secrets