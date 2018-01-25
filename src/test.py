from audio_validator import Audio_validator

if __name__ == '__main__':
    rc = Audio_validator('test.wav')
    print rc.check(5000, 1000, 0.9)