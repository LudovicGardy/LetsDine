import sys
import streamlit as st



def is_streamlit_active():
    """
    Check if Streamlit is the active runtime environment.
    """
    return "streamlit" in sys.modules


def create_cache_decorator(force_lru_cache: bool = False):
    if is_streamlit_active() and not force_lru_cache:
        cache_decorator = st.cache_data
        print("Streamlit Cache.")
    else:
        from functools import lru_cache

        cache_decorator = lru_cache(maxsize=None)
        print("LRU Cache.")

    return cache_decorator
