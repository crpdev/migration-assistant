from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import List, Dict

app = FastAPI(title="File Explorer MCP")

class FileExplorerRequest(BaseModel):
    path: str
    file_types: List[str] = ["pom.xml", "java"]

class FileExplorerResponse(BaseModel):
    files: List[Dict[str, str]]
    directories: List[str]

@app.post("/explore", response_model=FileExplorerResponse)
async def explore_directory(request: FileExplorerRequest):
    try:
        if not os.path.exists(request.path):
            raise HTTPException(status_code=404, detail="Path not found")
        
        files = []
        directories = []
        
        for root, dirs, filenames in os.walk(request.path):
            for filename in filenames:
                if any(filename.endswith(ft) for ft in request.file_types):
                    files.append({
                        "path": os.path.join(root, filename),
                        "type": filename.split(".")[-1]
                    })
            directories.extend([os.path.join(root, d) for d in dirs])
        
        return FileExplorerResponse(files=files, directories=directories)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from config import MCP_SERVERS
    
    server_config = MCP_SERVERS["file_explorer"]
    uvicorn.run(app, host=server_config["host"], port=server_config["port"]) 