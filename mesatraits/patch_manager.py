import random

class PatchManager:
    
    """
    Class that helps defining the patches into the model.
    
    attributes:

        ungrown_patches: list of all non grown patches
        
    methods:
        grow_patches
        add_patch
        remove_patch
    
    """
    
    def __init__(self):
       
        self.ungrown_patches = []
       
    def add_patch(self, patch):
        """
        Adds one patch to the  patch manager. Function that respects encapsulation
        """
        self.ungrown_patches.append(patch)   
    
    def remove_patch(self, patch):
        """
        removes one patch from patch manager. Function that respects encapsulation
        """
        self.ungrown_patches.remove(patch)
    
            
    def grow_patches(self):  
        """
        forces the growth of patches.and updates the list of ungrown patches
        """
        #randomize the order in which patches are called - 
        # it really makes a difference
        self.ungrown_patches = random.sample(self.ungrown_patches, len(self.ungrown_patches))
        while len(self.ungrown_patches) > 0:
            updated_ungrown_patches = []    
            for patch in self.ungrown_patches: #to randomize
                patch.become_patch()
                if not patch.is_grown():
                    updated_ungrown_patches.append(patch)
            self.ungrown_patches = updated_ungrown_patches