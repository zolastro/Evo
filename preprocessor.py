import numpy as np

from collections import deque
from skimage import transform
from PIL import Image, ImageEnhance 

class Preprocessor:
    def __init__(self, stack_size, frame_size):
        self.stack_size = stack_size

    def _preprocess_frame(self, frame):
        print(frame)
        preprocessed_frame = transform.resize(normalized_frame, [frame_size,frame_size])
        return preprocessed_frame


    def stack_frames(self, stacked_frames, state):
        # Preprocess frame
        frame = self._preprocess_frame(state)
        frame = np.expand_dims(frame, axis=0)

        if len(stack_frames) < stack_size:
            # Clear our previously stacked frames
            stacked_frames = deque([np.zeros((frame_size,frame_size), dtype=np.int) for i in range(self.stack_size)], maxlen=self.stack_size)
            # Initialize the frames deque by copying the same frame "stack_size" times
            for _ in range(self.stack_size):
                stacked_frames.append(frame)
        else:
            # Append the frames to the deque
            stacked_frames.append(frame)
        
        # Create an stack out of the deque
        stacked_state = np.stack(stacked_frames, axis=3) 
        stacked_state = stacked_state.reshape((frame_size, frame_size, self.stack_size))
        return stacked_state, stacked_frames