from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentFormater:    
    @staticmethod
    def split(doc):
        loader = TextLoader(doc, encoding='utf-8')
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 32000,
            chunk_overlap = 0,
            length_function = len,
            is_separator_regex = False,
        )
        
        documents = text_splitter.split_documents(documents)

        return documents