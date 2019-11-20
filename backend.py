# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:06:16 2017

@author: PC
"""
from estnltk import Text

from pprint import pprint
import string


#Meetod mis arvutab mitu sõna tekstis on
#sisend on kogu tekstikasti tekst
def kokku(tekstisse):
    #Kõikide sõnade loendamiseks
    #eemaldan kirjavahemärgid ning tagastan kõikide sõnade listi suuruse
    text = Text(tekstisse)

    sonad = text.word_texts
    uus = [w.rstrip( string.punctuation) for w in sonad ]
    uus = [s for s in uus if s]
 
    return len(uus)
    
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------
#Meetod millega loetakse informatsioon sisse tekstifailist maarussaavas.txt
def teemaarus():
    f=open('failid/maarussaavas.txt',encoding='utf-8')
    read = f.readlines()
    #esimesel real on mõiste
    #teiste ridade peal on näited
    #splititakse '|', sest vasakul pool sellest on näitelause, kus kantseliit on sees ja paremal pool on sama lause aga ilma kantseliidita
    #näitelaused ja moisted tagastatakse
    moiste=read[0]
    naited = []
    for rida in read[1:]:
        naited.append(rida.split('|'))
    return (moiste,naited)
    
global maarus
#teen globaalmuutuja maarus
#siis saan igalt poolt kätte eelmises funktsioonis loodud mõiste ja näitelaused
maarus = teemaarus()


def kassaavolemas(lause):
    #sisse tuleb süntaktilise analüüsiga lause
    tagastamine = []
    #saame moiste ja näitelaused globaalmuutujast
    moiste = maarus[0]
    naited = maarus[1]
    
    tagastamissonad = []
    #kaotame argumendist tühjad väljad
    lause = [x for x in lause if x]  
    #Käin kõik syntaksi listi läbi. Iga listi element koosneb sõnast,lemmast,süntaksist, sõnavormist ja sõnaliigist
    for i in range(len(lause)):
        #kui leitakse määrsõna ning vaadatakse kas tema ülemus on 'olema'
        #kui on, siis lisatakse nende sõnade indeksid tagastamise listi
        
        if(lause[i][2][0][0] == "@ADVL" and 'tr' in lause[i][3].split(" ") ):
            #print(lause[lause[i][2][0][1]])
            if('olema' in lause[lause[i][2][0][1]][1].split('|')):
                tagastamine.append([min(i,lause[i][2][0][1]),max(i,lause[i][2][0][1])])
                
       #tagastamise list käiakse läbi ning indeksite kohtade peal ja indeksite vahel olevad sõnad lisatakse tagastamissõnadesse         
    for paar in tagastamine:
        kohaliklause= []
        for alguslopp in range(paar[0],paar[1]+1):
            kohaliklause.append(lause[alguslopp][0])
        tagastamissonad.append(" ".join(kohaliklause))
    #tagastatakse lauseosa mis tuleb märkida, saavas käändes määruse kantseliidimõiste ning näitelaused
    return [tagastamissonad,moiste,naited]
                         
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------

def teepool():
    #loetakse pool-tarindi kohta info sisse
    f=open("failid/poolttarind.txt",encoding = "utf-8")
    read = f.readlines()
    #esimesel real on mõiste
    #teistel ridadel on näitelaused
    #splititakse ";" kohalt, kus vasakul pool on laused, kus on kantseliit sees ja paremal pool on samad laused, aga ilma kantseliidita
    moiste = read[0]
    naited = []
    for rida in read[1:]:
        naited.append(rida.split(";"))
        #moiste ja näited tagastatakse
    return (moiste,naited)

#teen globaalse muutuja, mis saab funktsiooni teepool tagastatud väärtuse 
global pool
pool = teepool()

def poolttarind(tekstsisse):
    #poolt-tarindi puhul tuleb kogu tekstikastis olev tekst argumendina
    moiste = pool[0]
    naited = pool[1]
    
    tagastamissonad = []
    tekst = Text(tekstsisse.lower())
    tekst = tekst.sentence_texts
    #käime teksti lausete kaupa läbi
    for lause in tekst:
        lause = Text(lause)
        kaane = lause.tag_analysis()['words']
        #käime lause sõnade kaupa läbi
        for words in range(len(lause.word_texts)):
            #kui lausest leitakse sõna poolt, siis vaadatakse eelneva sõna käänet
            if(lause.word_texts[words]=='poolt'):
                try:
                    #kui eelmine sõna oli 'g' ehk omastavad käändes, siis tagastatakse omastavas käändes sõna ja sõna poolt
                    if(kaane[words-1]['analysis'][0]['form'].split(" ")[1] =='g'):
                        tagastamissonad.append(lause.word_texts[words-1]+" "+lause.word_texts[words])
                except:
                    continue
    return [tagastamissonad,moiste,naited]
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------

#Samamoodi nagu eelmised meetodid
#loetakse fail sisse, et globaalsetesse muutujatele anda edasi moiste ja näitelaused
def teekesksona():
    f=open("failid/olemakesksona.txt",encoding="utf-8")
    read = f.readlines()
    
    moiste = read[0]
   
    tagastamisseletused=[]
    for rida in read[1:]:
        tagastamisseletused.append(rida.split("|"))
    return (moiste,tagastamisseletused)
    
global kesk
kesk = teekesksona()
  
#Otsib olema + kesksõna, mille lõpus on "tav" või "v" ning tagastab selliste paaride indeksid
def kasonolemas(lause):
    
    moiste = kesk[0]
    tagastamisseletused = kesk[1]
    tagastamissonad = []
    
    tagastamine = []
    #Käin sissetulnud syntaksi listi läbi. Iga listi element koosneb sõnast,lemmast,süntaksist, sõnavormist ja sõnaliigist
    
     #Kui leitakse sõna mis on predikaat ja mis lõppev 'tav' või 'v'-ga
    #Siis vaadatakse, kas ta ülemuse lemma on 'olema'   
    for i in range(len(lause)):       
        if(lause[i][2][0][0] == '@PRD' and (lause[i][1].endswith('tav') or lause[i][1].endswith('v'))):
            if('olema' in lause[lause[i][2][0][1]][1].split('|')):
                #kui leiti olema + kesksona
                #siis vaadatakse tagastamise listi, seal on indeksid, kust leidi olema ja kust leidi kesksõna
                #nende indeksite kohal olevad sõnad ja vahel olevad sõnad lisatakse tagastamislisti
                tagastamine.append([min(i,lause[i][2][0][1]),max(i,lause[i][2][0][1])])
    
    if(tagastamine):
        for paar in tagastamine:
            kohaliklause= []
            for alguslopp in range(paar[0],paar[1]+1):
                kohaliklause.append(lause[alguslopp][0])
            tagastamissonad.append(" ".join(kohaliklause))                 
            
         
    return [tagastamissonad,moiste,tagastamisseletused]
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------
def teenom():
    #teenom meetod põhimõte on sama, mis eelmistel tekstifailidest lugemise meetodid
    
    sonastik = {}
    f = open("failid/nominalisatsioon.txt",encoding="utf-8")
    moisted = []
    esimesedsonad=[]
    naited = []
    kohalikudnaited = []
    #käiakse ridu failist läbi
    for lines in f:
        #eemaldatakse veidrad sümbolid
        lines = lines.replace('\xad',"")
        esimenesona=""
        moiste = ""
        #kui rida pole tühi
        if(lines != "\n"):
            #kui real on täpp
            if("•" in lines):
                for p in lines:
                    #failis on sõna - sõna seletus
                    #sõnad on alati väikese tähega
                    #kui pole suur täht, on tegemist sõnaga
                    if(not p.isupper()):
                        esimenesona += p
                    else:
                        #mõiste on sõnast edasine tekst
                        moiste = lines[len(esimenesona):].replace('\n',"")
                        moisted.append(moiste)
                        break
            #sõnast eemaldatakse üleliigsed sümbolid
            #sõna lisatakse listi
            esimenesona = esimenesona.replace("\t","")[2:len(esimenesona)-4]
            esimesedsonad.append(esimenesona)
            #kui täppi pole real, siis on tegemist näitelaused
            #lisatakse näitelause listi
            if("•" not in lines):
                lines = lines.replace('\n',"")
                lines = lines.split(";")
                kohalikudnaited.append(lines)
            else:
                naited.append(kohalikudnaited) 
                kohalikudnaited=[]
    esimesedsonad = list(filter(None,esimesedsonad))
       
  
    liitsonad = []
    kahesedsonad=[]#kantseliilikud sõnad, mis on kahe sõnaga - aset leidma
    
    #tehakse sõnastik, kus võti on sõna ning väärtuses on selle sõna seletus ja sõna näitelaused.
    for i in range(len(esimesedsonad)):
        if(len(esimesedsonad[i].split(" "))==2):#kui " " splittides on pikkus kaks, siis on tegemis kahe sõna pikkuse sõnaga
            kahesedsonad.append(esimesedsonad[i])
        if("-" == esimesedsonad[i][0]):
            liitsonad.append(esimesedsonad[i])
        kokku = [esimesedsonad[i].upper()+" - "+moisted[i]]+naited[i+1]
        sonastik[esimesedsonad[i]]=kokku
    return (sonastik,kahesedsonad)

global nomin
nomin = teenom()    
        
def nominalisatsioon(tekstsisse):
    #see nominalisatsiooni meetod otsib sõnaaknaid ühendverbidele jaoks nt "aset leidma"
    #argument on kogu tekstikasti tekst
    sonastik = nomin[0]
    kahesedsonad = nomin[1]
    
    tekst = Text(tekstsisse.lower())
    kantseliit = []
    seletused = []
    uuedkahesedsonad = []
    
    for m in kahesedsonad:
        uuedkahesedsonad.append(m.split(" "))
    
    #Käiakse sisendtekst lausetena läbi
    #leitakse lemmad
    tekst = tekst.sentence_texts
    for i in tekst:
        i =Text(i)
        i.tag_analysis()
        lausesonad = i.word_texts
        lauselemmad = []
        #käime iga lause sõnadena läbi
        #lisame iga sõna lemma listi
        for m in lausesonad:
            m = Text(m)
            m.tag_analysis()
            
            if( '|' in m.lemmas[0]):    
                lauselemmad.append(m.lemmas[0].split('|')[0])
                lauselemmad.append(m.lemmas[0].split('|')[1])
            else:
                lauselemmad.append(m.lemmas[0])
        #käime lause sõnade kaupa läbi                
        for m in range(len(lausesonad)):
            #käime ühendverbe läbi
            #sonapaar[0] on esimene sõna
            #sonapaar[1] on teine sõna
            #nt vastavalt aset ja leidma
            for sonapaar in uuedkahesedsonad:   
                #kui esimene sõna võrdub hetkel käes oleva sõnaga 
                if (sonapaar[0] == lausesonad[m] and sonapaar[1] in lauselemmad):
                    try:
                        #siis vaatame selle sõna ümbert sõnu
                        for lahedus in range(m-3,m+3):
                            #Kui 3 sõna läheduses leidub ühendverbi teine sõna
                            if(lauselemmad[lahedus] == sonapaar[1]):
                                
                                lause = ""
                                #siis lisame kõik sõnad mis on ühendverbi sõnade vahel tagastamislisti ehk kantseliidi listi
                                for arv in range(min(lahedus,m),max(lahedus,m)+1):
                                    lause +=lausesonad[arv]+" "
                                #kui lausesonadest[m] oli sõna "aset", siis muudame selle nüüd teiseks sümboliks
                                #ja kui lauselemmad[lahedus] oli "leidma", siis muudame ka selle teiseks sümboliks
                                #seda tehakse sellepärast, et oleks võimalik lausest leida ka teisi selliseid sõnaaknaid ja need ei omavahel ei kattuks
                                lausesonad[m] ='#'
                                lauselemmad[lahedus] = '#'
                                seletused.append(sonastik[sonapaar[0]+" "+sonapaar[1]])
                                kantseliit.append(lause[:-1])
                    except:
                        continue
     
                    
    #leitud lauseosa tagastatakse ning seletused tagastakse       
    return ([kantseliit,seletused])
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------
#tekstifailist saadud informatsioon loetakse sisse
def teemitmus():
    f = open("failid/mitmus.txt", encoding ='utf-8')
    koik = f.readlines()
    #esimesel real on mõiste
    moiste = koik[0]
    sonad = []
   
    seletused = []
    kindlasonaseletused = []
    #järgmise for tsükliga loetakse sisse tekstifailist seletused ja sõnad
    for m in koik [1:]:
        
        #kui üks sõna, siis tegemist sonaga
        if(len(m.split(" "))==1 and m!="\n"):
            if(len(kindlasonaseletused)>0):
                seletused.append(kindlasonaseletused)
            kindlasonaseletused = []
            sonad.append(m.strip("\n"))
        else:
            m=m.strip("\n")
            kindlasonaseletused.append(m.split("|"))
    seletused.append(kindlasonaseletused)
    #sonad,seletused ja moiste tagastatakse
    return (sonad,seletused,moiste)

global mitmus
mitmus = teemitmus()
#globaalne muutuja mitmus saab eelmise funktsiooni tagastuse väärtuse

def mitmusanalyys(tekstsisse):
    #argumendina tuleb sisse kogu tekstikasti tekst
    
    sonad = mitmus[0]
    seletused = mitmus[1]
    moiste = mitmus[2]
    sonadelemmad = []
    
    #käime tekstifaili sõnad läbi
    #lisame sõnade lemmad sonadelemma listi
    for sona in sonad:
        sona = Text(sona)
        if('|' not in  sona.lemmas):
            sonadelemmad.append(sona.lemmas[0])
        else:
            sonadelemmad.append(sona.lemmas.split('|')[0])
            sonadelemmad.append(sona.lemmas.split('|')[1])
     
    tekst = Text(tekstsisse.lower())
  
    
    #tekst.tag_analysis()
    tekstisonad = tekst.word_texts
    
    lemmad = tekst.lemmas
    
    tagastamissonad = []
    tagastamisseletused = []
    
    #Praegu on tekstifailis ainult sõnad "arengud" ja "tegevused"
    # Nende leidmiseks otsin lemmade hulgat sõna "areng" või "tegevus" ning vaatan kas nad on mitmuses või ei.
    for i in range(len( lemmad)):
        tekstisonad[i] = Text(tekstisonad[i])
        for lemma in sonadelemmad:
            
            if(lemma in lemmad[i].split('|') and tekstisonad[i].analysis[0][0]['form'].split(" ")[0] == 'pl'): 
                #kui sõna leiti ja ta on mitmuses lisatakse nad tagastamislisti
                tagastamissonad.append(tekstisonad[i]['text'])
                tagastamisseletused.append(seletused[sonadelemmad.index(lemma)])
            
   
            
    return [tagastamissonad,moiste,tagastamisseletused]
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------            
#ltmäärsõnade kohta loetakse failist sisse
def teeltmaar():
    naited=[]
    f = open("failid/ltmaarsonad.txt",encoding="utf-8")
    koik = f.readlines()
    moiste = koik[0]
    for m in koik[1:]:
        naited.append(m.split('|'))
        #tagastatakse moiste ja näitelaused
    return (moiste,naited)
  
global lt
lt = teeltmaar()   
    
          
def ltmaar(tekstsisse):
    #sisse tuleb tekstikasti kogu tekst
    moiste = lt[0]
    naited = lt[1]
    
    tagastamine = []
    tekst = Text(tekstsisse.lower())
    #käime teksti sõna haaval läbi
    for i in tekst.word_texts:
        #need neli sõna olid juba kantseliidi sõnade peatükkis. Pole vaja kahekordselt lt- määrsõnu märkida.
        if(i!='juhinduvalt' and i!= 'jätkuvalt' and i!='järgselt' and i!= 'praktiliselt'):
            text = Text(i)
           
            #Kui sõna lõppeb "seltiga"
            if(text.endswith("selt")):
                #Siis võetkase sõnalt "selt" lõpust ära ning vaadatakse mis sõnaliik ta on. Kui oli näiteks sõna "koheselt" ja "kohe" on määrsõna siis see lisatakse
                #nii tegime kindlaks, et tegemist on ületuletamisega
                yletuletus = Text(i[:-4])
                yletuletus .tag_analysis()
                
                nelopuline = Text(i[:-2])
                nelopuline.tag_analysis()
                                
                try:
                    if(yletuletus .postags[0]=="D"):
                        tagastamine.append(i)
                
                #Võtan liitsõna juppideks ning vaatan kas viimane jupp lõppeb sõnaga 'ne' näiteks veelkordselt -> veelkordse -> saadakse [veel,kordne]
                    elif (nelopuline.analysis[0][0]['root_tokens'][len(nelopuline.analysis[0][0]['root_tokens'])-1] in ["aastane","kuine","ringne","kordne"]):
                    
                        tagastamine.append(i)
                except:
                    continue
 
    return [tagastamine,moiste,naited]
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------                          
#tehakse täpselt samamoodi nagu nominalisatsiooni sisselugemisel
#ainult, et siin tagastatakse ka liitsõnad
#näiteks sõna "-alane" korral on tegemist liitsõnaga

def teekants():
    sonastik = {}
    f = open("failid/kantseliidisonad.txt",encoding="utf-8")
    moisted = []
    esimesedsonad=[]
    naited = []
    kohalikudnaited = []
    for lines in f:
        lines = lines.replace('\xad',"")
        #eemaldan pdfist tulnud veidra märgi
        esimenesona=""
        moiste = ""
        if(lines != "\n"):
            if("•" in lines):
                for p in lines:
                    if(not p.isupper()):
                        esimenesona += p
                    else:
                        moiste = lines[len(esimenesona):].replace('\n',"")
                        moisted.append(moiste)
                        break
            esimenesona = esimenesona.replace("\t","")[2:len(esimenesona)-4]
            esimesedsonad.append(esimenesona)
            if("•" not in lines):
                lines = lines.replace('\n',"")
                lines = lines.split(";")
                kohalikudnaited.append(lines)
            else:
                naited.append(kohalikudnaited) 
                kohalikudnaited=[]
    esimesedsonad = list(filter(None,esimesedsonad))
    liitsonad = []
    kahesedsonad=[]#kantseliilikud sõnad, mis on kahe sõnaga - läbi viima

    for i in range(len(esimesedsonad)):
        if(len(esimesedsonad[i].split(" "))==2):#kui " " splittides on pikkus kaks, siis on tegemis kahe sõna pikkuse sõnaga
            kahesedsonad.append(esimesedsonad[i])
        if("-" == esimesedsonad[i][0]):
            liitsonad.append(esimesedsonad[i])
        kokku = [esimesedsonad[i].upper()+" - "+moisted[i]]+naited[i+1]
        sonastik[esimesedsonad[i]]=kokku
    return(kahesedsonad,sonastik,liitsonad)
global kants
kants = teekants()
    
    
def kantsonanalyys(tekstsisse):
    #argumendina tuleb sisse terve tekstikasti tekst
    
    kahesedsonad = kants[0]
    sonastik = kants[1]
    liitsonad = kants[2]
    kantseliit = []
    seletused = []
    tekst = Text(tekstsisse.lower())    
    #Uued kahesedsõnad - ntks sõnad läbi viima ja paika panema pannakse listi kujul [[paika,panema],[läbi,viima]]
    uuedkahesedsonad = []
    for m in kahesedsonad:
        uuedkahesedsonad.append(m.split(" "))
          
    #sisendteksti käiakse sõna haaval läbi
    for i in tekst.word_texts:
        text = Text(i)
        text.tag_analysis()
        
        #liitsõnade listis on praegu element "-alane"
        #iga liitsõna korral, mis listis on vaadatakse, kas käesoleva sõna lemma ei lõppe selle liitsõna lõpuga (näiteks, kas käesoleva sõna lemma ei lõppe -alane'ga)
        for p in liitsonad: 
            try:
                lemma=text.lemmas[0]
            except:
                lemma= text.lemmas[0].split("|")[1]
            if(i.endswith(p[1:]) or lemma.endswith(p[1:])):
                kantseliit.append(i)
                seletused.append(sonastik[p])
                
        #kui käesolev sõna on kantseliidi sõnastikus olemas
        if(i in sonastik and i not in kantseliit and sonastik[i] not in seletused):
            #lisatakse kohe sõna tagastamise listi
            kantseliit.append(i)
            seletused.append(sonastik[i])
        else:
            try:
                lemma=text.lemmas[0]
            except:
                lemma= text.lemmas[0].split("|")[1]
            #siis vaadatakse üle kas sõna lemma on sõnastikus olemas, kui on lisatakse tagastamislisti
            if(lemma in sonastik):
                
                kantseliit.append(i)
                seletused.append(sonastik[lemma])
               
    return ([kantseliit,seletused])
    
def syntaksileidmine(lause):
    #syntaks analüüsiga lause tuleb sisse
    #kahesedsonad on kantseliidisõnade tekstifailidst leitud ühendverbid
    #sonastik on kantseliidisõnade tekstifaili põhjal tehtud sõnastik, kus võti on sõna ja väärtus on seletus
    kahesedsonad = kants[0]
    sonastik = kants[1]
    
    
    seletused = []
    kantseliit = []
    
    #uuedkahesedsõnad - teeme listi, kus on ühendverbid eraldatud nt ('Läbi','viima')
    uuedkahesedsonad = []
    for m in kahesedsonad:
        uuedkahesedsonad.append(m.split(" "))
    
    #igaksjuhuks eemaldame süntaktilise analüüsiga tehtud lausest tühjad väljad
    lause = [x for x in lause if x]  
    #Käin sõnapaarid läbi nt [("läbi","viima"),("....","..."),....]
    for sonapaar in uuedkahesedsonad:
        tagastamine = []
        #sona1 võrdub siis ühendverbi esimese sõnaga
        #sona2 teise sõnaga
        sona1 = sonapaar[0]
        sona2 = sonapaar[1]
        #Käin kõik syntaksi listi läbi. Iga listi element koosneb sõnast,lemmast,süntaksist, sõnavormist ja sõnaliigist
        for i in range(len(lause)):
            #kui leitakse sõna, mis on sama, mis ühendverbi esimene sõna, siis vaadatakse selle ülemust,
            #Kui ülemus ühendverbi teine sõna, siis lisatakse nende sõnade indeksid tagastamise listi
            if(lause[i][1] == sona1 or lause[i][0] == sona1):   
            
                if(sona2 in lause[lause[i][2][0][1]][1].split('|')):
                    tagastamine.append([min(i,lause[i][2][0][1]),max(i,lause[i][2][0][1])])
                 
        #Tagastamise list käiakse läbi ning indeksite kohal olevad sõnad ning indeksite vahel olevad sõnad pannakse ühte listi
        #tagastame kantseliitliku vormi
        if(tagastamine):
             for m in tagastamine:
                tagastamislause=""
                for s in range(m[0],m[1]+1):
                   
                    tagastamislause+=lause[s][0]+" "
                
                seletused.append(sonastik[sonapaar[0]+" "+sonapaar[1]])
                kantseliit.append(tagastamislause[:-1])
    
    #Tagastame kõik leitud kantseliitlikud lauseosad ja nende seletused      
    return ([kantseliit,seletused])
#Splitter --------------------------------------------------------------------------------------------------------------------------------------------- 
#Loetakse sisse paronüümide txt failidst
def teeanalyys():
    sonastik = open("failid/parosonastik.txt",encoding="utf-8")
    sonaraamat = {}
    sonad=[]
    tahendused=[]
    #Esimest rida ei võeta arvesse, see on tühi rida
    #loetakse sõnad sisse
    #iga sõna pannakse sõnaraamatusse, kus võti on sõna ja väärtus on paronüümigrupp
    #tekstifailis on paronüümigrupid vahega eraldatud
    esimenerida =0
    for lines in sonastik:
        esimenerida+=1
        
        if(lines != '\n'and esimenerida!=1):
            esimenesona = (lines.split(' ',1)[0])
            
            if(esimenesona != ""):
                sonad.append(lines.split(' ',1)[0])
            tahendus = esimenesona.upper()+" -"
            tahendused.append(tahendus+lines[len(esimenesona):].replace('\n',""))
        if(lines == '\n' and esimenerida!=1):
            for sona in sonad:
                sonaraamat[sona]='\n'.join(tahendused)
            sonad = []
            tahendused = []
    return sonaraamat
global paron
paron = teeanalyys()  

#paronüümide korral tuleb kogu tekst argumendina sisse
def analyys(tekstsisse):
    sonaraamat = paron
    tekst = Text(tekstsisse.lower())
    #leitud paronyymid
    paronyymid = []
    seletused = []
    
    #Käin sisendteksti sõnade kaupa läbi
    for i in tekst.word_texts:
        text = Text(i)
        text.tag_analysis()
        teinelemma = ""
        #teen lemmade listi
        #Osadel sõnadel on kaks lemmat
        if("|" in text.lemmas[0]):
            lemma = text.lemmas[0].split("|")[1]
            teinelemma = text.lemmas[0].split("|")[0]
        elif("|" not in text.lemmas[0]):
            lemma = text.lemmas[0]  
            
        #Otsin sõnaraamatust, kui lemma on sõnaraamatus olemas, siis see lisatakse tagastmishulka, kui algne sõna (mitte lemma) leitakse 
        #sõnaraamatust siis lisatakse see tagastamishulka
        
        if(lemma in sonaraamat ):
            paronyymid.append(i)
            seletused.append(sonaraamat[lemma])
        elif(i in sonaraamat):
            paronyymid.append(i)
            seletused.append(sonaraamat[i])
        elif(teinelemma in sonaraamat ):
            paronyymid.append(i)
            seletused.append(sonaraamat[teinelemma])

    return ([paronyymid,seletused])
#Splitter ---------------------------------------------------------------------------------------------------------------------------------------------             

    
def kasnomolemas(lause):
    #see funktsioon on nominalisatsiooni leidmine süntaksiga
    #sisse tuleb lause millele on süntaktiline analüüs tehtud
    seletused = []
    kantseliit = []
    sonastik = nomin[0]
    
    #kaotan lausest tühjand elemendid
    lause = [x for x in lause if x]  
        
      #käiakse tühiverbidle hulk läbi
    
    for verb in list(sonastik):
        tagastamine = []
        #Käin kõik syntaksi listi läbi. Iga listi element koosneb sõnast,lemmast,süntaksist, sõnavormist ja sõnaliigist
        for i in range(len(lause)):

            
            sonalemmad = lause[i][1].split('|')
            for sona in sonalemmad:
                #Esimesena kui leitakse mõne sõna lemma, mis mine "mine" lõpuline, siis vaadatakse kas ta ülemus on tühiverb
                if(sona.endswith('mine')):
                    if(verb in lause[lause[i][2][0][1]][1].split('|')):                  
                        #kui leidus selline, siis leitud sõnade indeksid pannakse tagastamise listi
                        tagastamine.append([min(i,lause[i][2][0][1]),max(i,lause[i][2][0][1])])
                        
                        
                #Teisena vaadatakse, kas sõna on sihitis ja nimisõna
                #Kui tema ülemus on tühiverb, siis märgitakse nominalisatsioonina
                elif(lause[i][2][0][0] =='@OBJ' and lause[i][4] =='S' and len(lause[i][0].split(" "))==1):  
                    #Toimub rahvaarvu kasv" ei tööta, sest kasv märgitakse "@SUBJ" 
                    
                    if(verb in lause[lause[i][2][0][1]][1].split('|') ):
                        #kui leidus selline, siis leitud sõnade indeksid pannakse tagastamise listi
                        tagastamine.append([min(i,lause[i][2][0][1]),max(i,lause[i][2][0][1])])
                    
        #tagastamis listis on elementide indeksid, kus mingi nominalisatsioon leiti
        #nende indeksitega otsin lausest üles sõnad ning tagastan kogu lauseosa mis on nende indeksite vahel              
        if(tagastamine):   
            for paar in tagastamine:
                kohaliklause= ""
                for alguslopp in range(paar[0],paar[1]+1):
                    kohaliklause+=lause[alguslopp][0]+" "
                seletused.append(sonastik[verb])
                kantseliit.append(kohaliklause[:-1])
                tagastamine = []
      
    return ([kantseliit,seletused])


                        
                        
                          
        
    