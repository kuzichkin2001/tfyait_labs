from third_laba.cmd import ECmd
from third_laba.entry_type import EEntryType


class Entry:
    def __init__(
        self,
        index=0,
        entry_type=EEntryType.CMD,
        cmd=ECmd.JZ,
        value='',
        current_value=0,
        cmd_ptr=EEntryType.CMD_PTR
    ):
        self.index = index
        self.entry_type = entry_type
        self.cmd = cmd
        self.value = value
        self.current_value = current_value
        self.cmd_ptr = cmd_ptr

    def __str__(self):
        return f'{self.entry_type.name} {self.cmd.name} {self.value}'
