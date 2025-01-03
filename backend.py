from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

def callLLM(query:str, chat_history: list[dict[str, str]]):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = PineconeVectorStore(index_name="pdf-chat", embedding=embeddings)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_doc_chain= create_stuff_documents_chain(llm, retrieval_qa_prompt)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(llm = llm,retriever = vector_store.as_retriever(), prompt = rephrase_prompt)

    qa = create_retrieval_chain(retriever= history_aware_retriever,combine_docs_chain= stuff_doc_chain)
    result = qa.invoke({"input": query, "chat_history": chat_history})
    new_result = {
        "input": result["input"],
        "output": result["answer"]
    }
    return new_result


if __name__ == "__main__":
    print(callLLM("What is pratik's last job?", []))