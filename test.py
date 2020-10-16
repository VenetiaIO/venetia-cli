from bs4 import BeautifulSoup
text = ["""<li data-sizecm="23.0" data-sizeeu="35.5" data-sizeuk="3.5" data-sizeus="4.0" data-value="4.0">
35.5
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="23.5" data-sizeeu="36.5" data-sizeuk="4.0" data-sizeus="4.5" data-value="4.5">
36.5
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="23.5" data-sizeeu="37.5" data-sizeuk="4.5" data-sizeus="5.0" data-value="5.0">
37.5
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="24.0" data-sizeeu="38.5" data-sizeuk="5.5" data-sizeus="6.0" data-value="6.0">
38.5
<span class="product__available__pink">Pospiesz się, zostały tylko 2 sztuki</span>
</li>""", """<li data-sizecm="24.5" data-sizeeu="39.0" data-sizeuk="6.0" data-sizeus="6.5" data-value="6.5">
39.0
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="26.5" data-sizeeu="42.0" data-sizeuk="7.5" data-sizeus="8.5" data-value="8.5">
42.0
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="27.0" data-sizeeu="42.5" data-sizeuk="8.0" data-sizeus="9.0" data-value="9.0">
42.5
<span class="product__available__pink">Pospiesz się, została tylko 1 sztuka</span>
</li>""", """<li data-sizecm="27.5" data-sizeeu="43.0" data-sizeuk="8.5" data-sizeus="9.5" data-value="9.5">
43.0
<span class="product__available__pink">Pospiesz się, zostały tylko 2 sztuki</span>
</li>"""]

for s in text:
    soup = BeautifulSoup(s,"html.parser")
    print(soup.find('li')["data-sizeeu"])
