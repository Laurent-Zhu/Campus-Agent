from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class ExamGeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory()
        
        # 定义工具集
        self.tools = [
            Tool(
                name="题目生成器",
                func=self._generate_question,
                description="根据知识点生成不同类型的考试题目"
            ),
            Tool(
                name="试卷组装器",
                func=self._assemble_exam,
                description="将生成的题目组装成完整试卷"
            )
        ]
    
    def _generate_question(self, knowledge_point: str, question_type: str) -> dict:
        # 题目生成逻辑
        prompt = PromptTemplate(
            input_variables=["knowledge", "type"],
            template="""
            基于知识点: {knowledge}
            生成一道{type}题，包含:
            1. 题目描述
            2. 参考答案
            3. 详细解析
            4. 难度等级(1-5)
            """
        )
        # 调用LLM生成题目
        response = self.llm(prompt.format(
            knowledge=knowledge_point,
            type=question_type
        ))
        return self._parse_question_response(response)