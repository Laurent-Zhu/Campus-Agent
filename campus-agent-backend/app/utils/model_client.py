from zhipuai import ZhipuAI
from fastapi import HTTPException
from app.utils.pdf_utils import create_pdf

class ChatGLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.client = ZhipuAI(api_key=self.api_key)

    async def generate_text(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"API调用失败: {str(e)}")

    async def generate_pdf(self, prompt: str, filename: str) -> str:
        content = await self.generate_text(prompt)
        pdf_path = create_pdf(content, filename)
        return pdf_path