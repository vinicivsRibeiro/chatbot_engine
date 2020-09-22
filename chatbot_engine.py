import pandas as pd
import os
import sys

class Tree():
    def __init__(self):
        pass

    def ask_question(self):
        return self.question

    def check_answer(self,answer):
        if answer == self.answerTrue:
            return self.leftNode
        elif answer == self.answerFalse:
            return self.rightNode
        else:
            return False

df = pd.read_csv("tree_file.csv",sep=';',index_col="ID")

def rec_build_tree(state):
    row = df.loc[state]
    if row["Pergunta"] == "estado final":
        return row["Resposta A"]
    node = Tree()
    node.leftNode = rec_build_tree(int(row["Resposta A"]))
    node.rightNode = rec_build_tree(int(row["Resposta B"]))
    node.question = row["Pergunta"]
    node.answerTrue = row["A"]
    node.answerFalse = row["B"]
    return node

def is_obj(obj):
    return False if type(obj).__name__ == "str" else True

def check_and_create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)    

check_and_create_folder("pedidos")
counter_tickets = 0
while True:
    tree = rec_build_tree(1)
    pedido = "TICKET DO PEDIDO\n"
    estado = tree
    count_erros=0
    while True:
        if count_erros == 2:
            print("ERROS SUCESSIVOS\nVERIFIQUE AS OPÇÕES ANTES DE TENTAR NOVAMENTE\n")
            print("\nBuguei, muitas informações! :/ \nPor favor me reinicie.\nQuem Sabe na próxima estarei mais esperto!? :)")
            break
        opcoes = {1:estado.answerTrue,2:estado.answerFalse}
        print("\nEscolha uma das opções abaixo:"+"\n0 para sair"+"\n1 para "+opcoes[1]+"\n2 para "+opcoes[2]+"\n")
        response = input(estado.ask_question())
        while not response.isnumeric():
            if count_erros == 2:
                print("\nBuguei, muitas informações! :/ \nPor favor me reinicie.\nQuem Sabe na próxima estarei mais esperto!? :)")
                sys.exit()
            print("\nMe desculpe, não conhece essa opção, vamos tentar novamente? :)\n")
            print("Escolha uma das opções abaixo:"+"\n0 para sair"+"\n1 para "+opcoes[1]+"\n2 para "+opcoes[2])
            response = input(estado.ask_question())
            count_erros+=1
            
        if int(response) == 0:
            print("\nAté a próxima, estarei treinando enquanto te aguardo.\n")
            sys.exit()
        question = opcoes[int(response)]
        answer = estado.check_answer(question)
        if answer == False:
            print("\nMe desculpe, não conhece essa opção, vamos tentar novamente? :)")
            count_erros+=1
        elif not is_obj(answer):
            pedido+=question
            break
        else:
            if question == estado.answerTrue:
                pedido+=estado.answerTrue+"\n"
                print(estado.answerTrue)
                estado = answer      
            elif question == estado.answerFalse:
                pedido+=estado.answerFalse+"\n"
                estado = answer
            else:
                print("\nMe desculpe, não conhece essa opção, vamos tentar novamente? :) \n")
                count_erros+=1
    
    if pedido != "TICKET DO PEDIDO\n":
        print("\n{}".format(pedido))
        counter_tickets+=1
        file_name = "pedidos/"+str(counter_tickets)+".txt"
        with open(file_name,'w',encoding="utf-8") as f:
            f.write(pedido)
    print(chr(27) + "[2J")