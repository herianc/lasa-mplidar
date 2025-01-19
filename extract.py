from mplscripts import extract_info_mpl
import os
import warnings

warnings.filterwarnings("ignore")

# COLOQUE O NOME DO SEU DIRETÓRIO AQUI
PATH = "2024-10"

length = len(os.listdir(PATH))

print(f"O diretório selecionado tem {length} arquivos.")

df = extract_info_mpl(PATH)

print("Dados extraídos")
print(df[["data_hora", "aod", "clp"]].head().to_string())

os.makedirs("outputs", exist_ok=True)
df.to_csv("outputs/output.csv", index=False)


print("CSV disponível na pasta outputs.")
print("Fim.")
