def janky_decorator_dict_gen():
    """
    Gives a format for krajšave dictionary for the purpose of simplifying the
    translation process by removing most frequent tokens

    :return: None
    """
    okrs = '''
    adm. administracija
    aer. aeronavtika
    agr. agronomija, agrotehnika
    ali prim.
    alp. alpinistika
    anat. anatomija
    ant. antonim; prim.
    antr. antropologija
    arheol. arheologija
    arhit. arhitektura
    astrol. astrologija
    astron. astronomija
    avt. avtomobilizem, avtomehanika
    bibl. biblijsko; prim.
    biblio. bibliotekarstvo
    biokem. biokemija
    biol. biologija
    bot. botanika
    brezoseb. brezosebno
    čeb. čebelarstvo
    čl. člen
    člen. členek
    daj. dajalnik
    dv. dvojina
    ed. ednina
    ekon. ekonomija
    ekspr. ekspresivno; prim.
    elektr. elektrotehnika
    elipt. eliptično; prim.
    etn. etnografija, etnologija
    evfem. evfemistično; prim.
    farm. farmacija, farmakologija
    filat. filatelija
    film. filmski izraz
    filoz. filozofija
    fin. finančništvo
    fiz. fizika
    fot. fotografija
    friz. frizerstvo
    gastr. gastronomija, kuharstvo
    geod. geodezija
    geogr. geografija
    geol. geologija
    geom. geometrija
    gl. glej
    glasb. glasba, muzikologija
    gled. gledališče
    gost. gostinstvo
    gozd. gozdarstvo
    grad. gradbeništvo
    igr. igre (za zabavo)
    im. imenovalnik
    in prim.
    ipd. in podobno
    iron. ironično; prim.
    itd. in tako dalje
    jezikosl. jezikoslovje
    kem. kemija
    knjiž. knjižno; prim.
    kor. koreografija
    kozm. kozmetika
    krat. kratica
    les. lesarska stroka
    lit. literarna teorija, literarna zgodovina
    ljubk. ljubkovalno; prim.
    lov. lovstvo
    m samostalnik moškega spola
    m. moški spol
    mat. matematika
    med. medicina
    medm. medmet
    mest. mestnik
    metal. metalurgija
    meteor. meteorologija
    min. mineralogija
    mitol. mitologija, zlasti slovanska
    mn. množina
    mont. montanistika
    nam. namenilnik
    nar. narečno; prim.
    nav. navadno
    navt. navtika, pomorstvo
    nedov. nedovršni glagol
    neprav. nepravilno; prim.
    nepreh. neprehodna raba (glagola)
    neskl. nesklonljiv(o)
    nizko prim.
    nižje_pog. nižje pogovorno; prim.
    num. numizmatika
    obl. oblačilna stroka
    obrt. obrtnišvo
    okrajš. okrajšava
    or. orodnik
    os. oseba
    otr. otroško; prim.
    oz. oziroma
    pal. paleontologija
    papir. papirništvo
    ped. pedagogika
    pesn. pesniško; prim.
    petr. petrografija, petrologija
    pisar. pisarniško, prim.
    pog. pogovorno; prim.
    polit. politika
    pooseb. poosebljeno; prim.
    povdk. povedkovnik
    pravn. pravni izraz
    predl. predlog
    preg. pregovor
    preh. prehodna raba (glagola)
    pren. preneseno; prim.
    prid. pridevnik, pridevniška raba
    prim. primerjaj
    prisl. prislov, prislovna raba
    psih. psihologija
    psiht. psihiatrija
    ptt pošta, telegraf, telefon
    publ. publicistično; prim.
    rač. računalništvo
    rad. radiotehnika, radiotelevizija
    rel. religija
    rib. ribištvo
    rod. rodilnik
    s samostalnik srednjega spola
    s. srednji spol
    sam. samostalniška raba; prim.
    simb. simbol
    slabš. slabšalno; prim.
    soc. sociologija
    star. starinsko; prim.
    stil. stilno; prim.
    strojn. strojništvo
    sv. svet(i)
    šah. šahovski izraz
    šalj. šaljivo; prim.
    šol. šolstvo
    šport. športni izraz
    štev. števnik
    teh. tehnika
    tekst. tekstilna stroka
    tisk. tiskarstvo
    tož. tožilnik
    trg. trgovina
    tudi prim.
    tur. turizem
    um. umetnost, umetnostna zgodovina
    urb. urbanizem
    usnj. usnjarstvo
    vet. veterina
    vez. veznik, vezniška raba
    voj. vojska
    vrt. vrtnarstvo
    vulg. vulgarno; prim.
    vznes. vzneseno; prim.
    zaim. zaimek
    zal. založništvo
    zastar. zastarelo; prim.
    zgod. zgodovina, zgodovinske pomožne vede
    zool. zoologija
    ž samostalnik ženskega spola
    ž. ženski spol
    žarg. žargon; prim.
    žel. železnica
    '''
    space_filler = "_"

    krs_output = {}
    for line in okrs.strip().split('\n'):
        words = line.strip().split(' ')
        krs_output[words[0].replace("_", " ")] = {
            'si': ' '.join(words[1:]),
            'en': None
        }

    print('{')
    for key, value in krs_output.items():
        print(f'\t{key}: {value},')
    print('}')

janky_decorator_dict_gen()