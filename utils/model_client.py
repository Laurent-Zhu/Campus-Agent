import httpx
import json
import hmac
import base64
import time
import hashlib
from config.model_config import ModelConfig

class ChatGLMClient:
    def __init__(self):
        self.config = ModelConfig()
        self.api_key = self.config.API_KEY.strip()
        self.client = httpx.AsyncClient(
            base_url=self.config.API_BASE_URL,
            headers={
                "Authorization": self._generate_auth_string(),  # 使用新的认证方式
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=30.0
        )
    
    def _generate_auth_string(self) -> str:
        """生成认证字符串"""
        try:
            api_key_id, api_key_secret = self.api_key.split('.')
            # 生成 HMAC-SHA256 签名
            timestamp = str(int(time.time()))
            signature = hmac.new(
                api_key_secret.encode('utf-8'),
                f"{timestamp}.{api_key_id}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return f"{api_key_id}.{timestamp}.{signature}"
        except Exception as e:
            raise Exception(f"生成认证字符串失败: {str(e)}")

    async def generate_text(self, prompt: str) -> str:
        """调用 API 生成文本"""
        try:
            # 更新认证头
            self.client.headers["Authorization"] = self._generate_auth_string()
            
            request_data = {
                "model": self.config.API_VERSION,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            }
            print("Request Headers:", self.client.headers)
            print("Request Data:", json.dumps(request_data, ensure_ascii=False))
            
            response = await self.client.post(
                "/invoke",
                json=request_data
            )
            
            # 打印完整响应
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            if not result.get("success", False):
                error_msg = result.get("msg", "未知错误")
                raise Exception(error_msg)
            
            return result["data"]["choices"][0]["content"]
            
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")

    async def close(self):
        await self.client.aclose()