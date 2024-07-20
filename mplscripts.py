import pandas as pd
import numpy as np
import xarray as xr
import os


def particle_height(dataset: xr.Dataset, particle_value: int) -> tuple:
    '''
    Função que calcula a altitude média e o desvio padrão de uma particula do MPL. 

    ### Parametros:

    - dataset: Dataset do xarray que contém os dados do MPL

    - particle_value: Valor inteiro referente ao tipo de particula a ser analisada. 
    Os valores são (0 - Water Cloud, 1 - Mixed Cloud, 2 - Ice/Dust/Ash, 3 - Rain/Dust, 4 - Molecular,  5 - Clean Aerossol, 6 - Polluted Aerossol, 7 - Undefined)
    Estes valore são classificados pelo próprio LIDAR

    Exemplo de chamada para altura média dos aerossois limpos:

    particle_height(dataset, 6)
    '''

    indexes = np.where(dataset['particle_type'].values[0] == particle_value)[0]
    values = []

    for i in indexes:
        values.append(dataset['range_nrb'].values[i])

    height = np.array(values)

    return height.mean(), height.std()


def extract_info_mpl(PATH: str) -> pd.DataFrame:
    """
    Função que recebe um diretório da pasta onde estão os arquivos .nc que serão extraídas as informações.

    ### Parametro: 
    - PATH: Caminho/diretório da pasta onde estão conditos os arquivos NetCDF (.nc) do Mini MPL

    Exemplo de chamada:

    extract_info_mpl('./home/mpl/2023')
    """
    print('Extraindo as informações dos arquivos em:' + PATH + '...')
    print('Por favor, aguarde!')

    # Listas das variáveis que serão extraídas
    data_hora = []
    clp = []
    aod = []
    temp = []
    clean_aerossol = []
    clean_aerossol_h_mean = []
    clean_aerossol_h_std = []
    polluted_aerosol = []
    pol_aerossol_h_mean = []
    pol_aerossol_h_std = []
    rain_dust = []
    ice_dust_ash = []
    ice_h_mean = []
    ice_h_std = []
    water_clouds = []
    wcloud_h_mean = []
    wcloud_h_std = []
    mixed_clouds = []
    mcloud_h_mean = []
    mcloud_h_std = []
    molecular = []
    mol_h_mean = []
    mol_h_std = []
  

    # For para percorrer a pasta com os dados .nc
    for arquivo in os.listdir(PATH):
        if arquivo.endswith('.nc'):
            nome_arquivo = '/' + arquivo
            try:
                ds = xr.open_dataset(PATH + nome_arquivo)

                # Obtendo data e hora
                data_str = ds['date_yyyyMMdd'].data[0]
                hora_str = ds['time_hhmmss'].data[0]

                # Extraindo a altura média dos aerossois
                aero_media, aero_std = particle_height(ds, 5)
                clean_aerossol_h_mean.append(aero_media)
                clean_aerossol_h_std.append(aero_std)
            
                pol_media, pol_std = particle_height(ds, 6)
                pol_aerossol_h_mean.append(pol_media)
                pol_aerossol_h_std.append(pol_std)
                
                ice_media, ice_std = particle_height(ds, 2)
                ice_h_mean.append(ice_media)
                ice_h_std.append(ice_std)
                
                mol_media, mol_std = particle_height(ds, 4)
                mol_h_mean.append(mol_media)
                mol_h_std.append(mol_std)
                
                wcloud_media, wcloud_std = particle_height(ds, 0)
                wcloud_h_mean.append(wcloud_media)
                wcloud_h_std.append(wcloud_std)
                
                mcloud_media, mcloud_std = particle_height(ds, 1)
                mcloud_h_mean.append(mcloud_media)
                mcloud_h_std.append(mcloud_std)

                # Normalizando o AOD
                if ds['aod'].values[0] < 0:
                    aod_value = 0
                elif ds['aod'].values[0] > 2:
                    aod_value = 2
                else:
                    aod_value = ds['aod'].values[0]

                # Adicionando os dados as listas de variáveis
                clean_aerossol.append(ds['particle_type'].data[0].tolist().count(5))
                polluted_aerosol.append(ds['particle_type'].data[0].tolist().count(6))
                data_hora.append(data_str+' '+hora_str)
                clp.append(ds['pbls'].values[0][0]) # Altura da CLP
                aod.append(aod_value) # Valor da CLP 
                temp.append(ds['detector_temperature'].data[0])
                
                # Contagem de particulas 
                rain_dust.append(ds['particle_type'].data[0].tolist().count(3)) # Rain/Dust
                ice_dust_ash.append(ds['particle_type'].data[0].tolist().count(2)) # Ice/Dust/Ash
                molecular.append(ds['particle_type'].data[0].tolist().count(4)) # Molecular
                water_clouds.append(ds['particle_type'].data[0].tolist().count(0)) # Water Clouds
                mixed_clouds.append(ds['particle_type'].data[0].tolist().count(1)) # Mixed Clouds

                # Criando um dataframe do pandas para agrupar os dados
                df = pd.DataFrame({
                    'data_hora': data_hora,
                    'temperatura': temp,
                    'aod': aod,
                    'clp': clp,
                    'clean_aerossol': clean_aerossol,
                    'clean_aero_h_mean': clean_aerossol_h_mean,
                    'clean_aero_h_std': clean_aerossol_h_std,
                    'polluted_aerossol': polluted_aerosol,
                    'pol_aero_h_mean': pol_aerossol_h_mean,
                    'pol_aerossol_h_std': pol_aerossol_h_std,
                    'water_cloud': water_clouds,
                    'wcloud_h_mean': wcloud_h_mean,
                    'wcloud_h_std':wcloud_h_std,
                    'mixed_clouds': mixed_clouds,
                    'mcloud_h_mean': mcloud_h_mean,
                    'mcloud_h_std':mcloud_h_std,
                    'molecular': molecular,
                    'mol_h_mean':mol_h_mean,
                    'mol_h_std':mol_h_std,
                    'rain_dust': rain_dust,
                    'ice_dust_ash': ice_dust_ash,
                    'ice_h_mean':ice_h_mean,
                    'ice_h_std':ice_h_std,
                })

                # Convertendo a coluna data_hora de str para datetime
                df['data_hora'] = pd.to_datetime(df['data_hora'], format='%Y%m%d %H%M%S')

                # Convertendo o horário de GMT para Local
                df['data_hora'] = df['data_hora'] - pd.DateOffset(hours=3)

                # Ordenando o dataframe pela data
                df.sort_values('data_hora', inplace=True)
                df.reset_index(inplace=True)
                df.drop(columns=['index'], inplace=True)

            except Exception:
                print(f'Erro inesperado: Não foi possível extrair informações de {arquivo}')
                print(Exception)
                print('Extraindo informações dos demais arquivos')
                continue

    print('Encerrado')
    return df 


def extract_cloud_height(PATH:str) -> pd.DataFrame:
    """
    Função que recebe um diretório da pasta onde estão os arquivos .nc que serão extraídas as informações de altura de nuvens.

    ### Parametro: 
    - PATH: Caminho/diretório da pasta onde estão conditos os arquivos NetCDF (.nc) do Mini MPL

    Exemplo de chamada:

    extract_cloud_height('./home/mpl/2023')
    """
    data_hora = []
    cloud_base1 = []
    cloud_peak1 = []
    cloud_top1 = []
    cloud_base2 = []
    cloud_peak2 = []
    cloud_top2 = []
    cloud_base3 = []
    cloud_peak3 = []
    cloud_top3 = []
    
    print('Extraindo as informações dos arquivos em:' + PATH + '...')
    print('Por favor, aguarde!')
    
     # For para percorrer a pasta com os dados .nc
    for arquivo in os.listdir(PATH):
        if arquivo.endswith('.nc'):
            nome_arquivo = '/' + arquivo
            try:
                ds = xr.open_dataset(PATH + nome_arquivo)

                # Obtendo data e hora
                data_str = ds['date_yyyyMMdd'].data[0]
                hora_str = ds['time_hhmmss'].data[0]

                # Coletando as posições de base, pico e topo das nuvens
                cloud_base1.append(ds['clouds'].data.tolist()[0][0][0])
                cloud_peak1.append(ds['clouds'].data.tolist()[0][0][1])
                cloud_top1.append(ds['clouds'].data.tolist()[0][0][2])

                cloud_base2.append(ds['clouds'].data.tolist()[0][1][0])
                cloud_peak2.append(ds['clouds'].data.tolist()[0][1][1])
                cloud_top2.append(ds['clouds'].data.tolist()[0][1][2])

                cloud_base3.append(ds['clouds'].data.tolist()[0][2][0])
                cloud_peak3.append(ds['clouds'].data.tolist()[0][2][1])
                cloud_top3.append(ds['clouds'].data.tolist()[0][2][2])
                
                data_hora.append(data_str+' '+hora_str)

                # Criando um dataframe do pandas para agrupar os dados
                df = pd.DataFrame({
                    'data_hora': data_hora,
                    'cloud_base1': cloud_base1,
                    'cloud_peak1': cloud_peak1,
                    'cloud_top1': cloud_top1,
                    'cloud_base2': cloud_base2,
                    'cloud_peak2': cloud_peak2,
                    'cloud_top2': cloud_top2,
                    'cloud_base3': cloud_base3,
                    'cloud_peak3': cloud_peak3,
                    'cloud_top3': cloud_top3,
                })

                # Convertendo a coluna data_hora de str para datetime
                df['data_hora'] = pd.to_datetime(df['data_hora'], format='%Y%m%d %H%M%S')

                # Convertendo o horário de GMT para Local
                df['data_hora'] = df['data_hora'] - pd.DateOffset(hours=3)

                # Ordenando o dataframe pela data
                df.sort_values('data_hora', inplace=True)
                df.reset_index(inplace=True)
                df.drop(columns=['index'], inplace=True)

            except Exception:
                print(f'Erro inesperado: Não foi possível extrair informações de {arquivo}')
                print(Exception)
                print('Extraindo informações dos demais arquivos')
                continue

    print('Encerrado')
    return df 