def get_tools(db):
    retriever = db.as_retriever(search_kwargs={"k": 3})

    def retrieve_rulebook(query: str):
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])

    tools = [
        {
            "name": "Поиск по правилам",
            "description": "Поиск актуальных правил в книге правил",
            "function": retrieve_rulebook
        }
    ]
    return tools