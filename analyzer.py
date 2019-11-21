import backend

from estnltk import Text
from estnltk.names import LAYER_CONLL
from errortypes import Type
from collections import namedtuple

Error = namedtuple("Error", ("text", "type", "verb", "synonyms"))


def sisend(tekstsisse):
    errorList = []

    # Tekstile tehakse süntaktiline analüüs
    syntaksitekst = Text(tekstsisse)
    syntaksitekst.tag_syntax()

    syntaks = []

    # Kogu tekstile, millele tehti süntaksanalüüs käiakse lausete kaupa läbi
    # iga lause kohta lisatakse järjendisse syntaks - lauses olevad sõnad, lauses olevate sõnade lemmad, süntaktilise funktsioonimärgendi ja
    # sõna süntaktilise ülema lauses, sõnavorm ja sõnaliik
    for sentence in syntaksitekst.split_by('sentences'):
        syntaks.append(list(
            zip(sentence.word_texts, sentence.lemmas, [x['parser_out'] for x in sentence[LAYER_CONLL]], sentence.forms,
                sentence.postags)))


    # Siin hakatakse syntaxi listi läbi käima
    # syntaksi listis olid elemendid lausete kaupa

    for lause in syntaks:

        # Siin olevad funktsioonid vajavad kantseliidi leidmiseks süntaktilist infot

        # olema + kesksona jaoks kutsutakse välja funktsioon kasonolemas
        # tagastatakse leitud sõnad mida märgendada, seletus kantseliidivormi kohta ja näitelaused
        # Küsime lõimelt kesksonasyntaks meetodi kasonolemas tagastatud informatsiooni

        kesksona = backend.kasonolemas(lause)
        # Käime tagastatud info läbi
        # Esimesel kohal 'kesksona[0]' on kõik erinevad lauseosad, mis vajavad märgendamist - on kantseliit
        for m in range(len(kesksona[0])):
            # tehakse märgend, olema + kesksona märgend on punane
            # textbox.tag_config(kesksona[0][m], background="red")
            errorWord = "".join(kesksona[0][m])
            errorList.append(Error(errorWord, Type.OLEMA_KESKSONA, "", soovitused.get(errorWord, []))._asdict())

            # Täpselt samamoodi nagu eelmisega, aga siin on tegemist kantseliitlike sõnade (ühendverbide) leidmisega
            # Et teada, kas tegemist on kantseliidiga nt "läbi viima" ja, et teada, kas "läbi" ülem on "viima" peame kontrollima süntaksit
            # küsime lõimelt funktsiooni syntaksileidmine tagastatud järjendi
            kantseliidivastus1 = backend.syntaksileidmine(lause)

            # järjendi esimesel kohal on lauseosad mis vajavad märgendit
            for m in range(len(kantseliidivastus1[0])):
                # Defineerime märgendi iga lauseosa jaoks
                # textbox.tag_config(kantseliidivastus1[0][m],background='lightgreen')
                print("kantseliidivastus1 : "+str(kantseliidivastus1))
                errorWord = "".join(kantseliidivastus1[0][m])
                errorList.append(Error(errorWord, Type.KANTSELIIT, kantseliidivastus1[2].strip(), soovitused.get(errorWord, []))._asdict())

        # Tegemist määrus saavas käändes kantseliidiga
        # samamoodi nagu eelmistel tehakse lõim
        maarussaavas = backend.kassaavolemas(lause)

        # Saame vastuse, kus maarussaavas on nüüd esimesel kohal lausest leitud kantseliitlikud lauseosad
        for m in range(len(maarussaavas[0])):
            # defineeritakse märgend selle kantseliidivormi jaoks
            # textbox.tag_config(maarussaavas[0][m],background="grey78")
            errorWord = "".join(maarussaavas[0][m])
            errorList.append(Error(errorWord, Type.SAAV_KAANE, "", soovitused.get(errorWord, []))._asdict())

        # Tegemist on nominalisatsiooniga. Siin ei otsita ühendverbe vaid tühiverbi + -mine vormi või sihitisega koos tühiverbe
        # samamoodi lõimedega nagu eelmised
        nom = backend.kasnomolemas(lause)

        # nom esimesel kohal on lauseosad mis vajavad märkimist
        for m in range(len(nom[0])):
            # tehakse märgend iga lauseosa jaoks
            # textbox.tag_config(nom[0][m],background = "bisque3")
            print("nom : "+str(nom))
            errorWord = "".join(nom[0][m])
            errorList.append(Error(errorWord, Type.NOMINALISATSIOON, nom[2].strip(), soovitused.get(errorWord, []))._asdict())


    # Kutsutakse backend failist välja meetod kokku. Seal meetodis arvutatakse kogu sõnade arv kogu tekstis

    # Järgnevad if laused on kantseliidi leidmiseks ilma süntaks analüüsita

    # kutsutakse failist backend välja meetod poolttarid ning argumendiks on kogu tekstikasti tekst
    poolttar = backend.poolttarind(tekstsisse)
    # funktsiooni tagastuses on esimsel kohal kõik leitud lauseosad
    for m in range(len(poolttar[0])):
        # iga lauseosa korral tehakse märgend ning kutsutakse välja search funktsioon, mis lisab märgendi tekstikasti
        # textbox.tag_config(poolttar[0][m],background="maroon1")
        errorWord = "".join(poolttar[0][m])
        errorList.append(Error(errorWord, Type.POOLT_TARIND, "", soovitused.get(errorWord, []))._asdict())

    # Kutsutakse välja meetod ltmaar, argumendiks on sisendtekst
    ltmaarsonad = backend.ltmaar(tekstsisse)
    # funktsiooni tagastuses on esimsel kohal kõik leitud lauseosad
    for m in range(len(ltmaarsonad[0])):
        # iga lauseosa korral tehakse märgend ning kutsutakse välja search funktsioon, mis lisab märgendi tekstikasti
        # textbox.tag_config(ltmaarsonad[0][m],background='yellow')
        errorWord = "".join(ltmaarsonad[0][m])
        errorList.append(Error(errorWord, Type.LT_MAARSONA, "", soovitused.get(errorWord, []))._asdict())

    # Kui eelnevalt kutsusime paar funktsiooni eraldi lõimede peal välja (*)
    # siis siin hakkame nende tagastatud järjenditega tegelema

    # saame lõimel kutsutud funktsiooni tagastamisväärtuse
    # nomthread oli nominalisatsiooni ühendverbide jaoks mõeldud
    nom = backend.nominalisatsioon(tekstsisse)
    # nomi esimesel kohal on kõik tagastatud lauseosad
    for m in range(len(nom[0])):
        # defineerime märgendi
        # textbox.tag_config(nom[0][m],background = "bisque3")
        print("nom : " + str(nom))
        errorWord = "".join(nom[0][m])
        errorList.append(Error(errorWord, Type.NOMINALISATSIOON, nom[2].strip(), soovitused.get(errorWord, []))._asdict())

    # Saame lõimel kutsutud funktsiooni väärtuse
    vastus = backend.analyys(tekstsisse)
    # esimesel kohal on kõik leitud paronüümid
    for m in range(len(vastus[0])):
        # seame iga sõna vastavusse värviga - defineerime märgendi
        # textbox.tag_config(vastus[0][m],background='lightblue')
        print("paronuum : " + str(vastus))
        errorWord = "".join(vastus[0][m])
        errorList.append(Error(errorWord, Type.PARONUUM, "", soovitused.get(errorWord, []))._asdict())

    # Leitud kantseliit - mitmus ainsuse asemel

    # selle kantseliidi jaoks pole eraldi lõime kasutatud
    # kutsutakse lihtsalt välja meetod mitmusanalyys failist backend
    mitmusains = backend.mitmusanalyys(tekstsisse)
    for m in range(len(mitmusains[0])):
        # Esimesel kohal on leitud kantseliitlikud sõnad
        # Iga sõna jaoks defineeritakse märgend ja värv
        # textbox.tag_config(mitmusains[0][m],background='pink3')
        errorWord = "".join(mitmusains[0][m])
        errorList.append(Error(errorWord, Type.LIIGNE_MITMUS, "", soovitused.get(errorWord, []))._asdict())

    # Leitud kantseliitlikud sõnad
    # Lõim pandi alguses käima (*)
    # saame lõime tagastusväärtuse
    kantseliidivastus = backend.kantsonanalyys(tekstsisse)
    # kantseliidivastuse esimesel kohal on kõik leitud sõnad
    for m in range(len(kantseliidivastus[0])):
        # igale sõnale defineeritakse märgend
        # textbox.tag_config(kantseliidivastus[0][m],background='lightgreen')
        print("kantseliidivastus : " + str(kantseliidivastus))
        errorWord = "".join(kantseliidivastus[0][m])
        errorList.append(Error(errorWord, Type.KANTSELIIT, kantseliidivastus[2].strip(), soovitused.get(errorWord, []))._asdict())

    return errorList


soovitused = {
    "eesmärgiks oli": ["eesmärk oli"],
    "erinevate": ["erisugune", "isesugune"]

}