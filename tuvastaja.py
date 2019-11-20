# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:30:42 2017

@author: Kaarel Sõrmus
"""
from tkinter import ttk, HORIZONTAL
from tkinter import Tk
from tkinter import *

import backend


from tkinter import Text as boxText
from tkinter import messagebox
from estnltk.names import LAYER_CONLL

from multiprocessing.pool import ThreadPool
from estnltk import Text 

#NB! Kui programmi edenemisriba jääb käima ja ühtegi sõna samal ajal ei märgendata, siis vajalike installeerimiste juures võis midagi valesti minna
# errorite nägemiseks vaadata funnktsiooni sisend1 juures kommentaare


def suurenda_akent(naitelaused,root1):
    #suurenda_akent meetod on selleks, et infoakent saaks laiendada ja näitelauseid näidata
    #argumentideks on näitelaused ja eelmises funktsioonis loodud infoaken 
    
    #Proovikas1 tehakse selleks, et saaksin vajaliku akna suuruse arvutada, proovikas1 muud moodi ei kasutada
    
    
    #tehakse algne aken
    proovikas1=Toplevel(root1)
    proovikas = Message(proovikas1)
    #aknale lisatakse juurde kaks märget "halvem" ja "parem"
    valed1=Label(proovikas,text = "HALVEM",fg ="red")
    valed1.grid(row=1,column=0,padx=5,pady=5,sticky="nsew")
    oiged1 = Label(proovikas,text="PAREM",fg="green")
    oiged1.grid(row=1,column=1,padx=5,pady=5,sticky="nsew")
    suurim = valed1.winfo_reqheight()+oiged1.winfo_reqwidth()
    x=0
    y=0
    suurimy=0
    #populeerime proovikas1 näitelausetega
    for p in range(len(naitelaused)):
            vale1 = Message(proovikas,text=naitelaused[p][0], relief=RIDGE)
            vale1.grid(row=p+2,column=0,sticky="nsew",padx=5,pady=5)
            x+=vale1.winfo_reqheight()
            oige1 = Message(proovikas,text=naitelaused[p][1], relief=RIDGE)
            
            
            oige1.grid(row=p+2,column=1,sticky="nsew",padx=5,pady=5) 
            #arvutame maksimaalse proovika laiuse ja maksimaalse proovika pikkuse
            if(suurimy<oige1.winfo_reqwidth()):
                suurimy=oige1.winfo_reqwidth()
            if(y<vale1.winfo_reqwidth()+oige1.winfo_reqwidth()):
                y=vale1.winfo_reqwidth()+oige1.winfo_reqwidth()
    
    uusx = root1.winfo_reqheight()+30
    #Saadakse tehtud akna pikkus
    
    #laiendama vastavalt saadud pikkustele infoakent
    root1.geometry('{}x{}'.format(max(root1.winfo_reqwidth()+suurimy,suurim+30,y+30), uusx+x+len(naitelaused)*15+valed1.winfo_reqheight()))
    #Prooviaken kaotatakse ära, aga nüüd on vajalikud akna suurused olemas
    proovikas1.destroy()
    
    
    #ja populeerime infoakna näitelausetega
    valed=Label(root1,text = "HALVEM",fg ="red")
    valed.grid(row=1,column=0,padx=5,pady=5,sticky="nsew")
    oiged = Label(root1,text="PAREM",fg="green")
    oiged.grid(row=1,column=1,padx=5,pady=5,sticky="nsew")
    for p in range(len(naitelaused)):
            vale = Message(root1,text=naitelaused[p][0], relief=RIDGE)
            vale.grid(row=p+2,column=0,sticky="nsew",padx=5,pady=5)
            oige = Message(root1,text=naitelaused[p][1], relief=RIDGE)
            oige.grid(row=p+2,column=1,sticky="nsew",padx=5,pady=5)
    

def callback(event,sonaseletus,kantnaited):
    #see meetod on selleks, et saaksime märgendile peale vajutada, tekitatakse infokast
    #luuakse uus aken
    info_window = Toplevel(root)
    info_window.wm_title("")
    info_window.config(bg = tkColor)
   
    
    #Järgmine if, else plokk tehakse selleks, et saada kätte kui suur peab infokast olema, seal kasti ennast ei looda
    
    #Kui pole kantseliitliksona, siis naidete pikkus on 0.
    #Kui on kantnäited, siis tehakse õige suurusega kast koos nupuga,
    #muidu tehakse kastisuurus ilma nuputa.
    if(len(kantnaited) != 0):
        #siin on tegemist kantseliidi märgendi infokastiga, sest naited argument polnud tühi
        #tehakse message kast ning pannakse juurde nupp näited
        proov = Message(info_window,text=sonaseletus+"\n"+"\n"+"\n"+"\n")
        button = Button(proov,text="Näited")
        #jätame meelde selle kasti pikkuse ja laiuse
        m= proov.winfo_reqwidth()+20
        s= proov.winfo_reqheight()
        geomeetria=str(m)+"x"+str(s)+"+{0}+{1}"
    else:
        #siia jõutakse siis kui tegemist oli paronüümiga, argument kantneited oli tühi
        #Tekitame Message kasti
        proov = Message(info_window,text=sonaseletus)
        #jätame selle kasti suurused meelde
        m= proov.winfo_reqwidth()
        s= proov.winfo_reqheight()
        geomeetria=str(m)+"x"+str(s)+"+{0}+{1}"    
    
        
    #Nüüd on igal juhul meil infokasti suurused teada, olenemata sellest, kas tegu oli paronüümiga või mitte
    #Defineerime infokasti suuruse
    info_window.geometry(geomeetria.format((event.x_root),(event.y_root+10)))
    #Infokasti tekstiks on argument sonaseletus. See on tekst mis kuvatakse igale infokastile olenevalt sõnast või kantseliitlikust vormist
    label = Message(info_window, text=sonaseletus)
    #Kui argument kantnaited polnud tühi, lisame sellele nupu
    if(len(kantnaited)!=0):
        #Kui nupp lisatakse, siis kutsutakse välja uus meetod suurenda_akent, mis näitab näitelauseid
        button = Button(info_window,text="Näited",command = lambda uus=kantnaited:suurenda_akent(uus,info_window))
        button.grid(row=0,column=1)
     #muidu nuppu ei lisata   
            
        
    label.config(anchor = "w",bg = tkColor)
    label.grid(row=0,column=0)  
    info_window.mainloop()

    
    
def sisend1():
    #Siin tekitatakse uus lõim põhimeetodi sisend jaoks, seda selleks, et oleks võimalik märgendile vajutada enne kui kogu programm valmis jõuab
    sisse = ThreadPool(processes=1)
    sisse._terminate_pool
    sissethread = sisse.apply_async(sisend,[])
    
    #Kui programm jookseb kokku ja edenemisriba edeneb lõpmatult, siis on error tekkinud
    #Kui errorit tahetakse näha, siis tuleb, siin funktsioonis kõik tekst ära kustutada ja kutsuda lihtsalt välja meetod
    #sisend()
    
    
    
    
 
def edenemisriba(progress):
    #Meetod mis lisab muudab argumendis oleva edenemisriba väärtust
    progress['value'] += 5
   
def sisend():
        
    #Kui põhifunktsioon tööle pannakse, siis statistika näitajad nullitakse
    kokku.set(0)
    mitupar.set(0)
    mitusona.set(0)
    mitunom.set(0)
    mitupoolt.set(0)
    mituolema.set(0)
    mitumitmus.set(0)
    mitult.set(0)
    mitusaav.set(0)
    kantskokku.set(0)

    
    
    
    
    
   
    #Järgnev for tsükkel kustutab kõik märgendid tekstist, kui analüüsi nuppu kordualt vajutatakse, siis ei jää eelnevad märgendid teksti
    for tag in textbox.tag_names():
        textbox.tag_delete(tag)
        
    textbox.tag_remove("1.0","end")
    
    #Edenemisriba pannakse käima
    progress.place()
    progress.start()
    progress['value'] =0
    #Saadakse tekstikastist kogu tekst
    tekstsisse= textbox.get("1.0",END)
    
    #Tekstile tehakse süntaktiline analüüs
    syntaksitekst = Text(tekstsisse)
    syntaksitekst.tag_syntax()
    
    syntaks = []
    
   
    #Kogu tekstile, millele tehti süntaksanalüüs käiakse lausete kaupa läbi
    #iga lause kohta lisatakse järjendisse syntaks - lauses olevad sõnad, lauses olevate sõnade lemmad, süntaktilise funktsioonimärgendi ja 
    #sõna süntaktilise ülema lauses, sõnavorm ja sõnaliik 
    for sentence in syntaksitekst.split_by('sentences'):
        syntaks.append( list( zip(sentence.word_texts, sentence.lemmas, [x['parser_out'] for x in sentence[LAYER_CONLL]], sentence.forms, sentence.postags ) ) )
   
    #tekitatakse uued lõimed   
    pool = ThreadPool(processes=10)
    
    
    
    #järgnevates if lausete kontrollitakse, kas Menüü seadete alt, valikunupud on valitud või mitte if(nupp) ==1
    #iga if lause all kutsutakse välja edenemisriba funktsioon, et edenemisriba liiguks(edenemisriba(progress)
    #iga if lause all tehakse eraldi lõim igale funktsioonile
    #Allpool saadakse lõimede funktsioonide tagastatud järjendid kätte. (*)
    
    if(par.get()==1):
        #Minnakse  backendi failis olevasse funktsiooni analyys, kus otsitakse tekstist üles paronüümid
        edenemisriba(progress)
        parthread = pool.apply_async(backend.analyys, [tekstsisse])
        
    if(kants.get()==1):
        #Minnakse  backendi failis olevasse funktsiooni kantsoanalyys, kus kontrollitakse kantseliidisõnu lemmade või tekstis esinemise vormide järgi
        edenemisriba(progress)
        kantsthread = pool.apply_async(backend.kantsonanalyys, [tekstsisse])  
                
    if(nomin.get() ==1):
        #Minnakse backendi failis olevasse funktsiooni nominalisatsioon, kus kontrollitakse nominalisatsiooni ühendverbe akna kaudu nt "aset leidma"
        edenemisriba(progress)
        nomthread = pool.apply_async(backend.nominalisatsioon,[tekstsisse]) 
        
    #Siin hakatakse syntaxi listi läbi käima
    #syntaksi listis olid elemendid lausete kaupa
    
    for lause in syntaks:
        edenemisriba(progress)
        
        #Siin olevad funktsioonid vajavad kantseliidi leidmiseks süntaktilist infot
        
        if(olema.get()==1):
            #olema + kesksona jaoks kutsutakse välja funktsioon kasonolemas
            #tagastatakse leitud sõnad mida märgendada, seletus kantseliidivormi kohta ja näitelaused
            kesksonasyntaks = pool.apply_async(backend.kasonolemas, [lause])
            #Küsime lõimelt kesksonasyntaks meetodi kasonolemas tagastatud informatsiooni
            
            kesksona = kesksonasyntaks.get()
            #Käime tagastatud info läbi
            #Esimesel kohal 'kesksona[0]' on kõik erinevad lauseosad, mis vajavad märgendamist - on kantseliit
            for m in range(len(kesksona[0])):
                #statistilistele loenduritele lisatakse 1 juurde
                kantskokku.set(kantskokku.get()+1)
                mituolema.set(mituolema.get()+1)
                
                #tehakse märgend, olema + kesksona märgend on punane
                textbox.tag_config(kesksona[0][m],background="red")
                #kutsutakse välja search meetod, mis märgib tekstis argumentidena edasi antud lauseosad
                #search meetodi esimene argument on tekstikast,teine argument on lauseosa mida märgitakse, kolmas argument on näitelaused ning viimane
                #argument on seletus kantseliidi vormile
                search(textbox,kesksona[0][m],kesksona[2],kesksona[1])
                
                
                
        if(kants.get()==1):
            #Täpselt samamoodi nagu eelmisega, aga siin on tegemist kantseliitlike sõnade (ühendverbide) leidmisega
            #Et teada, kas tegemist on kantseliidiga nt "läbi viima" ja, et teada, kas "läbi" ülem on "viima" peame kontrollima süntaksit
            kantssyntaks = pool.apply_async(backend.syntaksileidmine,[lause])
            #küsime lõimelt funktsiooni syntaksileidmine tagastatud järjendi
            kantseliidivastus1 = kantssyntaks.get()
            
            #järjendi esimesel kohal on lauseosad mis vajavad märgendit
            for m in range(len(kantseliidivastus1[0])):
                #Statistilistele muutujatele lisatakse üks
                mitusona.set(mitusona.get()+1)
                kantskokku.set(kantskokku.get()+1)
                #print(kantseliidivastus[0][m])
                
                naited= []
                #Defineerime märgendi iga lauseosa jaoks
                textbox.tag_config(kantseliidivastus1[0][m],background='lightgreen')
               
            
                for p in kantseliidivastus1[1][m]:
                    naited.append(p)
                #kutsutakse iga lauseosa kohta search funktsioon, millega märgendatakse tekstis vastav lauseosa
                #search meetodi esimene argument on tekstikast,teine argument on sõna mida märgitakse, kolmas argument on näitelaused ning viimane
                #argument on seletus kantseliidi sõnale
                search(textbox,kantseliidivastus1[0][m],naited[1:],kantseliidivastus1[1][m][0])
                
                
        if(saav.get()==1):
            #Tegemist määrus saavas käändes kantseliidiga
            #samamoodi nagu eelmistel tehakse lõim
            saavthread = pool.apply_async(backend.kassaavolemas, [lause])
            maarussaavas = saavthread.get()
            #Saame vastuse, kus maarussaavas on nüüd esimesel kohal lausest leitud kantseliitlikud lauseosad
            for m in range(len(maarussaavas[0])):
                #statistika muutujatele lisatakse üks
                kantskokku.set(kantskokku.get()+1)
                mitusaav.set(mitusaav.get()+1)
                #defineeritakse märgend selle kantseliidivormi jaoks
                textbox.tag_config(maarussaavas[0][m],background="grey78")
                #search funktsiooni otsib lauseosa tekstist ja märgendab selle
                #search meetodi esimene argument on tekstikast,teine argument on lauseosa mida märgitakse, kolmas argument on näitelaused ning viimane
                #argument on seletus kantseliidi vormile
                search(textbox,maarussaavas[0][m],maarussaavas[2],maarussaavas[1]) 
          
                
        
        if(nomin.get()==1):
            #Tegemist on nominalisatsiooniga. Siin ei otsita ühendverbe vaid tühiverbi + -mine vormi või sihitisega koos tühiverbe
            #samamoodi lõimedega nagu eelmised
            nomsyntaksthread = pool.apply_async(backend.kasnomolemas, [lause])
            nom = nomsyntaksthread.get()
            #nom esimesel kohal on lauseosad mis vajavad märkimist
            for m in range (len(nom[0])):
                #statistika muutujatale lisatakse üks
                kantskokku.set(kantskokku.get()+1)
                mitunom.set(mitunom.get()+1)
                
                naited = []
                #tehakse märgend iga lauseosa jaoks
                textbox.tag_config(nom[0][m],background = "bisque3")
                
                for p in nom[1][m]:
                    naited.append(p)
                #search funktsiooni otsib lauseosa tekstist ja märgendab selle
                #search meetodi esimene argument on tekstikast,teine argument on lauseosa mida märgitakse, kolmas argument on näitelaused ning viimane
                #argument on seletus kantseliidi lauseosale
                search(textbox,nom[0][m],naited[1:],nom[1][m][0])
            
    #Kutsutakse backend failist välja meetod kokku. Seal meetodis arvutatakse kogu sõnade arv kogu tekstis
    #muutuja kokku saab selle väärtuse, ehk näitab mitu sõna tekstis kokku on
    kokku.set(backend.kokku(tekstsisse))
    
   
        
    #Järgnevad if laused on kantseliidi leidmiseks ilma süntaks analüüsita
    
    if(poolt.get()==1):
        edenemisriba(progress)
        #kutsutakse failist backend välja meetod poolttarid ning argumendiks on kogu tekstikasti tekst
        poolttar = backend.poolttarind(tekstsisse)
        #funktsiooni tagastuses on esimsel kohal kõik leitud lauseosad 
        for m in range(len(poolttar[0])):
            
            edenemisriba(progress)
            #statistika numbreid muudetakse
            kantskokku.set(kantskokku.get()+1)
            mitupoolt.set(mitupoolt.get()+1)
            
            #iga lauseosa korral tehakse märgend ning kutsutakse välja search funktsioon, mis lisab märgendi tekstikasti
            textbox.tag_config(poolttar[0][m],background="maroon1")
            #search meetodi esimene argument on tekstikast,teine argument on lauseosa mida märgitakse, kolmas argument on näitelaused ning viimane
            #argument on seletus kantseliidi vormile
            search(textbox,poolttar[0][m],poolttar[2],poolttar[1])
                           
    if(lt.get()==1):
        #Kutsutakse välja meetod ltmaar, argumendiks on sisendtekst
        ltmaarsonad = backend.ltmaar(tekstsisse)
        #funktsiooni tagastuses on esimsel kohal kõik leitud lauseosad 
        for m in range(len(ltmaarsonad[0])):
            edenemisriba(progress)
            #Statistika näitajaid muudetakse
            kantskokku.set(kantskokku.get()+1)
            mitult.set(mitult.get()+1)
             #iga lauseosa korral tehakse märgend ning kutsutakse välja search funktsioon, mis lisab märgendi tekstikasti
            textbox.tag_config(ltmaarsonad[0][m],background='yellow')
            #search meetodi esimene argument on tekstikast,teine argument on sõna mida märgitakse, kolmas argument on näitelaused ning viimane
            #argument on seletus kantseliidi vormile
            search(textbox,ltmaarsonad[0][m],ltmaarsonad[2],ltmaarsonad[1])
            
    
    #Kui eelnevalt kutsusime paar funktsiooni eraldi lõimede peal välja (*)   
    #siis siin hakkame nende tagastatud järjenditega tegelema
            
    if(nomin.get() ==1):
        #saame lõimel kutsutud funktsiooni tagastamisväärtuse
        #nomthread oli nominalisatsiooni ühendverbide jaoks mõeldud
        nom = nomthread.get()
        #nomi esimesel kohal on kõik tagastatud lauseosad
        for m in range (len(nom[0])):
            #muudame statistika muutujaid
            kantskokku.set(kantskokku.get()+1)
            mitunom.set(mitunom.get()+1)
            
            naited = []
            #defineerime märgendi
            textbox.tag_config(nom[0][m],background = "bisque3")
            for p in nom[1][m]:
                naited.append(p)
            #kutsume välja search funktsiooni, mis märgendab tekstis lauseosad
            #search meetodi esimene argument on tekstikast,teine argument on lauseosa mida märgitakse, kolmas argument on näitelaused ning viimane
            #argument on seletus kantseliidi vormile
            search(textbox,nom[0][m],naited[1:],nom[1][m][0])
  

    if(par.get()==1):
        empty = []
        edenemisriba(progress)
        #Saame lõimel kutsutud funktsiooni väärtuse
        vastus = parthread.get()
        #esimesel kohal on kõik leitud paronüümid
        for m in range(len(vastus[0])):
            edenemisriba(progress)
            #muudame statistika muutujat ühe võrra
            mitupar.set(mitupar.get()+1)
            #seame iga sõna vastavusse värviga - defineerime märgendi
            textbox.tag_config(vastus[0][m],background='lightblue')
            #Kutsume iga sõna korral funktsiooni search, mis otsib tekstikastist sõna ja märgendab vastavalt
            #kolmas argument on empty sellepärast, et paronüümidel pole näitelauseid
            #esimene arguemnt on tekstikast, teine on sõnad,kolmas on tühi ning neljas on paronüümide seletused
            search(textbox,vastus[0][m],empty,vastus[1][m])
        
    #Leitud kantseliit - mitmus ainsuse asemel
    if(mitmus.get()==1):
        edenemisriba(progress)
        #selle kantseliidi jaoks pole eraldi lõime kasutatud
        #kutsutakse lihtsalt välja meetod mitmusanalyys failist backend
        mitmusains = backend.mitmusanalyys(tekstsisse)
        for m in range(len(mitmusains[0])):
            #Esimesel kohal on leitud kantseliitlikud sõnad
            #Muudetakse statistilisi muutujaid
            kantskokku.set(kantskokku.get()+1)
            mitumitmus.set(mitumitmus.get()+1)
            
            #Iga sõna jaoks defineeritakse märgend ja värv
            textbox.tag_config(mitmusains[0][m],background='pink3')
            #Iga sõna märgendatakse tekstikastis vastavat värvi
            #search meetodi esimene argument on tekstikast,teine argument on sõna mida märgitakse, kolmas argument on näitelaused selle sõna kohta ning viimane argument on
            #seletus leitud sõnale
            search(textbox,mitmusains[0][m],mitmusains[2][m],mitmusains[1])
            
    #Leitud kantseliitlikud sõnad
    if(kants.get()==1):
        #Lõim pandi alguses käima (*)
         edenemisriba(progress)
         #saame lõime tagastusväärtuse
         kantseliidivastus = kantsthread.get()
         #kantseliidivastuse esimesel kohal on kõik leitud sõnad
         for m in range(len(kantseliidivastus[0])):
            edenemisriba(progress)
            #muudame statistika muutujaid
            mitusona.set(mitusona.get()+1)
            kantskokku.set(kantskokku.get()+1)
            
            
            naited= []
            #igale sõnale defineeritakse märgend
            textbox.tag_config(kantseliidivastus[0][m],background='lightgreen')
            
        
            for p in kantseliidivastus[1][m]:
                naited.append(p)
            #märgendid leitakse tekstikastist
            #search meetodi esimene argument on tekstikast,teine argument on sõna mida märgitakse, kolmas argument on näitelaused selle sõna kohta ning viimane argument on
            #seletus sõnale
            search(textbox,kantseliidivastus[0][m],naited[1:],kantseliidivastus[1][m][0])
            
    #Edenemisriba lõpetab töö
    #lõppväärtuseks pannakse 100
    progress.stop() 
    progress['value']=100
    
#search meetodit kasutatakse sõnade otsimiseks tekstikastist
#esimene argument on tekstikast, teine argument on sõna, mida otsitakse, kolmas on näitelaused ning neljas argument on seletused sõna kohta või kindla kantseliidivormi kohta  
def search(text_widget, keyword, naide,seletus):
    uussona = keyword
    #Kui märgitava sõnade sisse jääb mingi märgend, mis muudab regexi sisu, siis 'escape'-me need sümbolid
    for p in range(len(uussona)):
        if(keyword[p] in ['-','[',']','{','}','(',')','*','+','?','.',',','^','$','|','#']):
            keyword = uussona[:p-1]+"\\"+uussona[p-1:] 
        
    #sõnu leiame tekstikastist regulaaravaldiste kaudu
    #regulaaravaldis otsib ainult sõnu. kui on vaja näiteks leida sõna "täna", siis ta ei märgi sõnas "tänapäeval" sõnaosa "täna".
    if(keyword!="" and keyword[0]=='-'):
        reg = '(?i)-'+keyword[1:]
    else:
        reg='(?i)\y'+keyword+'\y'
    
    count = IntVar()    
    pos = '1.0'
    #see while tsükkel käib nii kaua kuni muutuja idx-l pole väärtust, ehk kui sõna ei leita tekstikastist
    while True:
        #textbox.search tagastab numbrilise väärtuse, mis indeksilt sõna tekstikastist leiti
        idx = textbox.search(reg, pos, END,count=count.get(),regexp=True)
        if not idx:
            break
        
        pos = '{}+{}c'.format(idx, len(keyword))
      
        #Lisame leitud sõnale märgendi.
        textbox.tag_add(keyword, idx, pos)
        #Siin lisame igale märgendile vajutamise võimaluse
        #kutsume välja meetodi callback ning anname argumentidena edasi seletuse ja näitelaused
        textbox.tag_bind(keyword, "<Button-1>",  lambda event,arg=seletus:callback(event,arg,naide))

  
def searchopetus(widget,keyword):
    #Õpetuse kasti jaoks tehtud funktsioon
    #argument keywordi järgi otsib argument widgetist sõna
    #töötab põhimõttelt samamoodi nagu search funktsioon
    
    reg='(?i)\y'+keyword+'\y'
    count = IntVar()    
    pos = '1.0'
    while True:
        idx = widget.search(reg, pos, END,count=count.get(),regexp=True)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        #Kui sõna leitakse, siis märgitakse ta ära
        widget.tag_add(keyword, idx, pos)
        
        
def info():
    #Info kast menüüst
    messagebox.showinfo("Info","Programm kasutab andmebaasina järgmiseid allikaid: \n\nPullerits. E raamatut 'Kuidas hoiduda kantseliidist' \nPlado H ja Mandra K. raamatut 'Väike paronüümisõnastik'\n \nProgramm on valminud bakalaureusetööna: \n'Kantseliidi- ja paronüümituvastaja'\n\nAutor: Kaarel Sõrmus ")
 

def opetus():
    #Õpetuse kast menüüst
    #Õpetuse kast on tekstikast
    opetus = Toplevel(root)
    uustext = boxText(opetus)
    uustext.insert("end","1) Sisestage programmi analüüsimist vajav tekst\n2) Valige seadete alt, mida tahate, et programm märgiks\n3) Vajutage nupule 'Analüüsi!\n4) Programm märgib kantseliiti ja paronüüme järgmiselt: \nParonüümid - helesinine\nNominalisatsioon - pruun\nPoolt-tarind - roosa\nOlema+kesksona - punane\nKantseliitlikud, tarbetud sõnad - roheline\nMitmus ainsuse asemel - tumeroosa\nMäärus saavas käändes - hall\nLt-määrsõnad - kollane\n5) Märgendi kohta informatsiooni saamiseks klikkige märgendile.")
    #Lisame tekstikastis sõnadele tagid ja anname neile värvi
    uustext.tag_config("helesinine",background='lightblue')  
    uustext.tag_config("kollane",background='yellow')
    uustext.tag_config('pruun',background='bisque3')
    uustext.tag_config('punane',background='red')
    uustext.tag_config('roosa',background='maroon1')
    uustext.tag_config('tumeroosa',background='pink3')
    uustext.tag_config('roheline',background='lightgreen')
    uustext.tag_config('hall',background='grey78')
    #Kasutatakse searchopetus meetodit, mis värvib vastavad sõnad vastavat värvi.
    searchopetus(uustext,"hall")
    searchopetus(uustext,"helesinine")
    searchopetus(uustext,"kollane")
    searchopetus(uustext,"pruun")
    searchopetus(uustext,"punane")
    searchopetus(uustext,"roosa")
    searchopetus(uustext,"tumeroosa")
    searchopetus(uustext,"roheline")
    
    
    uustext.pack()
    uustext.config(state=DISABLED)
    opetus.focus_force()

def muudakoiki():
    #muudakoiki meetod muudab korraga koikide kantseliitlike vormide IntVar muutujad vastavalt kantseliidi muutujale
    #Kui kantseliidi muutja pannakse nulliks, muudetakse kõik teised nulliks ja vastupidi
    kants.set(koik.get())
    nomin.set(koik.get())
    poolt.set(koik.get())
    olema.set(koik.get())
    mitmus.set(koik.get())
    lt.set(koik.get())
    saav.set(koik.get())

def statistika():
    #Statistika kasti tegemine
    statistika = Toplevel(root)
    parlabel = Label(statistika,textvariable =mitupar)
    #kasutatakse tulpasid, iga tulba esimeses veerus on tekst mida leiti, ning teises veerus on muutuja
    partekst = Label(statistika,text="Paronüüme leiti: ")
    partekst.grid(row=0,column=0)
    parlabel.grid(row=0,column=1)
    
    kankokkulabel = Label(statistika,textvariable = kantskokku)
    kankokku = Label(statistika,text="Kantseliiti leiti: ")
    kankokkulabel.grid(row=1,column=1)
    kankokku.grid(row=1,column=0)
    
    tyhi = Label(statistika,textvariable = "")
    tyhi.grid(row=2,column= 0)
    
    sonalabel = Label(statistika,textvariable =mitusona)
    sonatekst = Label(statistika,text="Kantseliitlikuid sõnu leiti: ")
    sonatekst.grid(row=3,column=0)
    sonalabel.grid(row=3,column=1)
    
    nomlabel = Label(statistika,textvariable =mitunom)
    nomtekst = Label(statistika,text="Nominalisatsiooni leiti: ")
    nomtekst.grid(row=4,column=0)
    nomlabel.grid(row=4,column=1)
    
    pooltlabel = Label(statistika,textvariable =mitupoolt)
    poolttekst = Label(statistika,text="Poolt-tarindeid leiti: ")
    poolttekst.grid(row=5,column=0)
    pooltlabel.grid(row=5,column=1)
    
    olemalabel = Label(statistika,textvariable =mituolema)
    olematekst = Label(statistika,text="Olema+kesksõnu leiti:  ")
    olematekst.grid(row=6,column=0)
    olemalabel.grid(row=6,column=1)
    
    mitulabel = Label(statistika,textvariable =mitumitmus)
    mitutekst = Label(statistika,text="Mitmus ainsuse asemel leiti:  ")
    mitutekst.grid(row=7,column=0)
    mitulabel.grid(row=7,column=1)
    
    maarlabel = Label(statistika,textvariable =mitusaav)
    maartekst = Label(statistika,text="Määrus saavas käändes leiti:  ")
    maartekst.grid(row=9,column=0)
    maarlabel.grid(row=9,column=1)
    
    ltlabel = Label(statistika,textvariable =mitult)
    lttekst = Label(statistika,text="Lt-määrsõnu leiti:  ")
    lttekst.grid(row=10,column=0)
    ltlabel.grid(row=10,column=1)
    
    tyhi1 = Label(statistika,textvariable = "")
    tyhi1.grid(row=11,column= 0)
    
    kokkulabel = Label(statistika,textvariable =kokku)
    kokkutekst = Label(statistika,text="Sõnu kokku tekstis:  ")
    kokkutekst.grid(row=12,column=0)
    kokkulabel.grid(row=12,column=1)
    
    
    
#Värvid mida aknal kasutan
tkColor = '#d7f5f7'
tkColor1 = '#dcdbe0'
tkColor2 = '#f7f7f7'
tkColor3 = "#595959"
tkLaius = 160
tkPikkus = 30

#Tekitan akna
root = Tk()
root.wm_title("Kantseliidi- ja paronüümituvastaja")
root.configure(background = tkColor2)

#Frame ülemise menüü jaoks
menuframe = Frame(root)
menuframe.config(bg=tkColor)



root.option_add('*tearOff', False)

#Abi nupu tegemine
menubar = Menubutton(menuframe, text="Abi")
pick = Menu(menubar)
menubar.config(menu=pick)
#Iga nupp kutsub eraldi fuktsiooni välja
#Juhend nupuga kutsutakse meetod opetus
pick.add_command(label='Juhend',command = opetus)
#Statistika nupuga kutsutakse meetod statistika
pick.add_command(label='Statistika',command=statistika)
pick.add_separator()
#Nupuga info kutsutakse meetod info
pick.add_command(label='Info',command=info)

menubar.config(bg=tkColor, bd=4)



#Seaded nupu tegemine
valik = Menubutton(menuframe,text = "Seaded")
valikud = Menu(valik)
valik.config(menu=valikud,bg=tkColor, bd=4)



#Seaded nupu all tekitan paronüümidele valikunupu
par = IntVar(value=1)
valikud.add_checkbutton(label="Paronüümid",onvalue = 1,offvalue = 0,variable = par)

valikud.add_separator()
#Kantseliitide valikunupud
#IntVarid muutuvad vastavalt kas nupule on vajutatud või ei, algselt on nupp 1 ehk True

kants = IntVar(value=1)
nomin = IntVar(value=1)
poolt = IntVar(value=1)
olema = IntVar(value=1)
mitmus = IntVar(value=1)
lt = IntVar(value=1)
saav = IntVar(value=1)
koik = IntVar(value=1)

#Tekitan valikunupud, muutujaks panen vastavad IntVarid
#Kui vajutatakse nupule Kantseliit, kutsutakse välja meetod muudakoiki
valikud.add_checkbutton(label="Kantseliit",onvalue=1,offvalue=0,variable= koik,command=muudakoiki)
valikud.add_separator()


valikud.add_checkbutton(label="Kantseliitlikud sõnad",onvalue = 1,offvalue = 0,variable = kants)

valikud.add_checkbutton(label="Nominalisatsioon",onvalue = 1,offvalue = 0,variable = nomin)

valikud.add_checkbutton(label="Poolt-tarind",onvalue = 1,offvalue = 0,variable = poolt)

valikud.add_checkbutton(label="Olema+kesksõna",onvalue = 1,offvalue = 0,variable = olema)


valikud.add_checkbutton(label="Mitmus ainsuse asemel",onvalue = 1,offvalue = 0,variable = mitmus)
valikud.add_checkbutton(label="Määrus saavas käändes",onvalue=1,offvalue=0,variable=saav)
valikud.add_checkbutton(label="Lt-määrsõnad",onvalue = 1,offvalue = 0,variable = lt)

#Tekitatakse loendurid, mis hiljem loevad palju mitu tüüpi kantseliiti/paronüümi leiti
kantskokku=IntVar(value=0)
mitusaav = IntVar(value=0)
mitupar = IntVar(value=0)
mitusona = IntVar(value=0)
mitunom = IntVar(value=0)
mitupoolt = IntVar(value=0)
mituolema = IntVar(value=0)
mitumitmus = IntVar(value=0)
mitult = IntVar(value=0)
kokku = IntVar(value=0)



#Teen aknaelemendid
title = Label(root, text ="Kantseliidi- ja paronüümituvastaja", fg=tkColor3, font =(None,20), background=tkColor2)
#Tekitatakse nupp analüüsi, mis kutsub välja meetodi sisend1
button = Button(root,text="Analüüsi!",background=tkColor,command=sisend1,width=30)
textbox = boxText(root,wrap='word')
scr = Scrollbar(root)
scr.config(command=textbox.yview)
textbox.config(yscrollcommand=scr.set)
# adding a tag to a part of text specifying the indices


#Packin rooti elemendid aknale
valik.pack(side=LEFT)
menubar.pack(side=LEFT)


#Manüünupud panen akna üles nurka
menuframe.pack(side = TOP,anchor = W,fill=X)
progress=ttk.Progressbar(root,mode="determinate",orient=HORIZONTAL,length=100)

title.pack(fill=X, padx=10,pady=10)
button.pack(side=BOTTOM,anchor=CENTER,padx=10,pady=10)
progress.pack(side=BOTTOM)
textbox.pack(fill="both",side=LEFT,padx=10,expand=True,pady= 10)

scr.pack(side=RIGHT, fill=Y, expand=False)


root.mainloop()


    