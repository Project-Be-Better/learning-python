def is_anagram(s: str, t: str) -> bool:
    """
    Returns True if both strings are anagrams
    """
    return sorted(s) == sorted(t)


def is_anagram_longer(s: str, t: str) -> bool:
    """
    Returns True if both strings are anagrams
    """

    # convert string to dict
    def convert_to_dict(str_to_convert):
        dict_holder = {}
        for i in str_to_convert:
            dict_holder[i] = dict_holder.get(i, 0) + 1

        return dict_holder

    dict_s = convert_to_dict(s)
    dict_t = convert_to_dict(t)

    return dict_s == dict_t
