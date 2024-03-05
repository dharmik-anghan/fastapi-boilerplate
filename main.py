import uvicorn
from src.config import Config
if __name__ == "__main__":
    uvicorn.run("src.app:app", host= Config.HOST , port= int(Config.PORT) , reload= True)