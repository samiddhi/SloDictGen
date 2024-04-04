from common.imports import *


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
        'aspect': {'perfective', 'biaspectual', 'progressive'},
        'number': {'dual', 'singular', 'plural'},
        'negative': {'yes', 'no'},
        'case': {'nominative', 'dative', 'instrumental', 'genitive',
                 'locative', 'accusative'},
        'animate': {'yes', 'no'},
        'definiteness': {'yes', 'no'},
        'type': {'special', 'personal', 'relative', 'general',
                 'auxiliary', 'cardinal', 'proper', 'ordinal', 'reflexive',
                 'pronominal', 'possessive', 'coordinating', 'negative',
                 'interrogative', 'subordinating', 'main', 'demonstrative',
                 'indefinite', 'common'},  # 'participle' removed!
        'person': {'first', 'third', 'second'},
        'degree': {'superlative', 'positive', 'comparative'},
        'vform': {'participle', 'future', 'imperative', 'supine',
                  'conditional', 'present', 'infinitive'},
        'gender': {'masculine', 'feminine', 'neuter'},
        'form': {'letter', 'roman', 'digit'},
        'clitic': {'yes', 'bound'}
    }
    #   'owner_number': {'dual', 'singular', 'plural'},
    #   'owner_gender': {'masculine', 'neuter', 'feminine'}

    for key, values in gram_feat_dict.items():
        if sample in {"yes", "no"}:
            lg.warning("'yes'/'no' appear in two grammar features")
            return_value = "animate/negative"
            return ic([sample, return_value])[1]
        if sample in values:
            if sample in {"participle"}:
                lg.warning('"participle" removed from "type" feature '
                        'for functionality')
            return key

    raise Exception(f"ERROR, {sample} not a known grammar feature.")


if __name__ == "__main__":
    return_gram_feat_type('yes')
