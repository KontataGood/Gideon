from gideon.core.event import Event
from gideon.core.event_bus import EventBus
from gideon.core.event_type import EventType

from gideon.tools.executor import ToolExecutor
from gideon.tools.registry import ToolRegistry

from gideon.ai.factory import AIFactory
from gideon.ai.manager import AIManager
from gideon.ai.context import ContextManager

from gideon.core.agent import Agent

from gideon.config.manager import ConfigManager
from gideon.platforms.factory import PlatformFactory

from gideon.tools.builtin.calculator import CalculatorTool
from gideon.tools.builtin.open_url import OpenUrlTool
from gideon.tools.builtin.open_application import OpenApplicationTool

from gideon.tools.builtin.process import ProcessTool

class Gideon:
    """
    Центральный объект ассистента.
    """

    def __init__(
        self,
        ai=None,
        memory=None,
        voice=None,
        config=None,
    ):
        self.memory = memory
        self.voice = voice

        self.config = config or ConfigManager(
            "config/config.json"
        )

        # Platform
        self.platform = PlatformFactory.create()

        # Events
        self.event_bus = EventBus()

        # Tools
        self.tools = ToolRegistry()

        self.tools.register(
            CalculatorTool()
        )

        self.tools.register(
            OpenUrlTool(self.platform)
        )

        self.tools.register(
            OpenApplicationTool(self.platform)
        )

        self.tools.register(
            ProcessTool(self.platform)
        )

        # AI
        provider = self.config.get(
            "ai.provider",
            "mock",
        )

        model = self.config.get(
            "ai.model",
            "test",
        )

        self.ai = AIManager(
            AIFactory.create_client(
                provider=provider,
                model=model,
            )
        )

        # Tool executor
        self.tool_executor = ToolExecutor(
            registry=self.tools,
            event_bus=self.event_bus,
        )

        # Context
        self.context = ContextManager(
            system_prompt=(
                "You are Gideon, a personal AI assistant. "
                "Be concise, helpful and intelligent."
            )
        )

        # Agent
        self.agent = Agent(
            ai=self.ai,
            tool_registry=self.tools,
            tool_executor=self.tool_executor,
            context=self.context,
        )

        self._running = False

    def start(self):
        """Запускает ассистента."""

        if self._running:
            return

        self._running = True

        self.event_bus.publish(
            Event(
                type=EventType.SYSTEM_STARTED,
                data={},
            )
        )

        print("Gideon started.")

    def stop(self):
        """Останавливает ассистента."""

        if not self._running:
            return

        self._running = False

        self.event_bus.publish(
            Event(
                type=EventType.SYSTEM_STOPPED,
                data={},
            )
        )

        print("Gideon stopped.")

    @property
    def running(self) -> bool:
        """Возвращает состояние ассистента."""

        return self._running
