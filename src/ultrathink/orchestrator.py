"""
AI Orchestrator for managing multiple AI models.

This module handles coordination between different AI models and manages
their lifecycle and interactions.
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict

# AI provider imports
import anthropic
import boto3
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

from .models import AIModel, AnalysisResult, TaskType

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """Orchestrates multiple AI models for different tasks."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the AI orchestrator.

        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config
        self.claude_client = None
        self.gemini_model = None
        self.bedrock_client = None
        self._initialize_models()

    def _initialize_models(self):
        """Initialize AI model clients"""
        # Claude setup
        if self.config.get('claude_api_key'):
            self.claude_client = anthropic.Anthropic(
                api_key=self.config['claude_api_key']
            )

        # Google Vertex AI setup
        if self.config.get('google_project_id'):
            aiplatform.init(project=self.config['google_project_id'])
            self.gemini_model = GenerativeModel('gemini-pro')

        # AWS Bedrock setup
        if self.config.get('aws_region'):
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.config['aws_region']
            )

    async def route_task(self, task_type: TaskType, context: Dict[str, Any]) -> AnalysisResult:
        """
        Route task to appropriate AI model based on type and requirements.

        Args:
            task_type: Type of task to perform
            context: Context and parameters for the task

        Returns:
            Analysis result from the AI model
        """
        model = self._select_model(task_type, context)

        if model == AIModel.CLAUDE_OPUS:
            return await self._process_with_claude(task_type, context)
        elif model == AIModel.GEMINI_ULTRA:
            return await self._process_with_gemini(task_type, context)
        elif model == AIModel.AWS_BEDROCK_CLAUDE:
            return await self._process_with_bedrock(task_type, context)
        else:
            raise ValueError(f"Unsupported model: {model}")

    def _select_model(self, task_type: TaskType, context: Dict[str, Any]) -> AIModel:
        """
        Select best model for the task.

        Args:
            task_type: Type of task
            context: Task context

        Returns:
            Selected AI model
        """
        # Complex reasoning tasks -> Claude
        if task_type in [TaskType.ARCHITECTURE_EVOLUTION, TaskType.REFACTORING]:
            return AIModel.CLAUDE_OPUS

        # Multimodal or specialized tasks -> Gemini
        if task_type == TaskType.DOCUMENTATION:
            return AIModel.GEMINI_ULTRA

        # High-throughput tasks -> Bedrock
        if task_type in [TaskType.CODE_REVIEW, TaskType.TEST_GENERATION]:
            return AIModel.AWS_BEDROCK_CLAUDE

        return AIModel.CLAUDE_OPUS  # Default

    async def _process_with_claude(self, task_type: TaskType, context: Dict[str, Any]) -> AnalysisResult:
        """Process task using Claude"""
        if not self.claude_client:
            raise ValueError("Claude client not initialized")

        prompt = self._build_prompt(task_type, context)

        message = self.claude_client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        return self._parse_ai_response(message.content, task_type, AIModel.CLAUDE_OPUS)

    async def _process_with_gemini(self, task_type: TaskType, context: Dict[str, Any]) -> AnalysisResult:
        """Process task using Gemini"""
        if not self.gemini_model:
            raise ValueError("Gemini model not initialized")

        prompt = self._build_prompt(task_type, context)
        response = self.gemini_model.generate_content(prompt)

        return self._parse_ai_response(response.text, task_type, AIModel.GEMINI_ULTRA)

    async def _process_with_bedrock(self, task_type: TaskType, context: Dict[str, Any]) -> AnalysisResult:
        """Process task using AWS Bedrock"""
        if not self.bedrock_client:
            raise ValueError("Bedrock client not initialized")

        prompt = self._build_prompt(task_type, context)

        # Select model based on task complexity
        model_id = self._select_bedrock_model(task_type)

        # Use Messages API format for Claude 3.5+
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        })

        try:
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                contentType='application/json',
                accept='application/json',
                body=body
            )

            result = json.loads(response['body'].read())
            
            # Extract text from Messages API response
            content_blocks = result.get('content', [])
            response_text = ''
            for block in content_blocks:
                if block.get('type') == 'text':
                    response_text += block.get('text', '')
            
            return self._parse_ai_response(response_text, task_type, AIModel.AWS_BEDROCK_CLAUDE)
        
        except Exception as e:
            logger.error(f"Bedrock invocation failed: {e}")
            # Fallback to Claude if available
            if self.claude_client:
                logger.info("Falling back to Claude API")
                return await self._process_with_claude(task_type, context)
            raise

    def _select_bedrock_model(self, task_type: TaskType) -> str:
        """Select appropriate Bedrock model based on task type"""
        # Use Claude 4.5 experimental for complex tasks
        if task_type in [TaskType.ARCHITECTURE_EVOLUTION, TaskType.REFACTORING]:
            return 'anthropic.claude-sonnet-4-5-20250929-v1:0'
        
        # Use Claude 3.5 for standard tasks (faster, cheaper)
        return 'anthropic.claude-3-5-sonnet-20240620-v1:0'

    def _build_prompt(self, task_type: TaskType, context: Dict[str, Any]) -> str:
        """Build task-specific prompt"""
        prompts = {
            TaskType.CODE_REVIEW: """
                Review the following code for:
                - Bugs and potential issues
                - Performance optimizations
                - Security vulnerabilities
                - Code quality and best practices

                Code:
                {code}

                Language: {language}

                Parse metadata (if provided):
                {parse_metadata}

                Provide your analysis as a JSON object with the following structure:
                {{
                    "findings": [
                        {{
                            "line_number": <int>,
                            "severity": "critical|high|medium|low|info",
                            "category": "bug|security|performance|quality|style",
                            "description": "Description of the issue",
                            "suggestion": "How to fix it"
                        }}
                    ],
                    "summary": "Overall assessment of the code",
                    "metrics": {{
                        "quality_score": <float 0-1>,
                        "security_score": <float 0-1>,
                        "maintainability_score": <float 0-1>
                    }}
                }}

                Return ONLY valid JSON, no additional text.
            """,
            TaskType.TEST_GENERATION: """
                Generate comprehensive test cases for the following code:

                Code:
                {code}

                Language: {language}

                Include:
                - Unit tests for all functions
                - Edge cases and error conditions
                - Property-based test ideas
                - Integration test scenarios
            """,
            TaskType.REFACTORING: """
                Refactor the following code for improved:
                - Readability
                - Maintainability
                - Performance
                - Adherence to design patterns

                Code:
                {code}

                Provide the refactored code with explanations.
            """
        }

        template = prompts.get(task_type, "Analyze the following code: {code}")
        return template.format(**context)

    def _parse_ai_response(self, response: Any, task_type: TaskType, model: AIModel) -> AnalysisResult:
        """Parse AI response into structured result"""
        # Extract text from response if it's not already a string
        response_text = str(response)
        if hasattr(response, 'text'):
            response_text = response[0].text if isinstance(response, list) else response.text

        # Try to parse as JSON for structured responses
        findings = []
        suggestions = []
        confidence = 0.85

        try:
            # Try to extract JSON from response (may have markdown code blocks)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed_data = json.loads(json_str)

                # Extract findings
                if 'findings' in parsed_data:
                    findings = parsed_data['findings']

                # Extract suggestions from findings
                suggestions = [f["suggestion"] for f in findings if "suggestion" in f]

                # Calculate confidence from metrics if available
                if 'metrics' in parsed_data:
                    metrics = parsed_data['metrics']
                    scores = [v for v in metrics.values() if isinstance(v, (int, float))]
                    if scores:
                        confidence = sum(scores) / len(scores)

                logger.info(f"Successfully parsed structured JSON response with {len(findings)} findings")
            else:
                # Fallback to unstructured response
                logger.warning("No JSON found in response, using raw text")
                findings = [{"raw_response": response_text}]
                suggestions = [response_text]

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            # Fallback to unstructured response
            findings = [{"raw_response": response_text, "parse_error": str(e)}]
            suggestions = [response_text]
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            findings = [{"raw_response": response_text, "error": str(e)}]
            suggestions = [response_text]

        return AnalysisResult(
            task_type=task_type,
            findings=findings,
            suggestions=suggestions,
            confidence=confidence,
            model_used=model.value,
            timestamp=datetime.now().isoformat()
        )
