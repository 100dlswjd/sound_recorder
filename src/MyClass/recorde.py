from threading import Thread, Event

class recorder:
    import pyaudio
    import wave
    MIC_DEVICE_ID = 1
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    SAMPLE_SIZE = 2  # FORMAT의 바이트 수

    def __init__(self):
        self.p = self.pyaudio.PyAudio()
        self.recorde_stop_flag = False
        self.stream = self.p.open(input_device_index=self.MIC_DEVICE_ID,
                        format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        self.frames = []
        self.exit_event = Event()
        self.exit_event.clear()
        self.recorde_thread = Thread(target = self.recorde_thread_proc)

    def recorde_thread_proc(self):
        while self.exit_event.is_set() == False:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def recorde_start(self):
        self.recorde_thread.start()
     
    def recorde_stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.exit_event.set()

    # 녹음 데이터를 WAV 파일로 저장하기
    def save_wav(self, file_name = "output.wav"):
        wf = self.wave.open(file_name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.SAMPLE_SIZE)
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
    
        if isinstance(file_name, str):
            wf.close()