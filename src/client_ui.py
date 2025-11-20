"""
Client UI Component
Command-line interface for interacting with ReqMind RAG system.
"""

from typing import Dict, Any


class ClientUI:
    """
    Command-line interface for ReqMind.
    Handles user input, displays responses, and manages conversation flow.
    """
    
    def __init__(self, retrieval_qa):
        """
        Initialize client UI.
        
        Args:
            retrieval_qa: RetrievalQAComponent instance
        """
        self.retrieval_qa = retrieval_qa
        self.conversation_history = []
        
        print("=" * 70)
        print("🤖 Kelly's RAG Chatbot - Requirements Document Q&A System")
        print("=" * 70)
        print()
    
    def display_welcome(self) -> None:
        """Display welcome message and instructions."""
        print("Welcome! I can help you search through requirements documents.")
        print()
        print("Example questions you can ask:")
        print("  • What are the authentication requirements?")
        print("  • What is the maximum response time?")
        print("  • Tell me about the security requirements")
        print("  • What are the scalability requirements?")
        print()
        print("Commands:")
        print("  • 'exit' or 'quit' - Exit the system")
        print("  • 'history' - Show conversation history")
        print("  • 'clear' - Clear conversation history")
        print()
        print("-" * 70)
        print()
    
    def send_query(self, query: str) -> Dict[str, Any]:
        """
        Send query to RetrievalQA system.
        
        Args:
            query: User's question
            
        Returns:
            Response dictionary
        """
        response = self.retrieval_qa.process_query(query)
        
        # Store in history
        self.conversation_history.append({
            "query": query,
            "response": response
        })
        
        return response
    
    def display_response(self, response: Dict[str, Any]) -> None:
        """
        Display formatted response with sources.
        
        Args:
            response: Response dictionary from RetrievalQA
        """
        # Display source documents (Task 5c - first 200 characters)
        if response.get("source_documents"):
            print("\n📚 Source Documents (first 200 characters):")
            print("-" * 70)
            for i, doc in enumerate(response["source_documents"], 1):
                snippet = doc.page_content[:200]
                print(f"Source {i}: {snippet}")
                print()
        
        # Display the bot-generated answer (Task 5c)
        print("📝 Answer:")
        print("-" * 70)
        print(response["result"])
        print("-" * 70)
        print()
    
    def show_error(self, error: str) -> None:
        """
        Display error message.
        
        Args:
            error: Error message to display
        """
        print(f"\n❌ Error: {error}\n")
    
    def show_history(self) -> None:
        """Display conversation history."""
        if not self.conversation_history:
            print("\nNo conversation history yet.\n")
            return
        
        print("\n📜 Conversation History:")
        print("=" * 70)
        for i, item in enumerate(self.conversation_history, 1):
            print(f"\n[{i}] Q: {item['query']}")
            print(f"    A: {item['response']['result'][:150]}...")
        print("\n" + "=" * 70 + "\n")
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        print("\n✓ Conversation history cleared.\n")
    
    def run(self) -> None:
        """
        Main interaction loop.
        Continuously prompts user for queries until exit.
        """
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                query = input("💬 Your question: ").strip()
                
                # Handle empty input
                if not query:
                    continue
                
                # Handle commands
                if query.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thank you for using ReqMind! Goodbye!\n")
                    break
                
                if query.lower() == 'history':
                    self.show_history()
                    continue
                
                if query.lower() == 'clear':
                    self.clear_history()
                    continue
                
                # Process query
                print("\n🔍 Searching documents...")
                response = self.send_query(query)
                
                # Display response
                self.display_response(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using ReqMind! Goodbye!\n")
                break
            except Exception as e:
                self.show_error(str(e))
    
    def query_once(self, query: str) -> None:
        """
        Process a single query (useful for testing).
        
        Args:
            query: Question to ask
        """
        print(f"\n💬 Question: {query}")
        response = self.send_query(query)
        self.display_response(response)
