import numpy as np

from collections import deque
from skimage import transform
from PIL import Image, ImageEnhance 

class Preprocessor:

    def preprocess_frame(frame, frame_size):
        preprocessed_frame = transform.resize(frame, [frame_size, frame_size])
        return preprocessed_frame

    def stack_frames(frame, stacked_frames, frame_size, stack_size):
        # Preprocess frame
        frame = Preprocessor.preprocess_frame(frame, frame_size)

        if len(stacked_frames) < stack_size:
            # Clear our previously stacked frames
            print('Creating new stack')
            stacked_frames = deque([np.zeros((frame_size,frame_size), dtype=np.int) for i in range(stack_size)], maxlen=stack_size)
            # Initialize the frames deque by copying the same frame "stack_size" times
            for _ in range(stack_size):
                print('New frame!')
                stacked_frames.append(frame)
        else:
            # Append the frames to the deque
            print('New frame!')
            stacked_frames.append(frame)
        
        # Create an stack out of the deque
        stacked_state = np.stack(stacked_frames, axis=2) 
        stacked_state = stacked_state.reshape((frame_size, frame_size, stack_size*3))
        return stacked_state, stacked_frames