# Documentação

## particle_height

```python
particle_height(dataset: xarray.Dataset, ref_particle: int) -> tuple:
```

Esta função é utilizada durante a execução da função __mplscripts.extract_info__. A função recebe um objeto da classe `Dataset` da biblioteca [xarray](https://docs.xarray.dev/en/stable/) e um número de referência da particula desejada. A partir do valor de referência da particula, é pego os índices referentes a particula em questão na variável __particle_type__ do Dataset. Em posse dos índices correspondentes a particula, utiliza-se estes índices para "parsear" na variável __range_nrb__ do mesmo Dataset e pegar os valores das alturas e adiciona-los a um `np.array` e assim retornar sua respectiva média e desvio padrão em uma `tuple`. Vale lembrar que __range_nrb__ é correspondente à __particle_type__. 

### Parâmetros
- __dataset: xarray.Dataset__<br>
Dataset que contém os dados NetCDF (.nc) do LIDAR 

- __ref_particle: int__<br>
Valor referente à partícula. 

Valores de referência das partícula:  0 - Water Cloud, 1 - Mixed Cloud, 2 - Ice/Dust/Ash, 3 - Rain/Dust, 4 - Molecular,  5 - Clean Aerossol, 6 - Polluted Aerossol, 7 - Undefined.  Valores disponíveis no arquivo NetCDF na variável __particle_type_mapping__.

### Exemplo de chamada 
```python
lidar = xr.open_dataset('caminho-do-arquivo.nc')
media, desvio_padrao = particle_height(lidar, 6)
```


## extract_info

```python
extract_info(path: str, file_name:str) -> pandas.DataFrame:
```

Função que extrai algumas informações do arquivo NetCDF do LIDAR (Abaixo a lista de variáveis obtidas). A função recebe o caminho/diretório do arquivo e um nome para o arquivo csv que será criado com a extração e retorna um DataFrame do Pandas com as informações obtidas. 

__Dados extraídos__:
- data_hora,
- temp: temperatura detectada pelo Mini MPL
- aod
- clp: Altura da CLP
- clean_aerossol: Quantidade de particulas de aerossóis limpos detectados
- clean_aerossol_h_mean: Altitude média dos aerossóis limpos 
- clean_aero_h_std: Desvio padrão da altitude dos aerossóis limpos 
- polluted_aerossol: Quantidade de partículas de aerossóis poluídos detectados
- pol_aero_h_mean : Altitude média dos aerossóis poluídos 
- pol_aerossol_h_std: Desvio padrão da altitude dos aerossóis poluídos
- water_cloud: Quantidade de partículas de nuvem de água detectados
- mixed_clouds: Quantidade de particulas de nuvem mista detectados
- molecular: Quantidade de particulas molecular detectados
- rain_dust: Quantidade de particulas de chuva/poeira detectados
- ice_dust_ash: Quantidade de particulas de gelo/poeira/cinzas detectados
- cloud_base1: Altitude da base de nuvem 1
- cloud_peak1: Altitude de pico de nuvem 1
- cloud_top1: Altitude de topo de nuvem 1
- cloud_base2: Altitude da base de nuvem 2
- cloud_peak2:  Altitude de pico de nuvem 2
- cloud_top2: Altitude de topo de nuvem 2
- cloud_base3: Altitude da base de nuvem 3
- cloud_peak3: Altitude da pico de nuvem 3
- cloud_top3: Altitude da topo de nuvem 3

### Parâmetros
- __path: str__<br>
  Caminho/Diretório da pasta que contém os arquivos .nc

- __file_name: str__<br>
  Nome que será dado ao csv gerado na extração.

### Exemplo de chamada 
```python
dataframe = extract_info('/caminho/da/pasta/com/arquivos', 'LIDAR-2023'):
dataframe.head()
```
  
