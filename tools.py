def get_tools(db, console):
    retriever = db.as_retriever(search_kwargs={"k": 3})

    def retrieve_rulebook(query: str):
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])

    tools = [
        {
            "name": "Поиск по правилам",
            "description": "Поиск актуальных правил в книге правил",
            "function": retrieve_rulebook
        },
        {
            "name": "Сыграть карту",
            "description": "Позволяет сыграть выбранную фишку в выбранную комнату в соответствии с картами и консолью",
            "function": console.play_card
        }
    ]
    return tools