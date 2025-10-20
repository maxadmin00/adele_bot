from langchain_unstructured import UnstructuredLoader
import re
from preprocess import preprocess
import getpass
import os
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

if __name__ == '__main__':
    loader = UnstructuredLoader(
        "./adele_rules.pdf",
        chunking_strategy='basic',
        languages= ['ru'],
        max_characters = 10e10
    )
    docs = loader.load()

    parts = re.split(r'\n\n(?=\d+\.\d+)', docs[0].page_content)
    parts = parts[15:]

    texts = [preprocess(t) for t in parts]

    if "MISTRAL_API_KEY" not in os.environ:
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")
    #bTbap9LPxThHl6xa03apaGS6wdhNH4Ue
    if "HF_TOKEN" not in os.environ:
        os.environ["HF_TOKEN"] = getpass.getpass("Enter your hf key: ")
    #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

    embeddings = MistralAIEmbeddings(model="mistral-embed")

    vectorstore = Chroma.from_texts(
        texts,
        embedding=embeddings,
        collection_name="rulebook",
        persist_directory="./chroma_rulebook"
    )