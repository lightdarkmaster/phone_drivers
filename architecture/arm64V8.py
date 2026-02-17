class ARM64V8:
    def __init__(self):
        self.instruction_set_architecture = "ARMv8"
        self.execute_unit_architecture = "ARMv8"
        self.memory_management_unit_architecture = "ARMv8"
        self.load_store_unit_architecture = "ARMv8"
        self.branch_prediction_unit_architecture = "ARMv8"
        self.floating_point_unit_architecture = "NEON"
        self.graphics_processing_unit_architecture = "Mali-G52 MP6"

    def get_instruction_set_architecture(self):
        return self.instruction_set_architecture

    def get_execute_unit_architecture(self):
        return self.execute_unit_architecture

    def get_memory_management_unit_architecture(self):
        return self.memory_management_unit_architecture

    def get_load_store_unit_architecture(self):
        return self.load_store_unit_architecture

    def get_branch_prediction_unit_architecture(self):
        return self.branch_prediction_unit_architecture

    def get_floating_point_unit_architecture(self):
        return self.floating_point_unit_architecture

    def get_graphics_processing_unit_architecture(self):
        return self.graphics_processing_unit_architecture

    def get_all_features(self):
        return {
            "Instruction Set Architecture": self.get_instruction_set_architecture(),
            "Execute Unit Architecture": self.get_execute_unit_architecture(),
            "Memory Management Unit Architecture": self.get_memory_management_unit_architecture(),
            "Load/Store Unit Architecture": self.get_load_store_unit_architecture(),
            "Branch Prediction Unit Architecture": self.get_branch_prediction_unit_architecture(),
            "Floating Point Unit Architecture": self.get_floating_point_unit_architecture(),
            "Graphics Processing Unit Architecture": self.get_graphics_processing_unit_architecture()
        }
