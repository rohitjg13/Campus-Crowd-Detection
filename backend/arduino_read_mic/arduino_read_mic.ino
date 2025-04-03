void setup() {
    Serial.begin(115200);
}

void loop() {
    unsigned int sample = analogRead(A0);
    
    // Send as 2 bytes (10-bit ADC)
    Serial.write(lowByte(sample));
    Serial.write(highByte(sample));

    delayMicroseconds(10);  // ~8kHz sample rate (1 sec / 8000 samples)
}