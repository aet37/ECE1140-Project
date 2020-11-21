# Created by Kenneth Meier
# Block implementation class

# SYSTEM INCLUDES
import sys
sys.path.append(".")

# Python PROJECT INCLUDES
from src.TrainModel.Block import Block
from src.signals import signals
class BlockCatalogue:
    # Call "m_blocklist.count()" for amount of blocks
    # Call "m_blocklist.append()" to add a block
    # Call "m_blocklist[#]" to load a specific block
    def __init__ (self):
        self.m_blockList = []

        # Receive blocks from evan
        # signals.TRAIN_MODEL_DISPATCH_TRAIN.connect(self.train_model_dispatch_train)


block_catalogue = BlockCatalogue()
