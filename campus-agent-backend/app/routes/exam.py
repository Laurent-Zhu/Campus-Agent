from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from app.utils.model_client import ChatGLMClient
from app.utils.pdf_utils import create_pdf
import os

router = APIRouter()

@router.post("/generate_exam")
async def generate_exam(prompt: str):
    client = ChatGLMClient()
    try:
        # Generate text using the model
        generated_content = await client.generate_text(prompt)
        
        # Create a PDF from the generated content
        pdf_path = create_pdf(generated_content)
        
        return {"pdf_url": pdf_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download_exam/{filename}")
async def download_exam(filename: str):
    pdf_path = os.path.join("path_to_your_pdf_directory", filename)
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf', filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")