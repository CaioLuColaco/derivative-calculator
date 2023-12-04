from pyfiglet import Figlet

def gerar_ascii_art(texto):
    f = Figlet(font='slant')  # Escolha uma fonte, 'slant' é apenas um exemplo
    ascii_art = f.renderText(texto)
    return ascii_art

banner = gerar_ascii_art("Derivative Calculator")
print(banner)

def calculadora(expression):

    terms = formatMultiplications(expression) # [expressão sem a multiplicação, expressão da multiplicação já derivada]

    derivadasComuns = calcular_derivada(terms[0])

    return derivadasComuns + terms[1]

def formatMultiplications(expression):
    multiplicatorPosition = expression.find(") * (")
    if multiplicatorPosition != -1: # Verifica se existe pelo menos uma multiplicação na expressão
        begin = expression.find("(")
        final = expression.find(")", multiplicatorPosition + 1)

        firstExpression = expression[begin + 1: multiplicatorPosition]
        secondExpression = expression[multiplicatorPosition + 5 : final]

        if begin > 1:
            sinal = expression[begin - 2]
            return [expression.replace(f'{sinal} ({firstExpression}) * ({secondExpression})', ""), f'{sinal} ({firstExpression}) * ({calcular_derivada(secondExpression)}) {sinal} ({calcular_derivada(firstExpression)}) * ({secondExpression})']

        return [expression.replace(f'{sinal} ({firstExpression}) * ({secondExpression})', ""), f'+ ({firstExpression}) * ({calcular_derivada(secondExpression)}) + ({calcular_derivada(firstExpression)}) * ({secondExpression})']
    
    return [expression, ""]
    

def calcular_derivada(expressao):
    # Dividir a string pelos espaços em branco e remover espaços no início e no final
    resposta = []
    componentes = [elemento.strip() for elemento in expressao.split()]

    for elemento in componentes:

        if elemento == "-" or elemento == "+": # Separando sinais
            resposta.append(elemento)

        elif not "x" in elemento: # Derivando numeros sem variaveis
            resposta.append("0")

        elif "e^" in elemento: # Para elementos do tipo: e^x
            resposta.append(elemento)

        else: # Derivando componentes com variáveis
            numeros = elemento.split("x") # Separa a multiplicação do expoente
            if "sin" in elemento:
                if "^" in elemento:
                    multiplicador = 1
                    if "*" in numeros[0]:
                        multiplicador = int(numeros[0].replace("*sin", ""))
                    expoente = int(numeros[1].replace("^", ""))
                    multiplicador = multiplicador*expoente
                    resposta.append(f'{multiplicador}*x*cosx^{expoente}')
                else:
                    resposta.append(elemento.replace("sin", "cos"))

            elif "cos" in elemento:
                if "^" in elemento:
                    multiplicador = 1
                    if "*" in numeros[0]:
                        multiplicador = int(numeros[0].replace("*cos", ""))
                    expoente = int(numeros[1].replace("^", ""))
                    multiplicador = -multiplicador * expoente
                    resposta.append(f'- {multiplicador*-1}*x*sinx^{expoente}') if multiplicador <= 0 else resposta.append(f'{multiplicador}*x*sinx^{expoente}')
                else:
                    resposta.append(elemento.replace("cos", "-sin"))
            elif "tan" in elemento:
                if "^" in elemento:
                    multiplicador = 1
                    if "*" in numeros[0]:
                        multiplicador = int(numeros[0].replace("*tan", ""))
                    expoente = int(numeros[1].replace("^", ""))
                    multiplicador = multiplicador * expoente
                    resposta.append(f'{multiplicador}*x*sec^2(x^{expoente})')
                else:
                    resposta.append(elemento.replace("tanx", "sec^2(x)"))
            elif numeros[1] == "" or numeros[1] == "^1": # Caso não tenha expoente ou seja igual a 1, retorna apenas o multiplicador
                resposta.append(numeros[0].replace("*", ""))
            else:
                if numeros[0] == "":
                    multiplicador = 1
                else:    
                    multiplicador = int(numeros[0].replace("*", ""))
                expoente = int(numeros[1].replace("^", ""))

                multiplicador = multiplicador * expoente
                expoente = expoente - 1

                resposta.append(f'{multiplicador}*x^{expoente}' )

    respostaFormatada = ""
    for item in resposta:
        respostaFormatada += f'{item} '
    if "- +" in respostaFormatada:
        respostaFormatada = respostaFormatada.replace("- +", "-")
    if "- -" in respostaFormatada:
        respostaFormatada = respostaFormatada.replace("- -", "+")
    if "+ -" in respostaFormatada:
        respostaFormatada = respostaFormatada.replace("+ -", "-")
    if "+ +" in respostaFormatada:
        respostaFormatada = respostaFormatada.replace("+ +", "+")

    return respostaFormatada

expressao = input("Insira a expressão para a qual deseja calcular a derivada. Exemplo: 2*x^3 - 4*x^2 + 7*x + 1 + e^x + 2*sinx^2 + 2*cosx^2 - 2*tanx^2 + (x^2 + 2*x^3 + 3*x) * (2*x^2 - 4*x) : ")
print("Entrada:")
print(expressao)

print_result = lambda expressao: print(calculadora(expressao))

print("Resposta:")
print_result(expressao)
