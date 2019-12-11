import datetime, sys

initalDate = datetime.datetime.now()
public = {
    #"data": {"dia": initalDate.day, "mes": initalDate.month, "ano": initalDate.year},
    "data": initalDate,
    "cadastrados": 0,
    "alugados": 0,
    "atrasos": 0
}
def init():
    atualizar()
    print("- Data atual: "+public["data"].strftime("%d/%m/%Y")+"\n- Quantidade de veículos cadastrados: "+str(public["cadastrados"])+"\n- Quantidade de veículos alugados: "+str(public["alugados"])+"\n- Quantidade de veiculos atrasados: "+str(public["atrasos"]))
    print("-"*50)
    print("Escolha uma opção digitando a letra que a representa: ")
    print("a. Consultar veículos\nb. Adicionar veículos\nc. Alugar/reservar veículos\nd. Devolver/liberar veículos\ne. Excluir veículos\nf. Avançar data atual\ng. Sair")
    foward()

def foward():
    option = input()
    if(option == "a"):
        consultar()
    elif(option == "b"):
        adicionar()
    elif(option == "c"):
        alugar()
    elif(option == "d"):
        devolver()
    elif(option == "e"):
        excluir()
    elif(option == "f"):
        avancar()
    elif(option == "g"):
        sys.exit(0)
    else:
        print("Digite somente a letra da opção escolhida")
        init()

veiculos = {}
def consultar():
    print("-"*50)
    print("CONSULTAR VEÍCULOS")
    for keyCodigo,veiculo in veiculos.items():
        print("Código: "+str(veiculo["codigo"])+" | Modelo: "+veiculo["modelo"]+" | Status: "+veiculo["status"])
    print("Para consultar detalhes, digite o código e para voltar digite qualquer letra ou um numero negativo: ")
    codigo = input()
    if codigo.isdigit():
        if veiculos[codigo]:
            print("\n"+("-"*50)+"\nDETALHES\nCódigo: "+str(codigo)+" | Marca: "+veiculo["marca"]+" | Ano: "+str(veiculo["ano"])+" |  Valor da diária: "+str(veiculo["valor"]))
        else:
            print("O código não existe")
    else:
        init()
    consultar()

def adicionar():
    novo = {
        "codigo": 0,
        "marca": "",
        "modelo": "",
        "ano": "",
        "valor": 0,
        "status": "disponivel", # reservado, alugado, atrasado
        "nome": "",
        "diasReservados": [],
        "qDiasAlugados": 0,
        "qDiasAtrasados": 0
    }
    print("-"*50)
    print("ADCIONAR VEICULO\nMarca: ")
    novo["marca"] = input()
    print("Modelo: ")
    novo["modelo"] = input()
    print("Ano: ")
    novo["ano"] = int(input())
    print("Valor da diária: ")
    novo["valor"] = float(input())
    aux = [0]
    for veiculo in veiculos:
        aux.append(int(veiculo))
    novo["codigo"] = max(aux)+1
    veiculos[str(novo["codigo"])] = novo
    public["cadastrados"] += 1
    init()

def alugar():
    novoAluguel = {
        "nome": "",
        "codigo": "",
        "inicio": "",
        "dias": 0
    }
    print("-"*50)
    print("ALUGAR/RESERVAR VEÍCULO")
    print("Nome do locatário: ")
    novoAluguel["nome"] = input()
    print("Data de inicio do aluguel(formato: dd/mm/aaaa): ")
    novoAluguel["inicio"] = input()
    print("Quantidade de dias: ")
    novoAluguel["dias"] = int(input())
    print("Codigo do veiculo: ")
    novoAluguel["codigo"] = input()
    veiculo = veiculos[novoAluguel["codigo"]]
    diasGerados = []
    startDate = datetime.datetime.strptime(novoAluguel["inicio"], "%d/%m/%Y")
    available = True
    timeLimit = True
    for dt in (startDate + datetime.timedelta(days=x*1) for x in range(novoAluguel["dias"])):
        if(abs(dt - public["data"]).days > 30):
            timeLimit = False
        genStr = dt.strftime("%d/%m/%Y")
        diasGerados.append(genStr)
        if(available):
            available = not (genStr in veiculo["diasReservados"])
    if(available and timeLimit):
        veiculos[novoAluguel["codigo"]]["diasReservados"].extend(diasGerados)
        veiculos[novoAluguel["codigo"]]["status"] = "reservado"
        veiculos[novoAluguel["codigo"]]["nome"] = novoAluguel["nome"]
        print("Veiculo "+novoAluguel["codigo"]+" reservado/alugado com sucesso")
    elif(not timeLimit):
        print("O veiculo NÃO pode ser reservado/alugado por estar fora do limite de dias adiante da data atual")
    else:
        print("O veiculo NÃO pode ser reservado/alugado para a data inserida")
    init()


def devolver():
    print("-"*50)
    print("DEVOLVER/LIBERAR VEÍCULO")
    for codigo,veiculo in veiculos.items():
        if(veiculo["status"] != "disponivel" ):
            print("Codigo: "+codigo+" | Status: "+veiculo["status"])
    print("Insira o codigo para devolver/liberar o veiculo: ")
    codigoIn = input()
    valor = veiculos[codigoIn]["valor"]
    print("Nome do cliente: "+veiculos[codigoIn]["nome"])
    if(veiculos[codigoIn]["status"] == "reservado"):
        veiculos[codigoIn]["status"] = "disponivel"
        veiculos[codigoIn]["diasReservados"] = []
    elif(veiculos[codigoIn]["status"] == "alugado"):
        veiculos[codigoIn]["status"] = "disponivel"
        veiculos[codigoIn]["diasReservados"] = []
        print("Valor a pagar: "+str(valor * veiculos[codigoIn]["qDiasAlugados"]))
    elif(veiculos[codigoIn]["status"] == "atrasado"):
        veiculos[codigoIn]["status"] = "disponivel"
        veiculos[codigoIn]["nome"] = ""
        veiculos[codigoIn]["diasReservados"] = []
        print("Valor a pagar com atraso: "+str((valor * 2 * veiculos[codigoIn]["qDiasAtrasados"]) + (valor * veiculos[codigoIn]["qDiasAlugados"])))
    init()

def excluir():
    print("-"*50)
    print("EXCLUIR VEÍCULO")
    print("Insira o codigo de um veiculo para deletar ou uma letra ou numero negativo para voltar: ")
    codigo = input()
    if(codigo.isdigit()):
        if(veiculos[codigo]["status"] == "disponivel"):
            del veiculos[codigo]
            print("Veiculo "+codigo+" excluido")
        else:
            print("Veiculo não disponivel")
    else:
        init()
    excluir()

def avancar():
    public["data"] += datetime.timedelta(days=1)
    print("Nova data: ", public["data"].strftime("%d/%m/%Y"))
    init()

def atualizar():
    strCurrentDate = public["data"].strftime("%d/%m/%Y")
    strYesterday = (public["data"] - datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    qAlugados = 0
    qAtrasados = 0
    for codigo,veiculo in veiculos.items():
        if(strCurrentDate in veiculo["diasReservados"]):
            veiculos[codigo]["status"] = "alugado"
            veiculos[codigo]["qDiasAlugados"] += 1
            qAlugados += 1
            if(strYesterday in veiculo["diasReservados"]):
                del veiculos[codigo]["diasReservados"][veiculo["diasReservados"].index(strYesterday)]
        if(not (strCurrentDate in veiculo["diasReservados"]) and veiculo["status"] == "alugado"):
            veiculos[codigo]["status"] = "atrasado"
            veiculos[codigo]["qDiasAtrasados"] += 1
            qAtrasados += 1
        elif(veiculos[codigo]["status"] == "atrasado"):
            veiculos[codigo]["qDiasAtrasados"] += 1
            qAtrasados += 1
    public["alugados"] = qAlugados
    public["atrasos"] =  qAtrasados

init()
