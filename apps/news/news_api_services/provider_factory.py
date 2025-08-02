from .providers.newsapi_org import NewsAPIProvider


PROVIDERS = {
    'newsapi': NewsAPIProvider,
}

def get_provider(provider_name: str):
    provider_class = PROVIDERS.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Provider with name {provider_name}, not found!")
    
    return provider_class()
