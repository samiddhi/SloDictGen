def return_gram_feat_type(sample: str) -> str:
    """
    Takes a string and returns its grammar feature name.

    e.g.
        "first"      -> "person"

        "nominative" -> "case"

    :param sample: (str) sample word to check for feature type
    :return: string of feature type
    """
    gram_feat_dict = {
        "v_form": [],
        "case": [],
        "person": [],
        "number": [],
        "gender": [],
        "x": [],
        "c": [],
        "z": []
    }
    raise NotImplementedError


def ordered_grammar_name(
        *,
        v_form: str = None,
        case: str = None,
        person: str = None,
        number: str = None,
        gender: str = None,
):
    """
    Ensures that grammatical data is ordered correctly before concatenating
    them into a grammar name. Intended for use for individual word forms.
    kwargs mandatory.

    :param v_form: Verb form.
    :param case: Grammatical case.
    :param person: Grammatical person (1st, 2nd, 3rd).
    :param number: Singular/Dual/Plural.
    :param gender: Grammatical gender.
    :return: String of found items concatenated with an underscore in the
        correct order.
    """
    return concatenate_variables(v_form, case, person, number, gender)


def concatenate_variables(*items):
    """
    Concatenates variables into a string, separated by underscores.

    :param items: Arguments to concatenate.
    :return: Concatenated string.
    """
    result = "_".join(str(item) for item in items if item is not None)
    return result
