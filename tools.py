from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

def get_tools(db, console):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    class RulebookQuery(BaseModel):
        query: str = Field(description="Запрос, который нужно найти в книге правил")

    class PlayCardInput(BaseModel):
        room: int = Field(description="Номер комнаты, куда нужно сыграть фишку")
        cap: str = Field(description="Тип фишки опасности, например 'пожар' или 'гипоксия'")

    class PlayAnomalyInput(BaseModel):
        anomaly_ind: int = Field(description="Индекс выбранной аномалии (начиная с 0)")

    def retrieve(query:str):
        return "\n\n".join([doc.page_content for doc in retriever.get_relevant_documents(query)])
    
    def play_card(room, cap):
        return console.play_card(room, cap)
    
    def play_anomaly(anomaly_ind):
        return console.play_anomaly(anomaly_ind)

    retrieve_rulebook = StructuredTool.from_function(
        name="Поиск по правилам",
        description="Поиск информации в книге правил по текстовому запросу",
        func=retrieve,
        args_schema=RulebookQuery
    )

    play_card = StructuredTool.from_function(
        name="Сыграть карту опасностей",
        description="Сыграть фишку опасности в указанную комнату. Требует room и cap.",
        func=play_card,
        args_schema=PlayCardInput
    )

    play_anomaly = StructuredTool.from_function(
        name="Сыграть карту аномалий",
        description="Разыграть выбранную аномалию по её индексу. Требует anomaly_ind.",
        func=play_anomaly,
        args_schema=PlayAnomalyInput
    )

    return [retrieve_rulebook, play_card, play_anomaly]