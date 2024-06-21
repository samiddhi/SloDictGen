from common.imports import *
from unidecode import unidecode
import re

ALPHA: str = "abcčdefghijklmnopqrsštuvwxyzž"

OKRS: Dict[str, str] = {
    'adm.': 'administracija',
    'aer.': 'aeronavtika',
    'agr.': 'agronomija, agrotehnika',
    'ali': 'prim.',
    'alp.': 'alpinistika',
    'anat.': 'anatomija',
    'ant.': 'antonim; prim.',
    'antr.': 'antropologija',
    'arheol.': 'arheologija',
    'arhit.': 'arhitektura',
    'astrol.': 'astrologija',
    'astron.': 'astronomija',
    'avt.': 'avtomobilizem, avtomehanika',
    'bibl.': 'biblijsko; prim.',
    'biblio.': 'bibliotekarstvo',
    'biokem.': 'biokemija',
    'biol.': 'biologija',
    'bot.': 'botanika',
    'brezoseb.': 'brezosebno',
    'čeb.': 'čebelarstvo',
    'čl.': 'člen',
    'člen.': 'členek',
    'daj.': 'dajalnik',
    'dv.': 'dvojina',
    'ed.': 'ednina',
    'ekon.': 'ekonomija',
    'ekspr.': 'ekspresivno; prim.',
    'elektr.': 'elektrotehnika',
    'elipt.': 'eliptično; prim.',
    'etn.': 'etnografija, etnologija',
    'evfem.': 'evfemistično; prim.',
    'farm.': 'farmacija, farmakologija',
    'filat.': 'filatelija',
    'film.': 'filmski izraz',
    'filoz.': 'filozofija',
    'fin.': 'finančništvo',
    'fiz.': 'fizika',
    'fot.': 'fotografija',
    'friz.': 'frizerstvo',
    'gastr.': 'gastronomija, kuharstvo',
    'geod.': 'geodezija',
    'geogr.': 'geografija',
    'geol.': 'geologija',
    'geom.': 'geometrija',
    'gl.': 'glej',
    'glasb.': 'glasba, muzikologija',
    'gled.': 'gledališče',
    'gost.': 'gostinstvo',
    'gozd.': 'gozdarstvo',
    'grad.': 'gradbeništvo',
    'igr.': 'igre (za zabavo)',
    'im.': 'imenovalnik',
    'in': 'prim.',
    'ipd.': 'in podobno',
    'iron.': 'ironično; prim.',
    'itd.': 'in tako dalje',
    'jezikosl.': 'jezikoslovje',
    'kem.': 'kemija',
    'knjiž.': 'knjižno; prim.',
    'kor.': 'koreografija',
    'kozm.': 'kozmetika',
    'krat.': 'kratica',
    'les.': 'lesarska stroka',
    'lit.': 'literarna teorija, literarna zgodovina',
    'ljubk.': 'ljubkovalno; prim.',
    'lov.': 'lovstvo',
    'm': 'samostalnik moškega spola',
    'm.': 'moški spol',
    'mat.': 'matematika',
    'med.': 'medicina',
    'medm.': 'medmet',
    'mest.': 'mestnik',
    'metal.': 'metalurgija',
    'meteor.': 'meteorologija',
    'min.': 'mineralogija',
    'mitol.': 'mitologija, zlasti slovanska',
    'mn.': 'množina',
    'mont.': 'montanistika',
    'nam.': 'namenilnik',
    'nar.': 'narečno; prim.',
    'nav.': 'navadno',
    'navt.': 'navtika, pomorstvo',
    'nedov.': 'nedovršni glagol',
    'neprav.': 'nepravilno; prim.',
    'nepreh.': 'neprehodna raba (glagola)',
    'neskl.': 'nesklonljiv(o)',
    'nizko': 'prim.',
    'nižje pog.': 'nižje pogovorno; prim.',
    'num.': 'numizmatika',
    'obl.': 'oblačilna stroka',
    'obrt.': 'obrtnišvo',
    'okrajš.': 'okrajšava',
    'or.': 'orodnik',
    'os.': 'oseba',
    'otr.': 'otroško; prim.',
    'oz.': 'oziroma',
    'pal.': 'paleontologija',
    'papir.': 'papirništvo',
    'ped.': 'pedagogika',
    'pesn.': 'pesniško; prim.',
    'petr.': 'petrografija, petrologija',
    'pisar.': 'pisarniško, prim.',
    'pog.': 'pogovorno; prim.',
    'polit.': 'politika',
    'pooseb.': 'poosebljeno; prim.',
    'povdk.': 'povedkovnik',
    'pravn.': 'pravni izraz',
    'predl.': 'predlog',
    'preg.': 'pregovor',
    'preh.': 'prehodna raba (glagola)',
    'pren.': 'preneseno; prim.',
    'prid.': 'pridevnik, pridevniška raba',
    'prim.': 'primerjaj',
    'prisl.': 'prislov, prislovna raba',
    'psih.': 'psihologija',
    'psiht.': 'psihiatrija',
    'ptt': 'pošta, telegraf, telefon',
    'publ.': 'publicistično; prim.',
    'rač.': 'računalništvo',
    'rad.': 'radiotehnika, radiotelevizija',
    'rel.': 'religija',
    'rib.': 'ribištvo',
    'rod.': 'rodilnik',
    's': 'samostalnik srednjega spola',
    's.': 'srednji spol',
    'sam.': 'samostalniška raba; prim.',
    'simb.': 'simbol',
    'slabš.': 'slabšalno; prim.',
    'soc.': 'sociologija',
    'star.': 'starinsko; prim.',
    'stil.': 'stilno; prim.',
    'strojn.': 'strojništvo',
    'sv.': 'svet(i)',
    'šah.': 'šahovski izraz',
    'šalj.': 'šaljivo; prim.',
    'šol.': 'šolstvo',
    'šport.': 'športni izraz',
    'štev.': 'števnik',
    'teh.': 'tehnika',
    'tekst.': 'tekstilna stroka',
    'tisk.': 'tiskarstvo',
    'tož.': 'tožilnik',
    'trg.': 'trgovina',
    'tudi': 'prim.',
    'tur.': 'turizem',
    'um.': 'umetnost, umetnostna zgodovina',
    'urb.': 'urbanizem',
    'usnj.': 'usnjarstvo',
    'vet.': 'veterina',
    'vez.': 'veznik, vezniška raba',
    'voj.': 'vojska',
    'vrt.': 'vrtnarstvo',
    'vulg.': 'vulgarno; prim.',
    'vznes.': 'vzneseno; prim.',
    'zaim.': 'zaimek',
    'zal.': 'založništvo',
    'zastar.': 'zastarelo; prim.',
    'zgod.': 'zgodovina, zgodovinske pomožne vede',
    'zool.': 'zoologija',
    'ž': 'samostalnik ženskega spola',
    'ž.': 'ženski spol',
    'žarg.': 'žargon; prim.',
    'žel.': 'železnica',
}

DECOR = {
    'adm.': {'si': 'administracija', 'en': 'administration'},
    'aer.': {'si': 'aeronavtika', 'en': 'aeronautics'},
    'agr.': {'si': 'agronomija, agrotehnika', 'en': 'agronomy, agricultural technology'},
    'ali': {'si': 'prim.', 'en': 'prim.'},
    'alp.': {'si': 'alpinistika', 'en': 'mountaineering'},
    'anat.': {'si': 'anatomija', 'en': 'anatomy'},
    'ant.': {'si': 'antonim; prim.', 'en': 'antonym; see'},
    'antr.': {'si': 'antropologija', 'en': 'anthropology'},
    'arheol.': {'si': 'arheologija', 'en': 'archaeology'},
    'arhit.': {'si': 'arhitektura', 'en': 'architecture'},
    'astrol.': {'si': 'astrologija', 'en': 'astrology'},
    'astron.': {'si': 'astronomija', 'en': 'astronomy'},
    'avt.': {'si': 'avtomobilizem, avtomehanika', 'en': 'automobile industry, automotive mechanics'},
    'bibl.': {'si': 'biblijsko; prim.', 'en': 'biblical; see'},
    'biblio.': {'si': 'bibliotekarstvo', 'en': 'library science'},
    'biokem.': {'si': 'biokemija', 'en': 'biochemistry'},
    'biol.': {'si': 'biologija', 'en': 'biology'},
    'bot.': {'si': 'botanika', 'en': 'botany'},
    'brezoseb.': {'si': 'brezosebno', 'en': 'impersonal'},
    'čeb.': {'si': 'čebelarstvo', 'en': 'beekeeping'},
    'čl.': {'si': 'člen', 'en': 'article'},
    'člen.': {'si': 'členek', 'en': 'particular'},
    'daj.': {'si': 'dajalnik', 'en': 'dative'},
    'dv.': {'si': 'dvojina', 'en': 'dual'},
    'ed.': {'si': 'ednina', 'en': 'singular'},
    'ekon.': {'si': 'ekonomija', 'en': 'economics'},
    'ekspr.': {'si': 'ekspresivno; prim.', 'en': 'expressive; see'},
    'elektr.': {'si': 'elektrotehnika', 'en': 'electrical engineering'},
    'elipt.': {'si': 'eliptično; prim.', 'en': 'elliptical; see'},
    'etn.': {'si': 'etnografija, etnologija', 'en': 'ethnography, ethnology'},
    'evfem.': {'si': 'evfemistično; prim.', 'en': 'euphemistic; see'},
    'farm.': {'si': 'farmacija, farmakologija', 'en': 'pharmacy, pharmacology'},
    'filat.': {'si': 'filatelija', 'en': 'philately'},
    'film.': {'si': 'filmski izraz', 'en': 'film expression'},
    'filoz.': {'si': 'filozofija', 'en': 'philosophy'},
    'fin.': {'si': 'finančništvo', 'en': 'finance'},
    'fiz.': {'si': 'fizika', 'en': 'physics'},
    'fot.': {'si': 'fotografija', 'en': 'photography'},
    'friz.': {'si': 'frizerstvo', 'en': 'hairdressing'},
    'gastr.': {'si': 'gastronomija, kuharstvo', 'en': 'gastronomy, cooking'},
    'geod.': {'si': 'geodezija', 'en': 'geodesy'},
    'geogr.': {'si': 'geografija', 'en': 'geography'},
    'geol.': {'si': 'geologija', 'en': 'geology'},
    'geom.': {'si': 'geometrija', 'en': 'geometry'},
    'gl.': {'si': 'glej', 'en': 'see'},
    'glasb.': {'si': 'glasba, muzikologija', 'en': 'music, musicology'},
    'gled.': {'si': 'gledališče', 'en': 'theater'},
    'gost.': {'si': 'gostinstvo', 'en': 'catering'},
    'gozd.': {'si': 'gozdarstvo', 'en': 'forestry'},
    'grad.': {'si': 'gradbeništvo', 'en': 'construction'},
    'igr.': {'si': 'igre (za zabavo)', 'en': 'games (for entertainment)'},
    'im.': {'si': 'imenovalnik', 'en': 'nominative'},
    'in': {'si': 'prim.', 'en': 'see'},
    'ipd.': {'si': 'in podobno', 'en': 'and the like'},
    'iron.': {'si': 'ironično; prim.', 'en': 'ironic; see'},
    'itd.': {'si': 'in tako dalje', 'en': 'and so on'},
    'jezikosl.': {'si': 'jezikoslovje', 'en': 'linguistics'},
    'kem.': {'si': 'kemija', 'en': 'chemistry'},
    'knjiž.': {'si': 'knjižno; prim.', 'en': 'literary; see'},
    'kor.': {'si': 'koreografija', 'en': 'choreography'},
    'kozm.': {'si': 'kozmetika', 'en': 'cosmetics'},
    'krat.': {'si': 'kratica', 'en': 'abbreviation'},
    'les.': {'si': 'lesarska stroka', 'en': 'woodworking industry'},
    'lit.': {'si': 'literarna teorija, literarna zgodovina', 'en': 'literary theory, literary history'},
    'ljubk.': {'si': 'ljubkovalno; prim.', 'en': 'endearing; see'},
    'lov.': {'si': 'lovstvo', 'en': 'hunting'},
    'm': {'si': 'samostalnik moškega spola', 'en': 'masculine noun'},
    'm.': {'si': 'moški spol', 'en': 'masculine gender'},
    'mat.': {'si': 'matematika', 'en': 'mathematics'},
    'med.': {'si': 'medicina', 'en': 'medicine'},
    'medm.': {'si': 'medmet', 'en': 'interjection'},
    'mest.': {'si': 'mestnik', 'en': 'locative'},
    'metal.': {'si': 'metalurgija', 'en': 'metallurgy'},
    'meteor.': {'si': 'meteorologija', 'en': 'meteorology'},
    'min.': {'si': 'mineralogija', 'en': 'mineralogy'},
    'mitol.': {'si': 'mitologija, zlasti slovanska', 'en': 'mythology, especially Slavic'},
    'mn.': {'si': 'množina', 'en': 'plural'},
    'mont.': {'si': 'montanistika', 'en': 'mining industry'},
    'nam.': {'si': 'namenilnik', 'en': 'purpose'},
    'nar.': {'si': 'narečno; prim.', 'en': 'dialectal; see'},
    'nav.': {'si': 'navadno', 'en': 'usually'},
    'navt.': {'si': 'navtika, pomorstvo', 'en': 'navigation, maritime'},
    'nedov.': {'si': 'nedovršni glagol', 'en': 'incomplete verb'},
    'neprav.': {'si': 'nepravilno; prim.', 'en': 'irregular; see'},
    'nepreh.': {'si': 'neprehodna raba (glagola)', 'en': 'intransitive use (of verb)'},
    'neskl.': {'si': 'nesklonljiv(o)', 'en': 'indeclinable'},
    'nizko': {'si': 'prim.', 'en': 'see'},
    'nižje pog.': {'si': 'nižje pogovorno; prim.', 'en': 'lower colloquial; see'},
    'num.': {'si': 'numizmatika', 'en': 'numismatics'},
    'obl.': {'si': 'oblačilna stroka', 'en': 'clothing industry'},
    "obrt.": {"si": "obrtnišvo", "en": "craftsmanship"},
    "okrajš.": {"si": "okrajšava", "en": "abbreviation"},
    "or.": {"si": "orodnik", "en": "instrumental case"},
    "os.": {"si": "oseba", "en": "person"},
    "otr.": {"si": "otroško; prim.", "en": "childish; colloquial"},
    "oz.": {"si": "oziroma", "en": "or"},
    "pal.": {"si": "paleontologija", "en": "paleontology"},
    "papir.": {"si": "papirništvo", "en": "paper industry"},
    "ped.": {"si": "pedagogika", "en": "pedagogy"},
    "pesn.": {"si": "pesniško; prim.", "en": "poetic; compare"},
    "petr.": {"si": "petrografija, petrologija", "en": "petrography, petrology"},
    "pisar.": {"si": "pisarniško, prim.", "en": "office; compare"},
    "pog.": {"si": "pogovorno; prim.", "en": "colloquial; compare"},
    "polit.": {"si": "politika", "en": "politics"},
    "pooseb.": {"si": "poosebljeno; prim.", "en": "personified; compare"},
    "povdk.": {"si": "povedkovnik", "en": "predicate noun"},
    "pravn.": {"si": "pravni izraz", "en": "legal term"},
    "predl.": {"si": "predlog", "en": "preposition"},
    "preg.": {"si": "pregovor", "en": "proverb"},
    "preh.": {"si": "prehodna raba (glagola)", "en": "transitive use (of a verb)"},
    "pren.": {"si": "preneseno; prim.", "en": "figuratively; compare"},
    "prid.": {"si": "pridevnik, pridevniška raba", "en": "adjective, adjectival use"},
    "prim.": {"si": "primerjaj", "en": "compare"},
    "prisl.": {"si": "prislov, prislovna raba", "en": "adverb, adverbial use"},
    "psih.": {"si": "psihologija", "en": "psychology"},
    "psiht.": {"si": "psihiatrija", "en": "psychiatry"},
    "ptt": {"si": "pošta, telegraf, telefon", "en": "post, telegraph, telephone"},
    "publ.": {"si": "publicistično; prim.", "en": "journalistic; compare"},
    "rač.": {"si": "računalništvo", "en": "computing"},
    "rad.": {"si": "radiotehnika, radiotelevizija", "en": "radiotechnology, radio and television"},
    "rel.": {"si": "religija", "en": "religion"},
    "rib.": {"si": "ribištvo", "en": "fishing"},
    "rod.": {"si": "rodilnik", "en": "genitive case"},
    "s": {"si": "samostalnik srednjega spola", "en": "neuter noun"},
    "s.": {"si": "srednji spol", "en": "neuter gender"},
    "sam.": {"si": "samostalniška raba; prim.", "en": "substantival; compare"},
    "simb.": {"si": "simbol", "en": "symbol"},
    "slabš.": {"si": "slabšalno; prim.", "en": "derogatory; compare"},
    "soc.": {"si": "sociologija", "en": "sociology"},
    "star.": {"si": "starinsko; prim.", "en": "archaic; compare"},
    "stil.": {"si": "stilno; prim.", "en": "stylistic; compare"},
    "strojn.": {"si": "strojništvo", "en": "mechanical engineering"},
    "sv.": {"si": "svet(i)", "en": "world(s)"},
    "šah.": {"si": "šahovski izraz", "en": "chess term"},
    "šalj.": {"si": "šaljivo; prim.", "en": "humorous; compare"},
    "šol.": {"si": "šolstvo", "en": "education"},
    "šport.": {"si": "športni izraz", "en": "sports term"},
    "štev.": {"si": "števnik", "en": "numeral"},
    "teh.": {"si": "tehnika", "en": "technique"},
    "tekst.": {"si": "tekstilna stroka", "en": "textile industry"},
    "tisk.": {"si": "tiskarstvo", "en": "printing"},
    "tož.": {"si": "tožilnik", "en": "accusative case"},
    "trg.": {"si": "trgovina", "en": "commerce"},
    "tudi": {"si": "prim.", "en": "compare"},
    "tur.": {"si": "turizem", "en": "tourism"},
    "um.": {"si": "umetnost, umetnostna zgodovina", "en": "art, art history"},
    "urb.": {"si": "urbanizem", "en": "urbanism"},
    "usnj.": {"si": "usnjarstvo", "en": "leather industry"},
    "vet.": {"si": "veterina", "en": "veterinary medicine"},
    "vez.": {"si": "veznik, vezniška raba", "en": "conjunction, conjunctional use"},
    "voj.": {"si": "vojska", "en": "army"},
    "vrt.": {"si": "vrtnarstvo", "en": "gardening"},
    "vulg.": {"si": "vulgarno; prim.", "en": "vulgar; compare"},
    "vznes.": {"si": "vzneseno; prim.", "en": "elevated; compare"},
    "zaim.": {"si": "zaimek", "en": "pronoun"},
    "zal.": {"si": "založništvo", "en": "publishing"},
    "zastar.": {"si": "zastarelo; prim.", "en": "obsolete; compare"},
    "zgod.": {"si": "zgodovina, zgodovinske pomožne vede", "en": "history, auxiliary historical disciplines"},
    "zool.": {"si": "zoologija", "en": "zoology"},
    "ž": {"si": "samostalnik ženskega spola", "en": "feminine noun"},
    "ž.": {"si": "ženski spol", "en": "feminine gender"},
    "žarg.": {"si": "žargon; prim.", "en": "jargon; compare"},
    "žel.": {"si": "železnica", "en": "railway"}
}

# Grammar Feature categories
gfcat: Dict[str, List[str]] = {
    'aspect': ['perfective', 'progressive', 'biaspectual'],
    'number': ['singular', 'dual', 'plural'],
    'negative': ['yes', 'no'],
    'case': ['nominative', 'genitive', 'dative', 'accusative', 'locative',
             'instrumental'],
    'animate': ['yes', 'no'],
    'definiteness': ['yes', 'no'],
    'word_type': [
        'special', 'personal', 'relative', 'general', 'auxiliary', 'cardinal',
        'proper', 'ordinal', 'reflexive', 'pronominal', 'possessive',
        'coordinating', 'negative', 'interrogative', 'subordinating', 'main',
        'demonstrative', 'indefinite', 'common'],
    'person': ['first', 'second', 'third'],
    'degree': ['positive', 'comparative', 'superlative'],
    'vform': [
        'present', 'imperative', 'participle', 'conditional', 'future',
        'infinitive', 'supine'
    ],
    'gender': ['masculine', 'feminine', 'neuter'],
    'form': ['letter', 'roman', 'digit'],
    'clitic': ['yes', 'bound']
}

#           table_name : (top/columns, left/rows)
table_types: Dict[str, Dict[str, List[List[str]]]] = dict(
    noun=dict(
        declension=[gfcat['number'], gfcat['case']]
    ),
    verb={
        'present': [gfcat['number'], gfcat['person'], ],
        'imperative': [gfcat['number'], ['first', 'second']],
        'participle': [gfcat['number'], gfcat['gender']],
        'Non-Finite': [['form', ], ['infinitive', 'supine']],
        'conditional': [['form', ], ['form', ], ],
        'future': [gfcat['number'], gfcat['person'], ],
    },
    adjective={
        'agender': [gfcat['number'], gfcat['case']],
        'masculine': [gfcat['number'], gfcat['case']],
        'feminine': [gfcat['number'], gfcat['case']],
        'neuter': [gfcat['number'], gfcat['case']],
    },
    adverb=dict(
        form=[['form', ], ['form', ], ]
    ),
    particle=dict(
        form=[['form', ], ['form', ], ]
    ),
    interjection=dict(
        form=[['form', ], ['form', ], ]
    ),
    conjunction=dict(
        form=[['form', ], ['form', ], ]
    ),
    preposition=dict(
        form=[['form', ], ['form', ], ]
    ),
    abbreviation=dict(
        form=[['form', ], ['form', ], ]
    ),
    pronoun={
        'agender': [gfcat['number'], gfcat['case']],
        'masculine': [gfcat['number'], gfcat['case']],
        'feminine': [gfcat['number'], gfcat['case']],
        'neuter': [gfcat['number'], gfcat['case']],
    },
    numeral={
        'agender': [gfcat['number'], gfcat['case']],
        'masculine': [gfcat['number'], gfcat['case']],
        'feminine': [gfcat['number'], gfcat['case']],
        'neuter': [gfcat['number'], gfcat['case']],
    },
)

#   'owner_number':  ['dual', 'singular', 'plural']
#   'owner_gender':  ['masculine', 'neuter', 'feminine']


def ordered_grammar_name(
        *,
        v_form: str = None,
        case: str = None,
        person: str = None,
        number: str = None,
        gender: str = None,
        degree: str = None,
        clitic: str = None,
        return_type: str = "tuple"
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
    if return_type == "string":
        return concatenate_variables(
            v_form, case, person, number, gender, degree, clitic
        )
    else:
        types = [v_form, case, person, number, gender, degree, clitic]
        non_none_types = [item for item in types if item is not None]
        if return_type == "list":
            return non_none_types
        elif return_type == "tuple":
            return tuple(non_none_types)



def concatenate_variables(*items):
    """
    Concatenates variables into a string, separated by underscores, and
    ignoring empty strings.

    :param items: Arguments to concatenate.
    :return: Concatenated string.
    """
    out = "_".join(str(item) for item in items if item not in {None, "", " "})
    return out


def return_gram_feat_type(sample: str) -> Union[str, None]:
    """
    Takes a string and returns its grammar feature name.

    e.g.
        "first"      -> "person"

        "nominative" -> "case"

    :param sample: (str) sample word to check for feature type
    :return: string of feature type
    """
    gram_feat_dict = {
        'aspect': gfcat['aspect'],
        'number': gfcat['number'],
        'negative': gfcat['negative'],
        'case': gfcat['case'],
        'animate': gfcat['animate'],
        'definiteness': gfcat['definiteness'],
        'type': gfcat['word_type'],  # 'participle' removed!
        'person': gfcat['person'],
        'degree': gfcat['degree'],
        'vform': gfcat['vform'],
        'gender': gfcat['gender'],
        'form': gfcat['form'],
        'clitic': gfcat['clitic']
    }

    for key, values in gram_feat_dict.items():
        if sample == "no":
            lg.warning("'no' appears in two grammar features")
            return_value = "animate/negative"
            return ic([sample, return_value])[1]
        if sample == "yes":
            lg.info("'yes' appears in three grammar features")
            return_value = "clitic"
            return ic([sample, return_value])[1]
        if sample in values:
            if sample in {"participle"}:
                lg.warning('"participle" removed from "type" feature '
                           'for functionality')
            return key
    if sample not in {'form'}:
        lg.warning(f'"{sample}" not a known grammar feature.')
    return None


def de_critic(word: str, inpt: str = ''):
    """
    Strips diacritics off of Slovenian words (leaving carons)

    :param word: str to be stripped
    :param inpt: ignore
    :return: stripped str
    """
    # if word + if word[0] not in "čžšČŽŠ"
    if word:
        if word[0] not in "čžšČŽŠ":
            outpt = inpt + unidecode(word[0])
        else:
            outpt = inpt + word[0]
        return de_critic(word[1:], outpt)
    else:
        return inpt

def has_chars(test_text: str) -> bool:
    """
    Returns true if input string contains any characters a-z or č, ž, š
    :param test_text:
    :return:
    """
    return bool(re.search(r'[A-Za-zčžšČŽŠ]', test_text))


if __name__ == "__main__":
    return_gram_feat_type('yes')
