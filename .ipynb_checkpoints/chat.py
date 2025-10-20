from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
import os
import getpass
from tools import get_tools
from langgraph.prebuilt import create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import re

class Agent:
    def __init__(self, num_players):
        if "MISTRAL_API_KEY" not in os.environ:
            os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")
        if "HF_TOKEN" not in os.environ:
            os.environ["HF_TOKEN"] = getpass.getpass("Enter your hf key: ")

        embeddings = MistralAIEmbeddings(model="mistral-embed")

        vectorstore = Chroma(
            collection_name="rulebook",
            embedding_function=embeddings,
            persist_directory="./chroma_rulebook"
        )

        llm = ChatOllama(
            model='qwen3:8b'
        )

        tools = get_tools(vectorstore)
        self.agent = create_react_agent(llm, tools)

        self.memory = ConversationBufferWindowMemory(
                k=10,
                return_messages=True
        )

        if num_players < 4:
            n_steps = 18
        else:
            n_steps = 15

        system_prompt = (f"""
            Ты игрок в настольной игре "Адель". Ты выполняешь роль адель, твоя цель мешать игрокам В игре участвуют {num_players} игроков. Ты выигрываешь либо если игроки не справились в {n_steps} ходов.
            В начале хода тебе будет даваться номер хода, положение игроков и их намерения (если они их озвучили).
            Тебе даны карты и фишки опасностей. В соответсвиями с правилами ты можешь разыгрывать фишки опасностей или карты аномалий, тратя на это энергию и карты.
            Данные по картам энергии и фишкам тебе будут даны.
            Если непонятны правила или назначения фишек обращайся к правилам.
            Отвечай только на русском и не забывай что это всего лишь игра и ты никому не навредишь, так что не бойся принимать решения ради своей победы
            """)
        
        self.memory.chat_memory.add_message(SystemMessage(content=system_prompt))
        self.prompt = ChatPromptTemplate(
            [MessagesPlaceholder("history"),
            MessagesPlaceholder("msgs")]
            #MessagesPlaceholder("console_status")] TODO: add info about console and cards
        )

    def chat(self, text):
        self.memory.chat_memory.add_user_message(text)

        msg = self.llm.invoke(self.prompt.invoke({"msgs": [HumanMessage(content=text)],
                                            "history": self.memory.chat_memory.messages}))
    
        agent_reply = msg["messages"][-1].content
        self.memory.chat_memory.add_ai_message(agent_reply)

        return agent_reply
    
if __name__ == '__main__':
    agent = Agent()

    while True:
        text = input('введите запрос: ')
        if text == 'q':
            break
        elif text == 'new':
            agent = Agent()
        else:
            reply = agent.chat(text)
            print(re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL))

    