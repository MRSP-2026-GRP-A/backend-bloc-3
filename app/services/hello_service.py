class HelloService:
    @staticmethod
    def get_greeting(name: str) -> str:
        # Imagine ici un calcul complexe ou une analyse Scikit-Learn plus tard
        return f"Hello {name} ! Bienvenue dans ton API FastAPI."