def is_anagram(s: str, t: str) -> bool:
    """
    Returns True if both strings are anagrams
    """
    return sorted(s) == sorted(t)
