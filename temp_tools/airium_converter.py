from airium import from_html_to_airium, Airium

# assume we have such a page given as a string:
html_str = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>retinoblastom</title>
    <style>
        
body {
    font-family: Verdana, sans-serif;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 10px
}

.content {
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 20px;
    padding: 20px;
    overflow-x: auto;
}

.heading {
    background-color: #f2f2f2;
    padding: 10px 20px;
    margin: 0;
}

.inflection {
    width: 100%;
    border-collapse: collapse;
    padding: 0px
}

.inflection th, .inflection td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: center;
}

.inflection th {
    background-color: #f2f2f2;
}

.hidden {
    display: none;
}

.button {
    font-family: Verdana, sans-serif;
    background-color: #fa7d7d;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}

.button:hover {
    background-color: #7ac3ff;
}

.lineabove {
    border-top: 1px solid #ccc; /* Added line above */
    margin-top: 10px; /* Added margin top */
    margin-bottom: 6px;
    padding-top: 10px
}

.gray {
    font-family: Verdana, sans-serif;
    color:#838383
}

.pop-up {
    position: relative;
    cursor: pointer;
}

.pop-up .pop-up-content {
    visibility: hidden;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 8px;
    position: absolute;
    z-index: 1;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    white-space: nowrap; /* Prevent text wrapping */
    width: max-content; /* Adjust width to fit content dynamically */
}

.pop-up:hover .pop-up-content {
    visibility: visible;
    opacity: 1;
}

    </style>
</head>

<body>
    <div class="container">
        <button class="button" onclick="toggleTable('inflection_retinoblastom')">Inflections</button>
        
        <div class="content hidden" id="inflection_retinoblastom">
            <p class="heading"> 
                <b>
                    <em>
                        noun
                    </em>
                </b>; 
                <em>
                    common
                </em>, 
            <em>masculine</em>
            <table class="inflection">
                <tr>
                    <th></th>
                    <th>singular</th>
                    <th>dual</th>
                    <th>plural</th>
                </tr>
                <tr>
                    <th>nom.</th>
                    <td title="nom sg" class="pop-up">retinoblastom<span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːm<br>ɾɛtinɔblaˈstoːm</span></td>
                    <td title="nom dl" class="pop-up"><span class=gray>retinoblastom<b>a</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːma<br>ɾɛtinɔblaˈstoːma</span></td>
                    <td title="nom pl" class="pop-up"><span class=gray>retinoblastom<b>i</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmi<br>ɾɛtinɔblaˈstoːmi</span></td>
                </tr>
                <tr>
                    <th>gen.</th>
                    <td title="gen sg" class="pop-up">retinoblastom<b>a</b><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːma<br>ɾɛtinɔblaˈstoːma</span></td>
                    <td title="gen dl" class="pop-up"><span class=gray>retinoblastom<b>ov</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔu̯<br>ɾɛtinɔblaˈstoːmɔu̯</span></td>
                    <td title="gen pl" class="pop-up"><span class=gray>retinoblastom<b>ov</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔu̯<br>ɾɛtinɔblaˈstoːmɔu̯</span></td>
                </tr>
                <tr>
                    <th>dat.</th>
                    <td title="dat sg" class="pop-up"><span class=gray>retinoblastom<b>u</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmu<br>ɾɛtinɔblaˈstoːmu</span></td>
                    <td title="dat dl" class="pop-up"><span class=gray>retinoblastom<b>oma</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔma<br>ɾɛtinɔblaˈstoːmɔma</span></td>
                    <td title="dat pl" class="pop-up"><span class=gray>retinoblastom<b>om</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔm<br>ɾɛtinɔblaˈstoːmɔm</span></td>
                </tr>
                <tr>
                    <th>acc.</th>
                    <td title="acc sg" class="pop-up">retinoblastom<span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːm<br>ɾɛtinɔblaˈstoːm</span></td>
                    <td title="acc dl" class="pop-up"><span class=gray>retinoblastom<b>a</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːma<br>ɾɛtinɔblaˈstoːma</span></td>
                    <td title="acc pl" class="pop-up"><span class=gray>retinoblastom<b>e</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɛ<br>ɾɛtinɔblaˈstoːmɛ</span></td>
                </tr>
                <tr>
                    <th>loc.</th>
                    <td title="loc sg" class="pop-up">retinoblastom<b>u</b><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmu<br>ɾɛtinɔblaˈstoːmu</span></td>
                    <td title="loc dl" class="pop-up"><span class=gray>retinoblastom<b>ih</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmix<br>ɾɛtinɔblaˈstoːmix</span></td>
                    <td title="loc pl" class="pop-up"><span class=gray>retinoblastom<b>ih</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmix<br>ɾɛtinɔblaˈstoːmix</span></td>
                </tr>
                <tr>
                    <th>ins.</th>
                    <td title="ins sg" class="pop-up"><span class=gray>retinoblastom<b>om</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔm<br>ɾɛtinɔblaˈstoːmɔm</span></td>
                    <td title="ins dl" class="pop-up"><span class=gray>retinoblastom<b>oma</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmɔma<br>ɾɛtinɔblaˈstoːmɔma</span></td>
                    <td title="ins pl" class="pop-up"><span class=gray>retinoblastom<b>i</b></span><span class="pop-up-content">Pronunciation:<br>ɾɛˈtiːnɔblaˈstoːmi<br>ɾɛtinɔblaˈstoːmi</span></td>
                </tr>
            </table>

            <function gigafida_footer at 0x000001D221F0C220>
        </div>
    </div>

    <script>
        function toggleTable(id) {
            var element = document.getElementById(id);
            element.classList.toggle("hidden");
        }
    </script>
</body>
</html>
"""

# to convert the html into python, just call:

py_str = from_html_to_airium(html_str)

a = Airium()

a('<!DOCTYPE html>')
with a.html(lang='en'):
    with a.head():
        a.meta(charset='UTF-8')
        a.meta(content='width=device-width, initial-scale=1.0', name='viewport')
        a.title(_t='retinoblastom')
        with a.body():
            with a.div(klass='container'):
                a.button(klass='button', onclick="toggleTable('inflection_retinoblastom')", _t='Inflections')
                with a.div(klass='content hidden', id='inflection_retinoblastom'):
                    with a.p(klass='heading'): ###
                        with a.b():
                            a.em(_t='noun')
                        a(';')
                        a.em(_t='common')
                        a(',')
                        a.em(_t='masculine')
                        with a.table(klass='inflection'):
                            with a.tr():
                                a.th()
                                a.th(_t='singular')
                                a.th(_t='dual')
                                a.th(_t='plural') ##
                            with a.tr():
                                a.th(_t='nom.') ####
                                with a.td(klass='pop-up', title='nom sg'): #@
                                    a('retinoblastom')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːm')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːm')
                                with a.td(klass='pop-up', title='nom dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='a')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːma')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːma')
                                with a.td(klass='pop-up', title='nom pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='i')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmi')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmi')
                            with a.tr():
                                a.th(_t='gen.')
                                with a.td(klass='pop-up', title='gen sg'):
                                    a('retinoblastom')
                                    a.b(_t='a')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːma')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːma')
                                with a.td(klass='pop-up', title='gen dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='ov')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔu̯')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔu̯')
                                with a.td(klass='pop-up', title='gen pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='ov')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔu̯')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔu̯')
                            with a.tr():
                                a.th(_t='dat.')
                                with a.td(klass='pop-up', title='dat sg'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='u')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmu')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmu')
                                with a.td(klass='pop-up', title='dat dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='oma')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔma')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔma')
                                with a.td(klass='pop-up', title='dat pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='om')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔm')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔm')
                            with a.tr():
                                a.th(_t='acc.')
                                with a.td(klass='pop-up', title='acc sg'):
                                    a('retinoblastom')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːm')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːm')
                                with a.td(klass='pop-up', title='acc dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='a')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːma')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːma')
                                with a.td(klass='pop-up', title='acc pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='e')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɛ')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɛ')
                            with a.tr():
                                a.th(_t='loc.')
                                with a.td(klass='pop-up', title='loc sg'):
                                    a('retinoblastom')
                                    a.b(_t='u')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmu')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmu')
                                with a.td(klass='pop-up', title='loc dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='ih')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmix')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmix')
                                with a.td(klass='pop-up', title='loc pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='ih')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmix')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmix')
                            with a.tr():
                                a.th(_t='ins.')
                                with a.td(klass='pop-up', title='ins sg'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='om')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔm')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔm')
                                with a.td(klass='pop-up', title='ins dl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='oma')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmɔma')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmɔma')
                                with a.td(klass='pop-up', title='ins pl'):
                                    with a.span(klass='gray'):
                                        a('retinoblastom')
                                        a.b(_t='i')
                                    with a.span(klass='pop-up-content'):
                                        a('Pronunciation:')
                                        a.br()
                                        a('ɾɛˈtiːnɔblaˈstoːmi')
                                        a.br()
                                        a('ɾɛtinɔblaˈstoːmi')
                        a.function(at='', gigafida_footer='', **{'0x000001d221f0c220': ''})
            with a.script():
                a('function toggleTable(id) {\n            var element = document.getElementById(id);\n            element.classList.toggle("hidden");\n        }')


if __name__ == '__main__':
    d = {"h":"hi"}

    k = d["r"] if d["r"] else None

    ic(k)