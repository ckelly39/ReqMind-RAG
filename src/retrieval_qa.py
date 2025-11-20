"""
RetrievalQA Component
Orchestrates the complete RAG workflow using LangChain's RetrievalQA chain.
Implements Facade pattern to simplify complex RAG interactions.
"""

from typing import Dict, Any
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate


class RetrievalQAComponent:
    """
    Orchestrates RAG workflow: retrieval + generation.
    Uses LangChain's RetrievalQA with "stuff" chain strategy.
    """
    
    def __init__(self, llm, retrieval_component):
        """
        Initialize RetrievalQA component.
        
        Args:
            llm: Custom HuggingFaceInferenceLLM instance
            retrieval_component: RetrievalComponent instance
        """
        self.llm = llm
        self.retrieval_component = retrieval_component
        
        # Create custom prompt template
        self.prompt_template = self._create_prompt_template()
        
        # Create LangChain RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # "stuff" strategy: put all context in one prompt
            retriever=retrieval_component.get_retriever(),
            return_source_documents=True,  # Return sources for citation
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        print(f"✓ RetrievalQA chain created (chain_type='stuff')")
        print("RAG chain successfully created\n")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create prompt template for the LLM.
        Structures how context and query are presented to the model.
        
        Returns:
            PromptTemplate object
        """
        template = """You are a helpful AI assistant specialized in analyzing software requirements documents.

RULES:
- Answer ONLY the question below using the provided context
- If not related to the requirements document, say: "I don't know. This question is not related to the requirements document."
- Cite requirement IDs when available
- Do NOT generate follow-up questions

Context:
{context}

Question: {question}

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query through the complete RAG pipeline.
        
        Steps:
        1. Validate query
        2. Retrieve relevant context (handled by retriever)
        3. Build prompt (handled by chain)
        4. Generate answer (handled by LLM)
        5. Format response
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with:
                - 'result': Generated answer
                - 'source_documents': List of source Document objects
                - 'query': Original query
        """
        # Validate query
        if not query or not query.strip():
            return {
                "result": "Please provide a valid question.",
                "source_documents": [],
                "query": query
            }
        
        try:
            # Run the RAG chain
            # This internally does: retrieve -> build_prompt -> generate -> format
            response = self.qa_chain.invoke({"query": query})
            
            return {
                "result": response["result"],
                "source_documents": response["source_documents"],
                "query": query
            }
            
        except Exception as e:
            # Handle errors gracefully
            return {
                "result": f"Error processing query: {str(e)}",
                "source_documents": [],
                "query": query,
                "error": str(e)
            }
    
    def invoke(self, input_dict: Dict[str, str]) -> Dict[str, Any]:
        """
        LangChain-compatible invoke method.
        
        Args:
            input_dict: Dictionary with 'query' key
            
        Returns:
            Response dictionary
        """
        query = input_dict.get("query", "")
        return self.process_query(query)
