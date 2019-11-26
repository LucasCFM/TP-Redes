

# Sumário

1. [Descrição do problema](#descricao-do-problema)
2. [Messagem de comunicação](#messagem-de-comunicacao)
3. [Principais Classes](#principais-classes)
4. [Bibliografia](#bibliografia)



## Descrição do problema

Desenvolver um sistema para enviar o preço de vários postos de combustíveis e requisitar o preço mais barato em uma dada região. Você deverá criar um programa cliente e outro programa servidor.



## Messagem de comunicação

#### Mensagem de inserção

Utilizada para fazer uma inserçao de preço, essa mensagem é composta pelas cordenadas do posto em que se quer inserir um derterminado preço de um combustível. 



Está mesagem é representada por um dicionário contendo seus atributos, que é convertido em uma sequencia de bytes e então, através de um connector UDP, que comunica com o servidor que irá receber a mensagem, é transmitida para seu destino, e então adicionada ao registro de combustíveis, associado com seu posto.



Descrição e especificação dos dados da mensagem de inserção de preço:

{

​	'type': 'D', # char(1)

​	'id': MSG_ID, # integer

​	'fuel_type': fuel_type, # integer

​	'fuel_price': PRICE, # float

​	'station_lat': station_lat, # float

​	'station_lon': station_lon # float

}



#### Messagem de pesquisa

Esta mensagem serve para se fazer uma pesquisa por preços de combustível em um determinado ponto utilizando um raio de busca, procurando postos de combustível que têm aquele combustível e informando seu preço. 



Da mesma forma que a mensagem de busca a mensagem de pesquisa é formada por um dicionário com os dados da mensagem do serviço que o cliente requisitou, tranfegando atravez de um conector UDP para o servidor. 



Descrição e especificação dos dados da mensagem de busca:

{

​	'type': 'P', # char(1)

​	'id': MSG_ID, # integer

​	'fuel_type': fuel_type, # integer

​	'search_radius': RADIUS, # float

​	'center_lat': CENTER_LAT, # float

​	'center_lon': CENTER_LON # float

}


## Principais Clases

#### UPD Cliente


#### UPD Server



## Bibliografia

[https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude]

[https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python]




