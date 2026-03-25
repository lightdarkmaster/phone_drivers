class ARM32V7A:
    """ARM32V7A architecture complex"""

    # Architecture configurations
    ARCHITECTURES = {
        "instruction_set": "ARMv7-A",
        "execute_unit": "ARMv7-A",
        "memory_management_unit": "ARMv7-A",
        "load_store_unit": "ARMv7-A",
        "branch_prediction_unit": "ARMv7-A",
        "floating_point_unit": "NEON",
        "graphics_processing_unit": "Mali-G71 MP8",
    }

    def __init__(self):
        for key, value in self.ARCHITECTURES.items():
            setattr(self, key, value)

    def get_architecture(self, arch_type):
        """Get specific architecture by type"""
        return self.ARCHITECTURES.get(arch_type)

    def get_all_features(self):
        """Return all architecture features"""
        return {
            "Instruction Set Architecture": self.instruction_set,
            "Execute Unit Architecture": self.execute_unit,
            "Memory Management Unit Architecture": self.memory_management_unit,
            "Load/Store Unit Architecture": self.load_store_unit,
            "Branch Prediction Unit Architecture": self.branch_prediction_unit,
            "Floating Point Unit Architecture": self.floating_point_unit,
            "Graphics Processing Unit Architecture": self.graphics_processing_unit,
        }

    def get_board_details(self):
        """Alias for get_all_features"""
        return self.get_all_features()
