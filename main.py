# Raspagem de noticías de vários websites de notícias, em tempo real e sobre demanda.
import argparse

class handle_demand:
    def __init__(self):
        pass

    def set_arguments(self):
        parser = argparse.ArgumentParser(description="casa")
        
        country = parser.add_argument("-c", "--country", type=str, default="global", required=False, help="defina a nacionalidade dos sites desejados, padrão é definido como global")
        time_stamp = parser.add_argument("-ts", "--timeStamp", required=False, type=str, default="today", help="insira se a busca deve ser de dias[today] atuais ou em determinado tempo[11/05/2024 - 15/05/2024]")
        websites = parser.add_argument("-ws", "--websites", required=False, type=str, default="all", nargs="+", help="insira quais websites separados por vírgulas no qual deseja raspar.")
        return_format = parser.add_argument("-ot", "--output", required=False, type=str, default="json", nargs="+", help="insira quais formas de retorno deseja receber as respostas.")
        return parser.parse_args()
        
    def parse_arguments(self):
        pass






if __name__ == "__main__":
    handle_demand().set_arguments()