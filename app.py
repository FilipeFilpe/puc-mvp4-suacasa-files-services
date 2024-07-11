import os
import time

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import FileStorage, Info, OpenAPI, Tag
from pydantic import BaseModel, Field

info = Info(title="Serviço de Arquivos", version="1.0.0")
app = OpenAPI(__name__, info=info,)
CORS(app)

class UploadFileForm(BaseModel):
    file: FileStorage
    file_name: str = Field(description="File Name")

class RemoveFileForm(BaseModel):
    path: str


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/upload/file')
def upload_file(form: UploadFileForm):
    path = f"./static/{time.time()}_{form.file_name}"
    form.file.save(path)
    return {"filename": form.file_name, "path": f"http://127.0.0.1:5001/{path}"}, 201

@app.delete('/file')
def remove_file(query: RemoveFileForm):
    path = query.path
    filename = f"./static/{path.split('/')[-1]}"
    if os.path.exists(filename):
        os.remove(filename)
        return {"message": "Arquivo removido com sucesso", "filename": path}, 201
    else:
        return {"message": "Arquivo não encontrado"}, 400

if __name__ == '__main__':
    app.run(debug=True)