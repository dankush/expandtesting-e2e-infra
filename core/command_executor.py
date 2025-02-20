from dataclasses import dataclass
from typing import List, Optional, Dict
import subprocess
import logging
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class CommandResult:
    """Immutable container for command execution results.
    
    Attributes:
        stdout: Command standard output as string
        stderr: Command standard error as string
        return_code: Command exit status code
        success: Whether command executed successfully
    """
    stdout: str
    stderr: str
    return_code: int
    success: bool

class CommandExecutor(ABC):
    """Abstract base class for command execution."""
    
    @abstractmethod
    def execute(self, command: List[str]) -> CommandResult:
        """Execute command and return results."""
        pass

class SubprocessExecutor(CommandExecutor):
    """Concrete implementation of command executor using subprocess."""
    
    def __init__(self, 
                 working_dir: Optional[str] = None, 
                 env: Optional[Dict] = None,
                 timeout: Optional[float] = None):
        self.working_dir = working_dir
        self.env = env
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, command: List[str]) -> CommandResult:
        """Execute shell command and return results."""
        if not command or not isinstance(command, list):
            raise ValueError("Command must be a non-empty list of strings")
            
        self.logger.debug(f"Executing command: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.working_dir,
                env=self.env,
                timeout=self.timeout,
                check=False
            )
            
            cmd_result = CommandResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                return_code=result.returncode,
                success=result.returncode == 0
            )
            
            if not cmd_result.success:
                self.logger.warning(f"Command returned non-zero exit code: {result.returncode}")
            
            return cmd_result
            
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Command timed out: {str(e)}")
            return CommandResult(
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                return_code=-1,
                success=False
            )
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            raise CommandExecutionError(f"Failed to execute command: {str(e)}")

class CommandExecutionError(Exception):
    """Custom exception for command execution failures."""
    pass