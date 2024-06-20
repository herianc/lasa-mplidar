import pandas as pd
import numpy as np
import xarray as xr
import os


def particle_height(dataset: xr.Dataset, ref_particle: int) -> tuple:
    '''
    Função que calcula a altitude média e o desvio padrão de uma particula do MPL. 

    ### Parametros:

    - dataset: Dataset do xarray que contém os dados do MPL

    - ref_particle: Valor inteiro referente ao tipo de particula a ser analisada. 
    Os valores são (0 - Water Cloud, 1 - Mixed Cloud, 2 - Ice/Dust/Ash, 3 - Rain/Dust, 4 - Molecular,  5 - Clean Aerossol, 6 - Polluted Aerossol, 7 - Undefined)
    Estes valore são classificados pelo próprio lidar

    Exemplo de chamada para altura média dos aerossois limpos:

    particle_height(dataset, 6)
    '''

    indexes = np.where(dataset['particle_type'].values[0] == ref_particle)[0]
    values = []

    for i in indexes:
        values.append(dataset['range_nrb'].values[i])

    height = np.array(values)

    return height.mean(), height.std()


def extract_info_mpl(path: str):
    """
    Função que recebe um diretório da pasta onde estão os arquivos .nc que serão extraídas as informações.

    ### Parametro: 
    - path: Caminho/diretório da pasta onde estão conditos os arquivos NetCDF (.nc) do Mini MPL

    Exemplo de chamada:

    extract_info_mpl('./home/mpl/2023')
    """
    print('Extraindo as informações dos arquivos em:' + path + '...')
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
    water_clouds = []
    mixed_clouds = []
    molecular = []
    cloud_base1 = []
    cloud_peak1 = []
    cloud_top1 = []
    cloud_base2 = []
    cloud_peak2 = []
    cloud_top2 = []
    cloud_base3 = []
    cloud_peak3 = []
    cloud_top3 = []

    # For para percorrer a pasta com os dados .nc
    for arquivo in os.listdir(path):
        if arquivo.endswith('.nc'):
            nome_arquivo = '/' + arquivo
            try:
                ds = xr.open_dataset(path + nome_arquivo)

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

                # Normalizando o AOD
                if ds['aod'].values[0] < 0:
                    aod_value = 0
                elif ds['aod'].values[0] > 2:
                    aod_value = 2
                else:
                    aod_value = ds['aod'].values[0]

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
                    'mixed_clouds': mixed_clouds,
                    'molecular': molecular,
                    'rain_dust': rain_dust,
                    'ice_dust_ash': ice_dust_ash,
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
                df['data_hora'] = pd.to_datetime(
                    df['data_hora'], format='%Y%m%d %H%M%S')

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
