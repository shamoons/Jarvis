import pyaudio
import wave
import time

def test_microphone():
    try:
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Print available devices
        print("\nAvailable audio devices:")
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            print(f"Device {i}: {dev_info['name']}")
        
        # Try to open default input device
        stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       input=True,
                       frames_per_buffer=1024)
        
        print("\nMicrophone test successful!")
        print("Recording 3 seconds of audio...")
        
        # Record for 3 seconds
        frames = []
        for _ in range(0, int(44100 / 1024 * 3)):
            data = stream.read(1024)
            frames.append(data)
        
        print("Recording completed!")
        
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    except Exception as e:
        print(f"\nError testing microphone: {str(e)}")
        print("\nDetailed error information:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_microphone() 