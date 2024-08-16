import sys


def is_streamlit_active():
    """Vérifie si Streamlit est l'environnement d'exécution actif."""
    return "streamlit" in sys.modules


def create_cache_decorator(force_lru_cache: bool = False):
    if is_streamlit_active() and not force_lru_cache:
        import streamlit as st

        cache_decorator = st.cache_data
        print("Streamlit Cache.")
    else:
        from functools import lru_cache

        cache_decorator = lru_cache(maxsize=None)
        print("LRU Cache.")

    return cache_decorator
