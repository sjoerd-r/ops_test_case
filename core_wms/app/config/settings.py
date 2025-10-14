from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    name: str = "Sophie"
    version: str = "1.0.0"

class DatabaseSettings(BaseSettings):
    database_url: str 
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class RabbitMQSettings(BaseSettings):
    rabbitmq_url: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class GraphQLSettings(BaseSettings):
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class GooglePubSubSettings(BaseSettings):
    project_id: str
    topic_id: str
    subscription_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class ApolloSettings(BaseSettings):
    apollo_graph_ref: str
    apollo_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" 

class AuthSettings(BaseSettings):
    pass

class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()
    graphql: GraphQLSettings = GraphQLSettings()
    google_pubsub: GooglePubSubSettings = GooglePubSubSettings()
    apollo: ApolloSettings = ApolloSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def settings() -> Settings:
    return Settings()