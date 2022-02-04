import requests
from bs4 import BeautifulSoup
import json

search=input("Nom d'une recette, un ingrédient, autre: ")
#city=input("Entrez la ville : ")

file= open("main.html", "w", encoding="utf-8")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="style.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Scrap Marmiton</title>
</head>

<style>
/* ----- Reset of default style ----- */
a,abbr,acronym,address,applet,article,aside,audio,b,big,blockquote,body,canvas,caption,center,cite,code,dd,del,details,dfn,div,dl,dt,em,embed,fieldset,figcaption,figure,footer,form,h1,h2,h3,h4,h5,h6,header,hgroup,html,i,iframe,img,ins,input,kbd,label,legend,li,mark,menu,nav,object,ol,output,p,pre,q,ruby,s,samp,section,small,span,strike,strong,sub,summary,sup,table,tbody,td,tfoot,th,thead,time,tr,tt,u,ul,var,video{margin:0;padding:0;border:0;font:inherit;vertical-align:baseline}article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section{display:block}body{line-height:1}ol,ul{list-style:none}blockquote,q{quotes:none}blockquote:after,blockquote:before,q:after,q:before{content:'';content:none}table{border-collapse:collapse;border-spacing:0}

/* ----- Typography ----- */
h1{font-size:32px;}
h3{font-size:18px;}
p{font-size:14px;}
a{font-size:18px;color:black;text-decoration: none;}

/* ----- Header ----- */
header{position:relative;float:left;width:100%;text-align:center;margin:50px 0 30px 0;}
header h1{position:relative;float:left;width:100%;font-weight:600;margin-bottom:20px;}
header p{position:relative;float:left;width:100%;font-size:24px;}

/* ----- Body ----- */
body{background-color: rgb(255, 155, 144);}
main{position:relative;float:left;width:90%;padding:20px 5%;}
main .row{min-height:450px;}
main .recipe{position:relative;float:left;width:15%;box-shadow: -5px 5px 10px rgba(0,0,0, 0.45);margin: 0 2.5% 20px 2.5%;background-color: white;border-radius:23px}
main .recipe .image{position:relative;float:left;width:100%;}
main .recipe .image img{width:100%;margin-bottom:20px;border-radius:23px 23px 0 0;}
main .recipe .image .sponso{position:absolute;left:0;padding:5px 10px;background-color:rgb(255, 111, 97);color:white;margin: 10px;border-radius: 10px;}
main .recipe_opinion, main .recipe_desc{position:relative;float:left;width:100%;}
main .recipe_desc{text-align:center;margin-bottom:20px;}
main .recipe_desc h3{margin-bottom:20px;}
main .stars{position:relative;float:left;width:50%;text-align:center;margin-left:5%;}
main .stars p{position:relative;float:left;width:20%;}
main .stars p svg{width: 90%;}
main .opinion_number{position:relative;float:left;width:40%;margin:10px 5% 10px 0;}
</style>

<body>''')

page = requests.get(f'https://www.marmiton.org/recettes/recherche.aspx?aqt={search}')
soupdata = BeautifulSoup(page.content, "html.parser")
title_search = soupdata.find("span", class_="MRTN__sc-16jp16z-1 gzsDhH")
results_number = soupdata.find("span", class_="MRTN__sc-16jp16z-2 elDEAz")

file.write(f'''<header>
    <h1> Résultat de la recherche pour : {title_search.text} </h1>
    <p>{results_number.text}</p>
</header>
<main>''')

datas = []

i = 1

for counter in range(1, 10):

    page = requests.get(f'https://www.marmiton.org/recettes/recherche.aspx?aqt={search}&page={counter}')

    soupdata = BeautifulSoup(page.content, "html.parser")

    results = soupdata.find_all("a", class_="MRTN__sc-1gofnyi-2 gACiYG")

    for result in results:
        picture = result.find("img",class_="SHRD__sc-dy77ha-0 vKBPb")
        sponsor = result.find("div",class_="MRTN__sc-30rwkm-1 bnabrb")
        title = result.find("h4",class_="MRTN__sc-30rwkm-0 dJvfhM")
        stars = result.find("div",class_="SHRD__sc-1q3upxa-2 egbhkM")
        star_state_1 = result.find("svg",class_="SHRD__sc-sr6s0j-1 cuxuXS")
        star_state_2 = result.find("svg",class_="SHRD__sc-sr6s0j-2 eHPLKd")
        star_state_3 = result.find("svg",class_="SHRD__sc-sr6s0j-0 gwcoTh")
        rate = result.find("span",class_="SHRD__sc-10plygc-0 jHwZwD")
        things = result.find("div",class_="MRTN__sc-30rwkm-3 fyhZvB")

        if (i%6 == 0) or (i==1):
            file.write(f'''<div class="row">''')

        file.write(f'''<div class="recipe">
        <a class="image" href="https://www.marmiton.org{result['href']}">
        <img src={picture['src']}>''')
        if sponsor:
            file.write(f'''<span class="sponso">Sponsorisé</span>''')
        file.write(f'''<div class="recipe_desc">
        <h3>{title.text}</h3>
        <div class="recipe_opinion">
        <div class="stars">''')
        for child in stars.children:
            if star_state_3 == child:
                file.write(f'''<p>{star_state_3}</p>''')
            if star_state_2 == child:
                file.write(f'''<p>{star_state_2}</p>''')
            if star_state_1 == child:
                file.write(f'''<p>{star_state_1}</p>''')
        file.write(f'''</div>
        <p class="opinion_number">{things.text}</p>
        </div>
        </div>
        </a></div>''')
        if sponsor:
            datas.append({'id':i,'name':title.text,'rate':rate.text,'things':things.text,'sponsor':sponsor.text,'picture_src':picture['src']})
        else:
            datas.append({'id':i,'name':title.text,'rate':rate.text,'things':things.text,'picture_src':picture['src']})

        if (i%5 == 0) and (i!=1):
            file.write(f'''</div>''')
            i=0

        i+=1
datas_gen = {'results':{'search_key':title_search.text,'search_results_number':results_number.text,'recipes': datas}}
json_string=json.dumps(datas_gen)
with open('json_data.json', 'w', encoding='utf8') as outfile:
    json.dump(json_string, outfile)

file.write('''</main>
    </div>
    </div>
</body>
</html>''')
