# skladiste-inventura
Repozitorij za projekt iz kolegija Programiranje za web. Tema je sustav za upravljanje skladištem i inventurom. Na aplikaciji radi samo Benjamin Jakupović
---
# Glavne funkcionalnosti
- Korisnik se prijavljuje pomoću korisničkog imena i lozinke (+)
- Korisnik se može registrirati. registriranjem on definira svoje korisničko ime, e-mail,lozinku te svoje ime i prezime (+)
- Korisnik može unositi, brisati, uređivati i vidjeti kategorije proizvoda, u kojima se definira naziv kategorije te iznos PDV-a za tu kategoriju (+)
- Korisnik može unositi, brisati, uređivati i vidjeti jedinice mjere u kojima se količina proizvoda mjeri (+)
- Korisnik može dodavati nove proizvode (+)
- Korisnik može vidjeti sve proizvode (+) te if filtrirati po nazivu i količini 
- Korisnik može brisati i izmjenjivati samo proizvode koje je on dodao (+)

#TODO-s:
-Kada korisnik pokuša izbrisati jedinicu mjere/kategoriju referenciranu u proizvodu, umjesto da se aplikacija sruši, redirect na stranicu "Unallowed action - {description}"
-kada korisnik ažurira pdv za kategoriju, proći kroz se proizvode te kategorije te ažurirati sve cijene
-napraviti filter po nazivu i količini za proizvode
- ui design (htmx ili bootstrap)
-navigation top bar