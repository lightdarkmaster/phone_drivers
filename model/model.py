class AndroidArchitecture:
    def __init__(self, instruction_set_architecture, execute_unit_architecture, memory_management_unit_architecture, 
                 load_store_unit_architecture, branch_prediction_unit_architecture, 
                 floating_point_unit_architecture, graphics_processing_unit_architecture):
        self.instruction_set_architecture = instruction_set_architecture
        self.execute_unit_architecture = execute_unit_architecture
        self.memory_management_unit_architecture = memory_management_unit_architecture
        self.load_store_unit_architecture = load_store_unit_architecture
        self.branch_prediction_unit_architecture = branch_prediction_unit_architecture
        self.floating_point_unit_architecture = floating_point_unit_architecture
        self.graphics_processing_unit_architecture = graphics_processing_unit_architecture
    
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
